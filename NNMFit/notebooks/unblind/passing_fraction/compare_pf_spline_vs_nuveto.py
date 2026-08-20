#!/usr/bin/env python3
"""
Compare conventional/prompt neutrino passing fractions from:
  1. Spline evaluator  (Spline_Evaluator from /data/user/nlad/PassingFractions/)
  2. nuVeto            (nuVeto.passing)

Three scans are performed:
  - PF vs log10(E)  at fixed depth and cos_theta grid
  - PF vs cos_theta at fixed depth and energy grid
  - PF vs depth     at fixed E=1e5 GeV and cos_theta=0.5

Usage:
  python compare_pf_spline_vs_nuveto.py --flux-type conv --flavor nu_mu
  python compare_pf_spline_vs_nuveto.py --flux-type pr   --flavor nu_mubar --test

Run all 8 combinations via:
  bash compare_pf_spline_vs_nuveto.sh
"""

import argparse
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tqdm import tqdm

# ── Spline evaluator ───────────────────────────────────────────────────────────
sys.path.insert(0, "/data/user/nlad/PassingFractions/")
from spline_evaluator import Spline_Evaluator

# ── nuVeto ─────────────────────────────────────────────────────────────────────
from nuVeto import passing
from nuVeto.utils import Units
import crflux.models as pm

# ── PDG codes ──────────────────────────────────────────────────────────────────
_PID = {"nu_e": 12, "nu_ebar": -12, "nu_mu": 14, "nu_mubar": -14}

# ── nuVeto physics configuration ───────────────────────────────────────────────
NUVETO_PMODEL  = (pm.HillasGaisser2012, "H3a")
NUVETO_HADR    = "SIBYLL2.3E"
NUVETO_DENSITY = ("CORSIKA", ("SouthPole", "December"))

# ── Default scan grids ─────────────────────────────────────────────────────────
# Energy: one point per decade, capped at spline max (~10^6.88 GeV)
LOG_E_MIN, LOG_E_MAX = 2, 7
N_E_PER_DECADE = 1
ENERGIES_GEV_DEFAULT = np.logspace(LOG_E_MIN, LOG_E_MAX,
                                    (LOG_E_MAX - LOG_E_MIN) * N_E_PER_DECADE + 1)

# cos_theta: 0.1 to 1.0 in steps of 0.1
COS_THETA_DEFAULT = np.round(np.arange(0.1, 1.01, 0.1), decimals=1)

# Fixed IceCube nominal depth for E and cos_theta scans
DEPTH_M = 1950.0

# Depth scan: fixed E and zenith
DEPTH_SCAN_E_GEV  = 1e5
DEPTH_SCAN_COSZEN = 0.5
DEPTH_GRID = np.linspace(1400, 3000, 17)  # m, within spline valid range [1400,3000]


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--flux-type", choices=["conv", "pr"], default="conv",
                   dest="flux_type", help="Flux component (default: conv)")
    p.add_argument("--flavor",
                   choices=["nu_e", "nu_ebar", "nu_mu", "nu_mubar"],
                   default="nu_mu", help="Neutrino flavor (default: nu_mu)")
    p.add_argument("--test", action="store_true",
                   help="Quick 2-point test run")
    return p.parse_args()


# ── Evaluation helpers ─────────────────────────────────────────────────────────

def spline_pf(hdl, energy_gev, cos_theta, kind, flavor, depth_m=DEPTH_M):
    zenith = np.arccos(np.clip(cos_theta, -1, 1))
    log_pf = hdl.evaluate(
        kind,
        pid    = np.array([_PID[flavor]]),
        depth  = np.array([depth_m]),
        zenith = np.array([zenith]),
        energy = np.array([energy_gev]),
    )
    return float(10.0 ** log_pf[0])


def nuveto_pf(energy_gev, cos_theta, kind_str, depth_m=DEPTH_M):
    return float(passing(
        energy_gev * Units.GeV,
        cos_theta,
        kind    = kind_str,
        pmodel  = NUVETO_PMODEL,
        hadr    = NUVETO_HADR,
        depth   = depth_m * Units.m,
        density = NUVETO_DENSITY,
    ))


