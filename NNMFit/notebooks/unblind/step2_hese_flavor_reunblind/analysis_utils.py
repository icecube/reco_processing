"""Shared helpers for the step2_hese_flavor_reunblind notebooks (and their studies).

Import with
    sys.path.insert(0, "/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/unblind/step2_hese_flavor_reunblind")
    from analysis_utils import ...

1D scans:
  get_1sigma          : 1 sigma errors from a profile likelihood scan
  scan_errors         : best fit and 1 sigma errors of all parameters of a scan
  CombinedScan        : 1D scans of several scan directories merged per parameter
2D scans:
  combine_2d_scans    : merge several 2D scans on a grid, lowest dllh per point
  load_hese75_2d      : HESE-7.5 (gamma, phi0) scan
Previous results:
  PREVIOUS_RESULTS    : HESE-7.5, HESE-7.5 flavor, HESE-12 flavor best fits
Flavor triangle:
  load_triangle_scan  : ScanHandler + contour points of one flavor scan
  combine_scans       : merge several flavor scans, lowest TS per scan point
  flavor_fractions    : flavor composition at Earth from astro_nue_ratio / astro_nutau_ratio
LaTeX tables:
  PARAMETERS, PARAM_LABELS, GROUP_LABELS, fmt_entry, latex_comparison_table
"""
import sys

import numpy as np
import pandas as pd

from NNMFit.utilities import ScanHandler

sys.path.append("/data/user/tvaneede/utils")
from FlavourScansPlotting import grided_TS_nutau_nue


# ---------------------------------------------------------------------------
# 1D scans
# ---------------------------------------------------------------------------

def get_1sigma(scan, parameter, bestfit_val, threshold=1.0):
    """Find where dllh crosses threshold via sign-change detection + linear interpolation."""
    scan_sorted = scan.sort_values(parameter).reset_index(drop=True)
    x = scan_sorted[parameter].values
    delta = scan_sorted["dllh"].values - threshold

    sign_changes = np.where(np.diff(np.sign(delta)))[0]
    roots = []
    for idx in sign_changes:
        x0, x1 = x[idx], x[idx + 1]
        y0, y1 = delta[idx], delta[idx + 1]
        roots.append(x0 - y0 * (x1 - x0) / (y1 - y0))

    roots = np.array(roots)
    lower = roots[roots < bestfit_val]
    upper = roots[roots > bestfit_val]

    err_lo = bestfit_val - lower[-1] if len(lower) else np.nan
    err_hi = upper[0] - bestfit_val if len(upper) else np.nan
    return err_lo, err_hi


def scan_errors(scan, bestfit, parameters, drop_unsuccessful):
    """{parameter: (bestfit, err_lo, err_hi)} for all parameters that are scanned in `scan`
    (ScanHandler or CombinedScan); parameters without a scan are skipped."""
    errors = {}
    for parameter in parameters:
        try:
            df = scan.get_scan_df(param_name=parameter, drop_unsuccessful=drop_unsuccessful)
        except Exception:
            continue
        errors[parameter] = (bestfit[parameter], *get_1sigma(df, parameter, bestfit[parameter]))
    return errors


class CombinedScan:
    """1D scans of several scan directories with the same likelihood, merged per parameter.
    dllh is computed relative to the lowest freefit llh of all scans; for scan points at the
    same parameter value the lowest llh is kept."""

    def __init__(self, scans, bestfits):
        self.scans = scans
        self.bestfit = min(bestfits.values(), key=lambda bf: bf["llh"])
        self.llh_min = self.bestfit["llh"]

    def get_scan_df(self, param_name, drop_unsuccessful=None):
        dfs = []
        for name, scan in self.scans.items():
            try:
                df = scan.get_scan_df(param_name=param_name, dllh_ref=self.llh_min, drop_unsuccessful=drop_unsuccessful)
            except Exception:
                continue
            if len(df):
                dfs.append(df.assign(scan=name))
        if not dfs:
            raise KeyError(f"{param_name} is not scanned in any of {list(self.scans)}")
        df = pd.concat(dfs, ignore_index=True)
        df["_x"] = df[param_name].astype(float).round(10)
        df = df.sort_values("llh").drop_duplicates("_x").drop(columns="_x")
        return df.sort_values(param_name).reset_index(drop=True)


