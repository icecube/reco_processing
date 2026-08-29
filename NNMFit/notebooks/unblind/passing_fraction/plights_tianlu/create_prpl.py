#!/usr/bin/env python3
"""
Create depth-dependent prpl NPZ files using the P_light functions from plights.pkl.

For each depth slice in plights.pkl, constructs a modified_sigmoid P_light function
and convolves it with the MMC muon-reaching probability (ice_allm97) to produce
a prpl(ei, l) interpolator, saved as a nuVeto-compatible NPZ file.

The output files can be passed directly to nuVeto's passing() via the prpl argument:

    from nuVeto import passing
    from nuVeto.utils import Units
    import crflux.models as pm

    pf = passing(
        1e5 * Units.GeV, 0.5,
        kind='conv nu_mu',
        prpl='/path/to/prpl_output/ice_allm97_hese_depth_1950.npz',
        pmodel=(pm.HillasGaisser2012, 'H3a'),
        hadr='SIBYLL2.3E',
        depth=1950 * Units.m,
        density=('CORSIKA', ('SouthPole', 'December')),
    )

Usage:
    python create_prpl.py [--out-dir OUTPUT_DIR]

Runtime: ~30–60 s per depth slice (50 slices total), dominated by the
         groupby integration in nuVeto.mu.int_ef.
"""

import argparse
import os
import pickle
import time
from importlib import resources

import numpy as np
from nuVeto.mu import int_ef

PLIGHTS_PKL = os.path.join(os.path.dirname(__file__), "plights.pkl")
DEFAULT_OUT_DIR = os.path.join(os.path.dirname(__file__), "prpl_output")


def modified_sigmoid(emu, k0, x0, k1, x1, c):
    """New depth-dependent P_light: sigmoid + Gaussian bump, goes to 0 at low E."""
    x = np.log10(np.asarray(emu, dtype=float))
    return 1 / (1 + np.exp(-k0 * (x - x0))) + c * np.exp(-(x - x1) ** 2 / k1)


def load_preach():
    """Load MMC ice_allm97 preach data from the current nuVeto installation."""
    with resources.files("nuVeto").joinpath("data", "mmc", "ice_allm97.npz").open("rb") as f:
        return np.load(f)["data"]


def build_prpl_grid(preach_arr, plight_fn):
    """
    Integrate preach × plight over ef, pivot to (ei × l) grid.

    Returns:
        ei_grid : 1D array of initial muon energies [GeV]
        l_grid  : 1D array of ice column lengths [m]
        values  : 2D array of prpl, shape (n_ei, n_l), clipped to [0, 1]
    """
    import pandas as pd
    from scipy import interpolate

    intg = int_ef(preach_arr, plight_fn)
    df = pd.DataFrame(intg, columns=["ei", "l", "prpl"])
    df = df.pivot_table(index="ei", columns="l", values="prpl").fillna(0)
    values = np.clip(df.values, 0.0, 1.0)
    return df.index.values, df.columns.values, values


def save_npz(out_path, ei_grid, l_grid, values):
    """Save prpl grid as a nuVeto-compatible NPZ file."""
    np.savez(
        out_path,
        grid_0=ei_grid,
        grid_1=l_grid,
        values=values,
        method="linear",
        fill_value="None",
        bounds_error=False,
    )


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)

    print("Loading MMC preach data (ice_allm97) …")
    preach = load_preach()
    print(f"  {preach.shape[0]:,} rows — ei: {preach[:,0].min():.1f}–{preach[:,0].max():.2e} GeV, "
          f"l: {preach[:,1].min():.0f}–{preach[:,1].max():.0f} m")

    with open(PLIGHTS_PKL, "rb") as fh:
        raw = pickle.load(fh, encoding="latin1")

    entries = sorted(
        [{"z": z, "depth_m": 1948.0 - z, "params": p} for z, p in raw.items()],
        key=lambda e: e["depth_m"],
    )
    print(f"Found {len(entries)} depth slices: "
          f"{entries[0]['depth_m']:.1f}–{entries[-1]['depth_m']:.1f} m\n")

    for i, e in enumerate(entries, 1):
        z = e["z"]
        depth_m = e["depth_m"]
        params = e["params"]

        plight_fn = lambda emu, p=params: modified_sigmoid(emu, *p)

        z_int = round(z)
        z_suffix = f"minus{abs(z_int)}" if z_int < 0 else str(z_int)
        out_path = os.path.join(out_dir, f"ice_allm97_hese_depth_{z_suffix}.npz")
        print(f"[{i:2d}/{len(entries)}] z={z_int:+d} (depth={depth_m:.1f} m) → {os.path.basename(out_path)} … ",
              end="", flush=True)

        t0 = time.time()
        ei_grid, l_grid, values = build_prpl_grid(preach, plight_fn)
        save_npz(out_path, ei_grid, l_grid, values)
        print(f"{time.time() - t0:.1f} s")

    print("\nDone. Output written to:", out_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create depth-dependent prpl NPZ files from plights.pkl."
    )
    parser.add_argument(
        "--out-dir", default=DEFAULT_OUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUT_DIR})"
    )
    args = parser.parse_args()
    main(args.out_dir)