# ── Formatting helpers ─────────────────────────────────────────────────────────

def fmt_table(header, rows):
    widths = [len(h) for h in header]
    for row in rows:
        for i, c in enumerate(row):
            widths[i] = max(widths[i], len(str(c)))
    sep = "  ".join("-" * w for w in widths)
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    lines = [fmt.format(*header), sep]
    for row in rows:
        lines.append(fmt.format(*[str(c) for c in row]))
    return "\n".join(lines)


def scan_block(label, x_name, x_vals, pf_spl, pf_nuv, ratio, x_fmt=".4f"):
    header = [x_name, "spline", "nuVeto", "ratio_S/N"]
    rows = []
    for k, x in enumerate(x_vals):
        rows.append([f"{x:{x_fmt}}",
                     f"{pf_spl[k]:.6f}",
                     f"{pf_nuv[k]:.6f}",
                     f"{ratio[k]:.6f}" if np.isfinite(ratio[k]) else "nan"])
    return f"{label}\n" + fmt_table(header, rows)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    args      = parse_args()
    flux_type = args.flux_type
    flavor    = args.flavor
    kind      = f"{flux_type} {flavor}"

    energies   = np.logspace(LOG_E_MIN, LOG_E_MAX, 3) if args.test \
                 else ENERGIES_GEV_DEFAULT
    cos_thetas = np.array([0.3, 0.7]) if args.test else COS_THETA_DEFAULT
    depth_grid = DEPTH_GRID[::4] if args.test else DEPTH_GRID  # 5 pts in test

    script_dir = os.path.dirname(os.path.abspath(__file__))
    plots_dir  = os.path.join(script_dir, "plots", f"{flux_type}_{flavor}")
    os.makedirs(plots_dir, exist_ok=True)

    print(f"Comparing passing fractions: {kind}")
    print(f"nuVeto hadr={NUVETO_HADR}  pmodel=HillasGaisser2012/H3a")
    print(f"Outputs → {plots_dir}\n")

    hdl = Spline_Evaluator()

    n_e, n_ct, n_d = len(energies), len(cos_thetas), len(depth_grid)
    log_e = np.log10(energies)

    # ── Scan 1: PF vs energy × cos_theta grid ─────────────────────────────────
    pf_spl_e  = np.zeros((n_e, n_ct))
    pf_nuv_e  = np.zeros((n_e, n_ct))

    total = n_e * n_ct
    with tqdm(total=total, desc=f"E×cos_theta scan ({kind})", unit="pt") as pbar:
        for i, E in enumerate(energies):
            for j, ct in enumerate(cos_thetas):
                pf_spl_e[i, j] = spline_pf(hdl, E, ct, kind, flavor)
                pf_nuv_e[i, j] = nuveto_pf(E, ct, kind)
                pbar.set_postfix(E=f"{E:.1e}", ct=f"{ct:.1f}")
                pbar.update(1)

    ratio_e = np.where(pf_nuv_e > 0, pf_spl_e / pf_nuv_e, np.nan)

    # ── Scan 2: depth scan at fixed E and cos_theta ────────────────────────────
    pf_spl_d = np.zeros(n_d)
    pf_nuv_d = np.zeros(n_d)

    with tqdm(total=n_d, desc=f"Depth scan ({kind})", unit="pt") as pbar:
        for k, dep in enumerate(depth_grid):
            pf_spl_d[k] = spline_pf(hdl, DEPTH_SCAN_E_GEV, DEPTH_SCAN_COSZEN,
                                     kind, flavor, depth_m=dep)
            pf_nuv_d[k] = nuveto_pf(DEPTH_SCAN_E_GEV, DEPTH_SCAN_COSZEN,
                                     kind, depth_m=dep)
            pbar.update(1)

    ratio_d = np.where(pf_nuv_d > 0, pf_spl_d / pf_nuv_d, np.nan)

    # ── Table ──────────────────────────────────────────────────────────────────
    table_blocks = [
        f"kind={kind}  hadr={NUVETO_HADR}  depth={DEPTH_M} m (E/cos_theta scans)",
        "",
    ]

    # PF vs energy (one block per cos_theta)
    for j, ct in enumerate(cos_thetas):
        table_blocks.append(
            scan_block(
                f"PF vs log10(E/GeV)  cos_theta={ct:.1f}",
                "log10(E)", np.log10(energies),
                pf_spl_e[:, j], pf_nuv_e[:, j], ratio_e[:, j],
                x_fmt=".1f",
            )
        )
        table_blocks.append("")

    # PF vs cos_theta (one block per energy)
    for i, E in enumerate(energies):
        table_blocks.append(
            scan_block(
                f"PF vs cos_theta  log10(E/GeV)={np.log10(E):.1f}",
                "cos_theta", cos_thetas,
                pf_spl_e[i, :], pf_nuv_e[i, :], ratio_e[i, :],
                x_fmt=".1f",
            )
        )
        table_blocks.append("")

    # Depth scan
    table_blocks.append(
        scan_block(
            f"PF vs depth  E={DEPTH_SCAN_E_GEV:.0e} GeV  "
            f"cos_theta={DEPTH_SCAN_COSZEN}",
            "depth_m", depth_grid,
            pf_spl_d, pf_nuv_d, ratio_d,
            x_fmt=".0f",
        )
    )

    table_str = "\n".join(table_blocks)
    print("\n" + table_str)

    table_path = os.path.join(plots_dir, "table.txt")
    with open(table_path, "w") as f:
        f.write(table_str + "\n")
    print(f"\nSaved: {table_path}")

    # ── Plots ──────────────────────────────────────────────────────────────────
    colors_ct = plt.cm.viridis(np.linspace(0, 1, n_ct))
    colors_e  = plt.cm.plasma(np.linspace(0, 1, n_e))

    # 1. PF vs log10(E) --------------------------------------------------------
    fig, (ax_s, ax_n) = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    fig.suptitle(f"PF vs energy — {kind}  |  depth={DEPTH_M} m")
    for j, ct in enumerate(cos_thetas):
        lbl = f"cos θ={ct:.1f}"
        ax_s.plot(log_e, pf_spl_e[:, j], "o-", color=colors_ct[j], label=lbl)
        ax_n.plot(log_e, pf_nuv_e[:, j], "o-", color=colors_ct[j], label=lbl)
    for ax, title in [(ax_s, "Spline"), (ax_n, "nuVeto")]:
        ax.set_xlabel(r"$\log_{10}(E_\nu\,/\,\mathrm{GeV})$")
        ax.set_ylabel("passing fraction")
        ax.set_title(title)
        ax.legend(fontsize=7, ncol=2)
        ax.set_ylim(0, 1.05)
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(os.path.join(plots_dir, "pf_vs_energy.pdf"), bbox_inches="tight")
    plt.close(fig)

    # 2. PF vs cos_theta -------------------------------------------------------
    fig, (ax_s, ax_n) = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    fig.suptitle(f"PF vs cos θ — {kind}  |  depth={DEPTH_M} m")
    for i, E in enumerate(energies):
        lbl = f"log₁₀E={log_e[i]:.1f}"
        ax_s.plot(cos_thetas, pf_spl_e[i, :], "o-", color=colors_e[i], label=lbl)
        ax_n.plot(cos_thetas, pf_nuv_e[i, :], "o-", color=colors_e[i], label=lbl)
    for ax, title in [(ax_s, "Spline"), (ax_n, "nuVeto")]:
        ax.set_xlabel(r"$\cos\theta$")
        ax.set_ylabel("passing fraction")
        ax.set_title(title)
        ax.legend(fontsize=7, ncol=2)
        ax.set_ylim(0, 1.05)
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(os.path.join(plots_dir, "pf_vs_coszen.pdf"), bbox_inches="tight")
    plt.close(fig)

    # 3. Ratio vs log10(E) -----------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.suptitle(f"Ratio spline/nuVeto vs energy — {kind}  |  depth={DEPTH_M} m")
    for j, ct in enumerate(cos_thetas):
        ax.plot(log_e, ratio_e[:, j], "o-", color=colors_ct[j],
                label=f"cos θ={ct:.1f}")
    ax.axhline(1.0, color="k", linestyle="--", linewidth=0.8)
    ax.set_xlabel(r"$\log_{10}(E_\nu\,/\,\mathrm{GeV})$")
    ax.set_ylabel("spline / nuVeto")
    ax.set_ylim(0, 2)
    ax.legend(fontsize=7, ncol=2)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(os.path.join(plots_dir, "ratio_vs_energy.pdf"), bbox_inches="tight")
    plt.close(fig)

    # 4. Ratio vs cos_theta ----------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.suptitle(f"Ratio spline/nuVeto vs cos θ — {kind}  |  depth={DEPTH_M} m")
    for i, E in enumerate(energies):
        ax.plot(cos_thetas, ratio_e[i, :], "o-", color=colors_e[i],
                label=f"log₁₀E={log_e[i]:.1f}")
    ax.axhline(1.0, color="k", linestyle="--", linewidth=0.8)
    ax.set_xlabel(r"$\cos\theta$")
    ax.set_ylabel("spline / nuVeto")
    ax.set_ylim(0, 2)
    ax.legend(fontsize=7, ncol=2)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(os.path.join(plots_dir, "ratio_vs_coszen.pdf"), bbox_inches="tight")
    plt.close(fig)

    # 5. Depth scan ------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f"Depth scan — {kind}\n"
                 f"E={DEPTH_SCAN_E_GEV:.0e} GeV  cos θ={DEPTH_SCAN_COSZEN}")

    ax_pf    = axes[0, 0]
    ax_ratio = axes[0, 1]
    ax_spl   = axes[1, 0]
    ax_nuv   = axes[1, 1]

    ax_pf.plot(depth_grid, pf_spl_d, "o-", label="Spline", color="C0")
    ax_pf.plot(depth_grid, pf_nuv_d, "s-", label="nuVeto", color="C1")
    ax_pf.set_xlabel("depth (m)")
    ax_pf.set_ylabel("passing fraction")
    ax_pf.set_title("Spline vs nuVeto")
    ax_pf.legend()
    ax_pf.grid(True, alpha=0.3)

    ax_ratio.plot(depth_grid, ratio_d, "o-", color="C2")
    ax_ratio.axhline(1.0, color="k", linestyle="--", linewidth=0.8)
    ax_ratio.set_xlabel("depth (m)")
    ax_ratio.set_ylabel("spline / nuVeto")
    ax_ratio.set_ylim(0, 2)
    ax_ratio.set_title("Ratio")
    ax_ratio.grid(True, alpha=0.3)

    ax_spl.plot(depth_grid, pf_spl_d, "o-", color="C0")
    ax_spl.set_xlabel("depth (m)")
    ax_spl.set_ylabel("passing fraction")
    ax_spl.set_title("Spline")
    ax_spl.grid(True, alpha=0.3)

    ax_nuv.plot(depth_grid, pf_nuv_d, "s-", color="C1")
    ax_nuv.set_xlabel("depth (m)")
    ax_nuv.set_ylabel("passing fraction")
    ax_nuv.set_title("nuVeto")
    ax_nuv.grid(True, alpha=0.3)

    plt.tight_layout()
    fig.savefig(os.path.join(plots_dir, "pf_vs_depth.pdf"), bbox_inches="tight")
    plt.close(fig)

    # 6. 2-D ratio heatmap (E × cos_theta) ------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.pcolormesh(cos_thetas, log_e, ratio_e,
                       cmap="RdBu_r", vmin=0.5, vmax=1.5)
    fig.colorbar(im, ax=ax, label="spline / nuVeto")
    ax.set_xlabel(r"$\cos\theta$")
    ax.set_ylabel(r"$\log_{10}(E_\nu\,/\,\mathrm{GeV})$")
    ax.set_title(f"Ratio 2D — {kind}  |  depth={DEPTH_M} m")
    plt.tight_layout()
    fig.savefig(os.path.join(plots_dir, "ratio_2d.pdf"), bbox_inches="tight")
    plt.close(fig)

    print(f"\nAll outputs written to {plots_dir}/")


if __name__ == "__main__":
    main()