# ---------------------------------------------------------------------------
# 2D scans
# ---------------------------------------------------------------------------

def combine_2d_scans(xs, ys, dllhs):
    """Combine multiple 2D scans by keeping the lowest dllh at each grid point.

    If all scans share the same grid, the minimum is taken directly (fast path).
    Otherwise every scan is interpolated onto a common grid first (intersection
    of all scan ranges, resolution of the finest scan).
    (combine_scans of step1_hese_flux_reunblind/fit_result_2D.ipynb)
    """
    from scipy.interpolate import RegularGridInterpolator

    xs    = [np.asarray(xi) for xi in xs]
    ys    = [np.asarray(yi) for yi in ys]
    dllhs = [np.asarray(di) for di in dllhs]

    # extract 1-D coordinate vectors from either 1-D or 2-D (meshgrid) arrays
    def _x1d(arr): return arr[0, :] if arr.ndim == 2 else arr
    def _y1d(arr): return arr[:, 0] if arr.ndim == 2 else arr

    x1ds = [_x1d(xi) for xi in xs]
    y1ds = [_y1d(yi) for yi in ys]

    # fast path: all grids are identical
    same_grid = all(
        np.array_equal(x1ds[0], x1d) and np.array_equal(y1ds[0], y1d)
        for x1d, y1d in zip(x1ds[1:], y1ds[1:])
    )
    if same_grid:
        return xs[0], ys[0], np.fmin.reduce(dllhs)  # fmin: ignore NaN of failed points

    # slow path: interpolate onto intersection of scan ranges
    x_common = np.linspace(max(x1d.min() for x1d in x1ds), min(x1d.max() for x1d in x1ds), max(len(x1d) for x1d in x1ds))
    y_common = np.linspace(max(y1d.min() for y1d in y1ds), min(y1d.max() for y1d in y1ds), max(len(y1d) for y1d in y1ds))
    xmesh, ymesh = np.meshgrid(x_common, y_common)
    pts = np.stack([ymesh.ravel(), xmesh.ravel()], axis=1)  # (N, 2) in (y, x) order

    dllhs_interp = []
    for x1d, y1d, dllh in zip(x1ds, y1ds, dllhs):
        interp = RegularGridInterpolator((y1d, x1d), dllh, method="linear", bounds_error=False, fill_value=np.inf)
        dllhs_interp.append(interp(pts).reshape(xmesh.shape))

    return xmesh, ymesh, np.fmin.reduce(dllhs_interp)


def load_hese75_2d():
    """HESE-7.5 (gamma, phi0 per flavor) likelihood scan.
    Returns (gamma_grid, norm_grid, dllh_grid, levels for 1 and 2 sigma (2 dof), (gamma_bf, norm_bf))."""
    import scipy.special

    params_llhs = np.loadtxt("/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/unblind/debug_bdt/astro_scan_data_hese7.5.txt")
    bf_gamma, bf_norm, bf_llh = 2.87375956, 6.36488608 / 3, 122.95919881139868  # [gamma, phi0, -LLH]

    gamma, norm, llhs = params_llhs[:, 0], params_llhs[:, 1] / 3, params_llhs[:, 2]
    proportions = scipy.special.erf(np.array([1, 2]) / np.sqrt(2.0))
    levels = scipy.special.gammaincinv(2 / 2.0, proportions)

    ng, nn = len(np.unique(gamma)), len(np.unique(norm))
    return (gamma.reshape(ng, nn), norm.reshape(ng, nn), (llhs - bf_llh).reshape(ng, nn), levels, (bf_gamma, bf_norm))


# ---------------------------------------------------------------------------
# Previous results: (best_fit, err_lo, err_hi); err None = no error available,
# parameter missing = not in that analysis
# ---------------------------------------------------------------------------

