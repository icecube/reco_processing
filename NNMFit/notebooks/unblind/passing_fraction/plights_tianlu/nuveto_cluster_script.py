#!/usr/bin/env python3
"""
Compute nuVeto atmospheric passing fractions at one (depth, cos_theta) point
using depth-dependent prpl files built from plights.pkl.

One cluster job per (depth, cos_theta) pair; all requested neutrino kinds are
computed in a single job to amortise the MCEq initialisation cost.

The correct prpl file is selected automatically from --prpl-dir by finding the
z-slice whose rounded z-coordinate is nearest to (1948 - depth_m).

Usage (called by nuveto_cluster_script.sh):
    python nuveto_cluster_script.py -c COS_THETA -d DEPTH_M -o OUTFILE
        [-k KIND1,KIND2,...] [--prpl-dir PRPL_DIR]
"""

import argparse
import os
import pickle
import time

import numpy as np
from nuVeto.nuveto import passing
from nuVeto.utils import Units
import crflux.models as pm

# ── nuVeto parameters ─────────────────────────────────────────────────────────
PMODEL  = (pm.HillasGaisser2012, "H3a")
HADR    = "SIBYLL2.3E"
DENSITY = ("CORSIKA", ("SouthPole", "December"))

ALL_KINDS = [
    "conv nu_mu", "conv nu_mubar",
    "conv nu_e",  "conv nu_ebar",
    "pr nu_mu",   "pr nu_mubar",
    "pr nu_e",    "pr nu_ebar",
]

ENERGIES_GEV = np.logspace(1, 9, 51)

DEFAULT_PRPL_DIR = "/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/unblind/passing_fraction/plights_tianlu/prpl_output"


def build_prpl_dict(prpl_dir):
    """Scan prpl_dir for ice_allm97_hese_depth_*.npz and return {z_int: path}."""
    d = {}
    prefix = "ice_allm97_hese_depth_"
    for fname in os.listdir(prpl_dir):
        if not (fname.startswith(prefix) and fname.endswith(".npz")):
            continue
        stem = fname[len(prefix):-len(".npz")]
        z = -int(stem[len("minus"):]) if stem.startswith("minus") else int(stem)
        d[z] = os.path.join(prpl_dir, fname)
    return d


def pick_prpl(depth_m, prpl_dict):
    """Return path of the prpl file whose z is nearest to (1948 - depth_m)."""
    z_target = 1948.0 - depth_m
    z_keys = np.array(list(prpl_dict.keys()), dtype=float)
    z_nearest = int(z_keys[np.argmin(np.abs(z_keys - z_target))])
    return prpl_dict[z_nearest]


def parse_kinds(kind_str):
    """Convert comma-separated kind string (e.g. 'conv_nu_mu,pr_nu_e') to nuVeto format."""
    kinds = []
    for k in kind_str.split(","):
        k = k.strip().replace("conv_", "conv ").replace("pr_", "pr ")
        kinds.append(k)
    return kinds


def compute_pf(cos_theta, depth_m, prpl_path, kinds=ALL_KINDS):
    results = {}
    for kind in kinds:
        t0 = time.time()
        pf_list = []
        for e_gev in ENERGIES_GEV:
            pf = passing(
                e_gev * Units.GeV,
                cos_theta,
                kind=kind,
                prpl=prpl_path,
                pmodel=PMODEL,
                hadr=HADR,
                depth=int(depth_m) * Units.m,
                density=DENSITY,
            )
            pf_list.append(float(pf))
        results[kind] = {
            "energies_gev": ENERGIES_GEV.copy(),
            "pfs":          np.array(pf_list),
            "info": {
                "cos_theta": cos_theta,
                "depth_m":   depth_m,
                "kind":      kind,
                "prpl":      prpl_path,
                "pmodel":    "HillasGaisser2012 H3a",
                "hadr":      HADR,
                "density":   str(DENSITY),
            },
        }
        print(f"  {kind}: {time.time() - t0:.1f} s", flush=True)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compute passing fractions at one (depth, cos_theta) point."
    )
    parser.add_argument("-c", "--cos-theta", type=float, required=True, dest="cos_theta")
    parser.add_argument("-d", "--depth",     type=float, required=True, dest="depth_m")
    parser.add_argument("-o", "--outfile",   type=str,   required=True)
    parser.add_argument("-k", "--kind",      type=str,
                        default=",".join(k.replace(" ", "_") for k in ALL_KINDS),
                        help="Comma-separated neutrino kinds, e.g. conv_nu_mu,pr_nu_e")
    parser.add_argument("--prpl-dir",        type=str,   default=DEFAULT_PRPL_DIR,
                        dest="prpl_dir")
    args = parser.parse_args()

    prpl_dict = build_prpl_dict(args.prpl_dir)
    prpl_path = pick_prpl(args.depth_m, prpl_dict)
    kinds     = parse_kinds(args.kind)

    print(f"cos_theta={args.cos_theta}  depth={args.depth_m} m")
    print(f"prpl: {os.path.basename(prpl_path)}")
    print(f"kinds: {kinds}")

    t_start = time.time()
    results = compute_pf(args.cos_theta, args.depth_m, prpl_path, kinds=kinds)
    print(f"Total: {time.time() - t_start:.1f} s")

    with open(args.outfile, "wb") as fh:
        pickle.dump(results, fh)
    print(f"Saved → {args.outfile}")
