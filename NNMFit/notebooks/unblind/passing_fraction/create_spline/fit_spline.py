#!/usr/bin/env python3
"""
Fit photosplines to the passing-fraction grid produced by compute_pf_grid.py.

Reads all depth_NNN_cos_theta_NNN.pickle files from a grid directory, assembles
the 3D (depth × cos_theta × log10_energy) array, and fits a tensor B-spline to
log10(PF) using photospline.glam_fit.

Usage:
    python fit_spline.py --grid-dir /path/to/grid/ --spline-dir /path/to/splines/
"""

import os
import glob
import pickle
import argparse
import numpy as np
from photospline import glam_fit, ndsparse

# ── Grid definition — must match compute_pf_grid.py ──────────────────────────
DEPTH_GRID      = np.linspace(1400, 3000, 11)   # metres
COS_THETA_GRID  = np.linspace(0.05, 1.0, 21)
ENERGIES_GEV    = np.logspace(1, 9, 51)
LOG_E_GRID      = np.log10(ENERGIES_GEV)

# ── Spline properties — tuned to follow nlad's grid fitter ───────────────────
SPLINE_ORDER    = [2, 2, 2]
SMOOTHING       = [1e-4, 1e-6, 1e-3]
PENALTY_ORDER   = [2, 2, 2]


def pad_knots(knots, order):
    pre  = knots[0]  - (knots[1]  - knots[0])  * np.arange(order, 0, -1)
    post = knots[-1] + (knots[-1] - knots[-2]) * np.arange(1, order + 1)
    return np.concatenate((pre, knots, post))


def knots_between_grid(grid, order):
    w = grid[1] - grid[0]
    knots = np.linspace(grid[0] - w / 2, grid[-1] + w / 2, len(grid) + 1)
    return pad_knots(knots, order)


def load_grid(grid_dir: str, kind: str) -> np.ndarray:
    """Assemble 3D PF array (n_depth × n_costh × n_energy) for one kind."""
    pf_grid = np.empty(
        (len(DEPTH_GRID), len(COS_THETA_GRID), len(ENERGIES_GEV)),
        dtype=np.float32
    )
    missing = []
    for i_d, depth in enumerate(DEPTH_GRID):
        for i_c, cos_theta in enumerate(COS_THETA_GRID):
            fname = os.path.join(
                grid_dir,
                f"depth_{depth:.0f}_cos_theta_{cos_theta:.2f}.pickle"
            )
            if not os.path.exists(fname):
                missing.append(fname)
                pf_grid[i_d, i_c, :] = np.nan
                continue
            with open(fname, "rb") as fh:
                res = pickle.load(fh)
            pf_grid[i_d, i_c, :] = res[kind]["pfs"]

    if missing:
        print(f"  WARNING: {len(missing)} missing grid file(s), e.g. {missing[0]}")
    return pf_grid


def fit_splines(grid_dir: str, spline_dir: str, kinds=None):
    os.makedirs(spline_dir, exist_ok=True)

    # auto-detect available kinds from first file if not specified
    if kinds is None:
        sample_files = glob.glob(os.path.join(grid_dir, "depth_*.pickle"))
        if not sample_files:
            raise FileNotFoundError(f"No grid pickles found in {grid_dir}")
        with open(sample_files[0], "rb") as fh:
            kinds = list(pickle.load(fh).keys())

    knots = [
        knots_between_grid(DEPTH_GRID,    SPLINE_ORDER[0]),
        knots_between_grid(COS_THETA_GRID, SPLINE_ORDER[1]),
        knots_between_grid(LOG_E_GRID,     SPLINE_ORDER[2]),
    ]
    grid_axes = [DEPTH_GRID, COS_THETA_GRID, LOG_E_GRID]

    for kind in kinds:
        print(f"Fitting: {kind}")
        pf_grid = load_grid(grid_dir, kind)

        n_nan = np.sum(~np.isfinite(pf_grid))
        if n_nan:
            print(f"  {n_nan} non-finite values — replacing with 0 before log")
        pf_grid = np.clip(pf_grid, 1e-12, 1.0)

        log_pf = np.log10(pf_grid)
        zs, w  = ndsparse.from_data(log_pf, np.ones_like(log_pf))

        spline = glam_fit(zs, w, grid_axes, knots,
                          SPLINE_ORDER, SMOOTHING, PENALTY_ORDER)

        safe_kind = kind.replace(" ", "_")
        out_path  = os.path.join(spline_dir, f"pf_spline_{safe_kind}.fits")
        spline.write(out_path)
        print(f"  → {out_path}")

    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fit photosplines to a passing-fraction grid."
    )
    parser.add_argument("--grid-dir",   required=True,
                        help="Directory containing compute_pf_grid.py output pickles")
    parser.add_argument("--spline-dir", required=True,
                        help="Output directory for .fits spline files")
    args = parser.parse_args()

    fit_splines(args.grid_dir, args.spline_dir)