# HESE-7.5, single power law without flavor fit: values given as (bf, CL_lo, CL_hi)
HESE75_RESULTS = {
    "astro_norm":   (6.37/3,  6.37/3 - 4.75/3,  7.83/3 - 6.37/3),
    "gamma_astro":  (2.87,    2.87 - 2.68,       3.08 - 2.87),
    "conv_norm":    (1.01,    1.01 - 0.67,        1.35 - 1.01),
    "prompt_norm":  (0.0,     0.0,                5.34 - 0.0),
    "combined_muongun_norm": (1.19,    1.19 - 0.75,        1.64 - 1.19),
    "delta_gamma":  (-0.053,  -0.053 - (-0.184),  -0.005 - (-0.053)),
    "dom_eff":      (0.952,   0.952 - 0.886,      1.045 - 0.952),
}

# HESE-7.5 flavor: Phi_astro = 6.98 (all flavors), nu_e : nu_mu : nu_tau = 0.29 : 0.43 : 0.28.
# With Phi_astro = astro_norm * (1 + astro_nue_ratio + astro_nutau_ratio):
#   astro_norm = f_mu * Phi_astro, astro_nue_ratio = f_e / f_mu, astro_nutau_ratio = f_tau / f_mu
_hese75_phi_astro = 6.98
_hese75_f_e, _hese75_f_mu, _hese75_f_tau = 0.29, 0.43, 0.28
HESE75_FLAVOR_RESULTS = {
    "astro_norm":        (_hese75_f_mu * _hese75_phi_astro, None, None),
    "astro_nue_ratio":   (_hese75_f_e / _hese75_f_mu,       None, None),
    "astro_nutau_ratio": (_hese75_f_tau / _hese75_f_mu,     None, None),
    "gamma_astro":       (2.89, 0.20, 0.21),
    "conv_norm":         (0.97, 0.36, 0.36),
    "prompt_norm":       (0.0,  0.0,  6.1),
    "combined_muongun_norm": (1.16, 0.45, 0.46),
}

# HESE-12 flavor
HESE12_RESULTS = {
    "astro_norm":   (2.53,    1.49,   1.78),
    "gamma_astro":  (2.84,    0.18,   0.19),
    "astro_nue_ratio":   (0.45,  0.40, 0.68),
    "astro_nutau_ratio": (0.896, 0.89, 1.34),
    "conv_norm":    (0.99,    0.20,   0.19),
    "prompt_norm":  (0.0,     0.0,    2.25),
    "combined_muongun_norm": (1.16,    0.43,   0.42),
    "delta_gamma":  (-0.00,   1.0,    1.0),
    "CR_grad":      (0.042,   1.0,    2.0),
    "barr_h":       (0.0,     0.5,    0.5),
    "barr_w":       (0.0,     0.5,    0.5),
    "barr_y":       (0.0,     0.5,    0.5),
    "barr_z":       (0.0,     0.5,    0.5),
    "dom_eff":      (1.04,    0.04,   0.06),
    "ice_scat":     (0.98,    0.04,   0.04),
    "ice_abs":      (0.99,    0.04,   0.04),
    "ice_holep0":   (-0.27,   0.38,   0.28),
    "ice_holep1":   (-0.08,   0.05,   0.04),
}

PREVIOUS_RESULTS = {
    "HESE-7.5":        HESE75_RESULTS,
    "HESE-7.5 flavor": HESE75_FLAVOR_RESULTS,
    "HESE-12 flavor":  HESE12_RESULTS,
}


# ---------------------------------------------------------------------------
# Flavor triangle
# ---------------------------------------------------------------------------

