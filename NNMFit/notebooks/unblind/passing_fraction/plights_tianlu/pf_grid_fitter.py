#!/usr/bin/env python3
"""
Fit photosplines to the passing-fraction grid produced by nuveto_cluster_script.py.

Adapted from /data/user/nlad/PassingFractions/v0_2021_passing_fraction_grid_fitter.py.

Key differences from nlad's version:
  - No prpl/plight dimension: each grid pickle contains res[kind]["pfs"] directly,
    rather than res[kind][prpl]["pfs"].  One spline per neutrino kind.
  - Energy key is "energies_gev" (not "energies").
  - Uses standard logging (no pf_logging dependency).
  - Fixed bug in knots_in_grid: uses len(var_grid) not len(depth_grid) for every axis.
  - Output: pf_spline_{kind}.fits flat in splines_dir (no per-kind subdirectory).

Usage:
    python pf_grid_fitter.py --res PF_GRID_DIR --out SPLINES_DIR [options]
"""

import glob
import logging
import os
import pickle

import numpy as np
from photospline import glam_fit, ndsparse

logger = logging.getLogger(__name__)


class PF_Grid_Fitter:

    def __init__(self, res_dir):
        """
        Read grid metadata and detect available kinds.

        Args:
            res_dir: directory containing nuveto_cluster_script.py output pickles
                     and info.pickle written by create_dag.py.
        """
        self.res_dir = res_dir if res_dir.endswith("/") else res_dir + "/"

        info_path = os.path.join(res_dir, "info.pickle")
        if not os.path.exists(info_path):
            raise FileNotFoundError(
                f"info.pickle not found in {res_dir}. "
                "Run create_dag.py to generate it before submitting jobs."
            )
        with open(info_path, "rb") as fh:
            grid_info = pickle.load(fh)

        # read one result file to get energy grid and kind list
        sample_files = glob.glob(self.res_dir + "depth_*.pickle")
        if not sample_files:
            raise FileNotFoundError(f"No depth_*.pickle files found in {res_dir}")
        with open(sample_files[0], "rb") as fh:
            sample = pickle.load(fh)

        self.kinds = list(sample.keys())
        logger.info(f"Found kinds: {self.kinds}")

        grid_info["energy_grid"] = sample[self.kinds[0]]["energies_gev"]
        self.grid_info = grid_info

        nuveto_info = sample[self.kinds[0]]["info"]
        logger.info(f'Primary CR model : {nuveto_info["pmodel"]}')
        logger.info(f'Hadronic model   : {nuveto_info["hadr"]}')
        logger.info(f'Density model    : {nuveto_info["density"]}')

    def npx_results_to_grid(self, kind,
                             drop_depth_points=0,
                             drop_theta_points=0,
                             cut_energy=None):
        """
        Assemble the 3D PF array (n_depth × n_cos_theta × n_energy) for one kind.

        Args:
            kind             : neutrino kind string, e.g. "conv nu_mu"
            drop_depth_points: drop this many depth slices from the shallow end
            drop_theta_points: drop this many cos_theta slices from the low end
            cut_energy       : discard energies above this value [GeV]
        """
        depth_grid     = self.grid_info["depth_grid"]
        cos_theta_grid = self.grid_info["cos_theta_grid"]
        energy_grid    = self.grid_info["energy_grid"]

        pf_grid = np.empty(
            (len(depth_grid), len(cos_theta_grid), len(energy_grid)),
            dtype=np.float32,
        )

        for d, depth in enumerate(depth_grid):
            for c, cos_theta in enumerate(cos_theta_grid):
                fname = self.res_dir + f"depth_{depth:.0f}_cos_theta_{cos_theta:.2f}.pickle"
                with open(fname, "rb") as fh:
                    res = pickle.load(fh)
                pf_grid[d, c, :] = res[kind]["pfs"]

        pf_grid = pf_grid[drop_depth_points:, drop_theta_points:, :]

        grid_info_mod = {
            "depth_grid":     depth_grid[drop_depth_points:],
            "cos_theta_grid": cos_theta_grid[drop_theta_points:],
            "energy_grid":    energy_grid,
        }

        if cut_energy is not None:
            cut_idx = np.argmin(np.abs(energy_grid - cut_energy))
            pf_grid = pf_grid[:, :, : cut_idx + 1]
            grid_info_mod["energy_grid"] = energy_grid[: cut_idx + 1]

        return grid_info_mod, pf_grid

    def grid_to_splines(self, splines_dir, spline_prop,
                        drop_depth_points=0, drop_theta_points=0,
                        cut_energy=None):
        """
        Fit and write one spline per neutrino kind.

        Args:
            splines_dir       : output directory for .fits files and info.pickle
            spline_prop       : dict with keys "order", "smoothing", "penalty_order"
            drop_depth_points : drop this many depth slices from the shallow end
            drop_theta_points : drop this many cos_theta slices from the low end
            cut_energy        : discard energies above this value [GeV]
        """
        os.makedirs(splines_dir, exist_ok=True)

        for kind in self.kinds:
            logger.info(f"Fitting: {kind}")
            grid_info_mod, data = self.npx_results_to_grid(
                kind, drop_depth_points, drop_theta_points, cut_energy
            )

            n_nonfinite = np.sum(~np.isfinite(data))
            if n_nonfinite:
                logger.warning(
                    f"  {n_nonfinite} non-finite values for {kind} — "
                    f"indices: {np.argwhere(~np.isfinite(data))[:5]}"
                )

            spline = self.fit_spline_to_grid(grid_info_mod, data, spline_prop)

            out_path = os.path.join(splines_dir,
                                    f"pf_spline_{kind.replace(' ', '_')}.fits")
            spline.write(out_path)
            logger.info(f"  → {out_path}")

        # save grid info alongside splines
        grid_info_mod.update({"kinds": self.kinds})
        with open(os.path.join(splines_dir, "info.pickle"), "wb") as fh:
            pickle.dump(grid_info_mod, fh)

    @staticmethod
    def fit_spline_to_grid(grid_info, griddata, spline_prop):
        """
        Fit a tensor B-spline to log10(PF) on a 3D grid.

        Args:
            grid_info  : dict with depth_grid, cos_theta_grid, energy_grid
            griddata   : 3D array of PF values, shape (n_d, n_c, n_e)
            spline_prop: dict with order, smoothing, penalty_order
        """
        # replace NaN (failed nuVeto jobs) with 1e-12 before log — np.clip
        # leaves NaN intact, which would corrupt the entire spline
        data_clipped = np.clip(np.where(np.isfinite(griddata), griddata, 1e-12),
                               1e-12, 1.0)
        zs, w = ndsparse.from_data(np.log10(data_clipped),
                                   np.ones_like(data_clipped))

        depth_grid     = grid_info["depth_grid"]
        cos_theta_grid = grid_info["cos_theta_grid"]
        log_e_grid     = np.log10(grid_info["energy_grid"])

        def knots_in_grid(var_grid, order):
            nknots = len(var_grid) + 1
            width  = var_grid[1] - var_grid[0]
            knots  = np.linspace(var_grid[0] - width / 2,
                                 var_grid[-1] + width / 2,
                                 nknots)
            return pad_knots(knots, order)

        order = spline_prop["order"]
        knots = [
            knots_in_grid(depth_grid,     order[0]),
            knots_in_grid(cos_theta_grid, order[1]),
            knots_in_grid(log_e_grid,     order[2]),
        ]
        grid_axes = [depth_grid, cos_theta_grid, log_e_grid]

        return glam_fit(zs, w, grid_axes, knots,
                        order,
                        spline_prop["smoothing"],
                        spline_prop["penalty_order"])


