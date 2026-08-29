#!/usr/bin/env python3
"""
Compute nuVeto atmospheric passing fractions at one (depth, cos_theta) point.

Designed to run as one cluster job per (depth, cos_theta) pair. All eight
neutrino kinds are computed in a single job to amortise the MCEq initialisation
cost (~30–60 s per kind).

Usage:
    python compute_pf_grid.py -d 1950 -c 0.5 -o /path/to/grid_output/
"""

import os
import sys
import argparse
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

# ice_allm97_step_1: Heaviside detection probability at 1 TeV.
# This differs from the HESE depth-dependent prpl used for the original
# GlobalFit splines. To reproduce those exactly, the ice_allm97_hese_depth_NNN
# files (from rnaab's Python 3.6 nuVeto venv) would need to be converted to
# .npz format and placed in the current venv's nuVeto/data/prpl/ directory.
PRPL = "ice_allm97_step_1"

# ── Neutrino kinds ────────────────────────────────────────────────────────────
ALL_KINDS = [
    "conv nu_mu", "conv nu_mubar",
    "conv nu_e",  "conv nu_ebar",
    "pr nu_mu",   "pr nu_mubar",
    "pr nu_e",    "pr nu_ebar",
]

# ── Energy grid ───────────────────────────────────────────────────────────────
# 51 log-spaced points from 10 GeV to 10^9 GeV — same range as nlad's grid
ENERGIES_GEV = np.logspace(1, 9, 51)


def compute_pf(depth_m: float, cos_theta: float, kinds=ALL_KINDS) -> dict:
    results = {}
    for kind in kinds:
        t0 = time.time()
        pf_list = []
        for e_gev in ENERGIES_GEV:
            pf = passing(
                e_gev * Units.GeV,
                cos_theta,
                kind=kind,
                prpl=PRPL,
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
                "prpl":      PRPL,
                "pmodel":    "HillasGaisser2012 H3a",
                "hadr":      HADR,
                "density":   str(DENSITY),
            },
        }
        print(f"  {kind}: {time.time() - t0:.1f} s")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compute passing fractions at one (depth, cos_theta) point."
    )
    parser.add_argument("-d", "--depth",     type=float, required=True,
                        help="Vertical depth in metres (e.g. 1950)")
    parser.add_argument("-c", "--cos-theta", type=float, required=True,
                        dest="cos_theta",
                        help="cos(zenith angle), range [0.05, 1.0]")
    parser.add_argument("-o", "--out",       type=str,   required=True,
                        help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    outfile = os.path.join(
        args.out,
        f"depth_{args.depth:.0f}_cos_theta_{args.cos_theta:.2f}.pickle"
    )

    print(f"depth={args.depth} m  cos_theta={args.cos_theta}  →  {outfile}")
    t_start = time.time()
    results = compute_pf(args.depth, args.cos_theta)
    print(f"Total: {time.time() - t_start:.1f} s")

    with open(outfile, "wb") as fh:
        pickle.dump(results, fh)
    print("Done.")