def load_triangle_scan(scan_dir, N_grid=40, drop_unsuccessful=False, drop_unsuccessful_points=True):
    """Load one flavor scan. Returns (scan_handler, data, bestfit), with data holding
    ftau/fe/ts (used scan points), ftau_grid/fe_grid/ts_grid (interpolated) and
    n_converged / n_points (scan points with fit_success / all scan points).

    Same as FlavourScansPlotting.get_contour_points, but the dropping of failed scan fits is
    configurable: get_contour_points always calls get_scan_xydllh(drop_unsuccessful=True), so the
    drop_unsuccessful of the ScanHandler has no effect there. With NNMFit v0.3.0 this did not matter
    (result_handlers.py hardcodes success = 1), from v0.5.0 on the real minimizer flag is used and
    failed fits (e.g. ABNORMAL_TERMINATION_IN_LNSRCH) are removed. drop_unsuccessful_points=True
    reproduces get_contour_points.
    """
    scan = ScanHandler(scan_dir, dump=False, drop_unsuccessful=drop_unsuccessful)
    xydllh = lambda drop: scan.get_scan_xydllh(x="astro_nue_ratio", y="astro_nutau_ratio", drop_unsuccessful=drop)
    nue, nutau, ts = xydllh(drop_unsuccessful_points)

    norm = nue + 1 + nutau
    fe, ftau = nue / norm, nutau / norm
    ftau_grid, fe_grid, ts_grid = grided_TS_nutau_nue(ftau, fe, ts, interp_method="linear", N_grid=N_grid)

    data = {"ftau": ftau, "fe": fe, "ts": ts, "ftau_grid": ftau_grid, "fe_grid": fe_grid, "ts_grid": ts_grid,
            "n_converged": len(xydllh(True)[2]), "n_points": len(xydllh(False)[2])}
    return scan, data, scan.get_freefit()


def combine_scans(names, data, bestfits, N_grid):
    """Combine scans: take lowest dllh at each scan point, renormalized to the global best fit.

    dllh convention: 2*(scan_llh - freefit_llh), renormalize by 2*(freefit_llh_s - global_best_llh).
    Scans may have different numbers of points (dropped unsuccessful fits), so merge by coordinates.
    Returns (combined data, bestfit of the scan with the lowest freefit llh).
    """
    global_best_name = min(names, key=lambda n: bestfits[n]["llh"])
    global_best_llh = bestfits[global_best_name]["llh"]

    dfs = []
    for name in names:
        shift = 2 * (bestfits[name]["llh"] - global_best_llh)
        dfs.append(pd.DataFrame({
            "ftau": data[name]["ftau"],
            "fe":   data[name]["fe"],
            "ts":   data[name]["ts"] + shift,
        }))

    combined_df = pd.concat(dfs).groupby(["ftau", "fe"], as_index=False)["ts"].min()
    combined_ftau = combined_df["ftau"].values
    combined_fe   = combined_df["fe"].values
    combined_ts   = combined_df["ts"].values

    ftau_grid, fe_grid, ts_grid = grided_TS_nutau_nue(
        combined_ftau, combined_fe, combined_ts, interp_method='linear', N_grid=N_grid
    )

    print(f"Global best fit from: {global_best_name} (llh={global_best_llh:.4f})")
    print(f"Combined scan points: {len(combined_ts)}")
    combined = {
        "ftau":      combined_ftau,
        "fe":        combined_fe,
        "ts":        combined_ts,
        "ftau_grid": ftau_grid,
        "fe_grid":   fe_grid,
        "ts_grid":   ts_grid,
    }
    return combined, bestfits[global_best_name]


def flavor_fractions(params):
    """Flavor composition at Earth (f_e, f_mu, f_tau) from astro_nue_ratio and astro_nutau_ratio."""
    norm = 1 + params["astro_nue_ratio"] + params["astro_nutau_ratio"]
    return {"f_e": params["astro_nue_ratio"] / norm, "f_mu": 1 / norm, "f_tau": params["astro_nutau_ratio"] / norm}


# ---------------------------------------------------------------------------
# LaTeX tables
# ---------------------------------------------------------------------------