def pad_knots(knots, order=2):
    pre  = knots[0]  - (knots[1]  - knots[0])  * np.arange(order, 0, -1)
    post = knots[-1] + (knots[-1] - knots[-2]) * np.arange(1, order + 1)
    return np.concatenate((pre, knots, post))


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description="Fit photosplines to a nuVeto passing-fraction grid."
    )
    parser.add_argument("--res",            required=True,
                        help="Grid calculation results directory")
    parser.add_argument("--out",            required=True,
                        help="Output spline directory")
    parser.add_argument("--drop_N_depth",   default=0,  type=int,
                        help="Drop the first N depth slices (shallowest)")
    parser.add_argument("--drop_N_theta",   default=0,  type=int,
                        help="Drop the first N cos_theta slices (lowest values)")
    parser.add_argument("--cut_energy",     default=None,
                        help="Discard energy grid points above CUT_ENERGY [GeV]")
    parser.add_argument("--log-level",      default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(levelname)s  %(name)s  %(message)s",
    )

    if args.cut_energy is not None:
        args.cut_energy = float(args.cut_energy)

    spline_prop = {
        "order":         [2, 2, 2],
        "penalty_order": [2, 2, 2],
        "smoothing":     [1e-4, 1e-6, 1e-3],
    }

    hdl = PF_Grid_Fitter(args.res)
    hdl.grid_to_splines(
        splines_dir=args.out,
        spline_prop=spline_prop,
        drop_depth_points=args.drop_N_depth,
        drop_theta_points=args.drop_N_theta,
        cut_energy=args.cut_energy,
    )
    print(f"Splines written to: {args.out}")


if __name__ == "__main__":
    main()