# step2 fit parameters in table order
PARAMETERS = [
    "astro_norm", "gamma_astro", "astro_nue_ratio", "astro_nutau_ratio",
    "conv_norm", "prompt_norm", "combined_muongun_norm", "muongun_asymmetry",
    "delta_gamma", "CR_grad", "barr_h", "barr_w", "barr_y", "barr_z",
    "dom_eff", "ice_scat", "ice_abs", "ice_crystal", "ice_holep0", "ice_holep1",
]

PARAM_LABELS = {
    "astro_norm":    r"$\Phi_{0,\nu_\mu}$",
    "gamma_astro":   r"$\gamma_\mathrm{astro}$",
    "conv_norm":     r"$\Phi_\mathrm{conv}$",
    "prompt_norm":   r"$\Phi_\mathrm{prompt}$",
    "astro_nue_ratio":   r"$\Phi_{\nu_e}/\Phi_{\nu_\mu}$",
    "astro_nutau_ratio": r"$\Phi_{\nu_\tau}/\Phi_{\nu_\mu}$",
    "combined_muongun_norm": r"$\Phi_\mathrm{muon}$",
    "muongun_asymmetry":     r"$a_\mathrm{muon}$",
    "delta_gamma":   r"$\Delta\gamma_{\rm CR}$",
    "CR_grad":       r"CR grad",
    "barr_h":        r"Barr $h$",
    "barr_w":        r"Barr $w$",
    "barr_y":        r"Barr $y$",
    "barr_z":        r"Barr $z$",
    "dom_eff":       r"DOM eff.",
    "ice_scat":      r"Ice scattering",
    "ice_abs":       r"Ice absorption",
    "ice_crystal":   r"Ice crystal",
    "ice_holep0":    r"Ice hole $p_0$",
    "ice_holep1":    r"Ice hole $p_1$",
    "f_e":           r"$f_{\nu_e}$",
    "f_mu":          r"$f_{\nu_\mu}$",
    "f_tau":         r"$f_{\nu_\tau}$",
}

# first parameter of each group in the table
GROUP_LABELS = {
    "astro_norm": "Signal",
    "conv_norm":  "Flux nuisance",
    "dom_eff":    "Detector nuisance",
}


def _missing(v):
    return v is None or np.isnan(v)


def fmt_entry(entry, n_decimals=3):
    """(bf, err_lo, err_hi) -> $bf^{+hi}_{-lo}$; missing errors as ---, entry None as ---."""
    if entry is None:
        return "---"
    bf, lo, hi = entry
    if _missing(lo) and _missing(hi):
        return f"${bf:.{n_decimals}f}$"
    hi_str = "---" if _missing(hi) else f"+{hi:.{n_decimals}f}"
    lo_str = "---" if _missing(lo) else f"-{lo:.{n_decimals}f}"
    return f"${bf:.{n_decimals}f}^{{{hi_str}}}_{{{lo_str}}}$"


def latex_comparison_table(columns, caption, label, parameters=PARAMETERS, n_decimals=3):
    """LaTeX table with one column per entry of `columns` = {column name: {parameter: (bf, err_lo, err_hi)}}."""
    n_cols = len(columns) + 1
    lines = [
        r"\begin{table}[h]",
        r"  \centering",
        f"  \\caption{{{caption}}}",
        f"  \\label{{{label}}}",
        r"  \begin{tabular}{l " + " ".join("r" for _ in columns) + "}",
        r"    \hline\hline",
        "    Parameter & " + " & ".join(columns) + r" \\",
        r"    \hline",
    ]
    for p in parameters:
        if p in GROUP_LABELS:
            lines.append(r"    \hline")
            lines.append(f"    \\multicolumn{{{n_cols}}}{{l}}{{\\textbf{{{GROUP_LABELS[p]}}}}} \\\\")
            lines.append(r"    \hline")
        entries = [fmt_entry(results.get(p), n_decimals) for results in columns.values()]
        lines.append(f"    {PARAM_LABELS.get(p, p)} & " + " & ".join(entries) + r" \\")
    lines += [
        r"    \hline\hline",
        r"  \end{tabular}",
        r"\end{table}",
    ]
    return "\n".join(lines)
