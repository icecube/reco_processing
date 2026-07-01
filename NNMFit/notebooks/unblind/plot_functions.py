"""Plotting functions for reco-space BDT diagnostic plots."""
import os
import glob

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kstwobign

from unifigs.figures import RatioPlot
from NNMFit.utilities import load_pickle

COMPONENT_COLORS = {"Astro": "tab:red", "Conv": "tab:green", "Muon": "tab:orange"}
COMPONENTS = ["Astro", "Conv", "Muon"]

FLAVOR_COMPONENTS = ["Astro_NuE", "Astro_NuMu", "Astro_NuTau"]
FLAVOR_COMPONENT_COLORS = {
    "Astro_NuE":   "#E69F00",   # amber
    "Astro_NuMu":  "#56B4E9",   # sky blue
    "Astro_NuTau": "#CC79A7",   # pink/mauve
}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def _apply_gradient_to_components(hcoll):
    """Distribute the per-bin Snowstorm gradient among non-Muon components.

    Computes the gradient per bin and det_config as (total_syst - total_nosyst),
    then adds each non-Muon component's weighted share:
        adjusted[comp][bin] = nosyst[comp][bin]
                              + gradient[bin] * nosyst[comp][bin] / total_non_muon_nosyst[bin]

    Muon bins are taken directly from the nosyst histogram (unaffected by the gradient).

    If flavor components (Astro_NuE/NuMu/NuTau) are present in hcoll, the Astro gradient
    share is further redistributed among them weighted by their nosyst rates, so that
    NuE + NuMu + NuTau (corrected) == Astro (corrected) in every bin.

    Results are stored in hcoll[comp] so the rest of the plotting code is unchanged.
    Requires hcoll to contain "mc", "mc_nosyst", and at least one "{comp}_nosyst" key.
    """
    if "mc_nosyst" not in hcoll:
        return

    det_configs = list(hcoll["mc"]["histograms"].keys())
    non_muon = [c for c in COMPONENTS if c != "Muon"]

    for det_config in det_configs:
        total_syst   = hcoll["mc"]["histograms"][det_config]
        total_nosyst = hcoll["mc_nosyst"]["histograms"][det_config]
        gradient     = total_syst - total_nosyst

        nosyst_bins = {
            comp: hcoll[f"{comp}_nosyst"]["histograms"][det_config]
            for comp in non_muon
            if f"{comp}_nosyst" in hcoll and det_config in hcoll[f"{comp}_nosyst"]["histograms"]
        }
        if not nosyst_bins:
            continue

        total_non_muon = sum(nosyst_bins.values())

        for comp, bins in nosyst_bins.items():
            weight = np.where(total_non_muon > 0, bins / total_non_muon, 0.0)
            adjusted = bins + gradient * weight
            if comp not in hcoll:
                hcoll[comp] = {**hcoll[f"{comp}_nosyst"], "histograms": dict(hcoll[f"{comp}_nosyst"]["histograms"])}
            hcoll[comp]["histograms"][det_config] = adjusted

        if "Muon_nosyst" in hcoll and det_config in hcoll["Muon_nosyst"]["histograms"]:
            if "Muon" not in hcoll:
                hcoll["Muon"] = {**hcoll["Muon_nosyst"], "histograms": dict(hcoll["Muon_nosyst"]["histograms"])}
            hcoll["Muon"]["histograms"][det_config] = hcoll["Muon_nosyst"]["histograms"][det_config]

        # Redistribute the Astro gradient share among flavor components if they are present.
        # The Astro-gradient share per bin is (Astro_corrected - Astro_nosyst); each flavor
        # receives a fraction of that proportional to its nosyst rate.
        flavor_comps = [c for c in FLAVOR_COMPONENTS if c in hcoll]
        if not flavor_comps or "Astro_nosyst" not in hcoll:
            continue

        astro_nosyst    = hcoll["Astro_nosyst"]["histograms"][det_config]
        astro_corrected = hcoll["Astro"]["histograms"][det_config]
        astro_gradient  = astro_corrected - astro_nosyst

        flavor_nosyst_bins = {c: hcoll[c]["histograms"][det_config] for c in flavor_comps}
        total_flavor_nosyst = sum(flavor_nosyst_bins.values())

        for comp, bins in flavor_nosyst_bins.items():
            weight   = np.where(total_flavor_nosyst > 0, bins / total_flavor_nosyst, 0.0)
            hcoll[comp] = {**hcoll[comp], "histograms": dict(hcoll[comp]["histograms"])}
            hcoll[comp]["histograms"][det_config] = bins + astro_gradient * weight


def load_histograms(step0_path, plots):
    """Load MC, data, and component histograms for every scan referenced in `plots`.

    Returns a dict  {scan_name: {"data": ..., "mc": ..., "Astro": ..., ...}}.
    When nosyst files are present, component histograms are gradient-adjusted:
    the per-bin Snowstorm shift (total_syst - total_nosyst) is distributed among
    non-Muon components weighted by their nosyst rate. Muon is unaffected.
    Missing component files are silently skipped.
    """
    scan_names = list(dict.fromkeys(
        scan_name for plot in plots for scan_name, _ in plot["scans"]
    ))
    collection = {}
    for scan_name in scan_names:
        print(scan_name)
        hcoll = {}

        data_paths = glob.glob(os.path.join(step0_path, scan_name, "Data_Histogram.pickle"))
        if len(data_paths) != 1:
            raise FileNotFoundError(
                f"Expected one Data_Histogram.pickle for '{scan_name}', found {len(data_paths)} "
                f"in {step0_path}"
            )
        hcoll["data"] = load_pickle(data_paths[0])

        mc_paths = glob.glob(os.path.join(step0_path, scan_name, "MC_Histogram.pickle"))
        if not mc_paths:
            raise FileNotFoundError(
                f"No MC_Histogram.pickle found for '{scan_name}' in {step0_path}"
            )
        hcoll["mc"] = load_pickle(mc_paths[0])

        nosyst_path = os.path.join(step0_path, scan_name, "MC_Histogram_nosyst.pickle")
        if os.path.exists(nosyst_path):
            hcoll["mc_nosyst"] = load_pickle(nosyst_path)

        for component in COMPONENTS:
            nosyst_comp_path = os.path.join(step0_path, scan_name, f"MC_Histogram_{component}_nosyst.pickle")
            if os.path.exists(nosyst_comp_path):
                hcoll[f"{component}_nosyst"] = load_pickle(nosyst_comp_path)
            else:
                comp_paths = glob.glob(os.path.join(step0_path, scan_name, f"MC_Histogram_{component}.pickle"))
                if comp_paths:
                    hcoll[component] = load_pickle(comp_paths[0])

        for component in FLAVOR_COMPONENTS:
            nosyst_comp_path = os.path.join(step0_path, scan_name, f"MC_Histogram_{component}_nosyst.pickle")
            if os.path.exists(nosyst_comp_path):
                hcoll[component] = load_pickle(nosyst_comp_path)

        _apply_gradient_to_components(hcoll)
        collection[scan_name] = hcoll

    return collection


# ---------------------------------------------------------------------------
# Low-level histogram helpers
# ---------------------------------------------------------------------------

def get_histogram_projection(histogram, binning, dims, projected_dimension, flip=False):
    reshape_shape = tuple(binning[dim].shape[0] - 1 for dim in binning)
    sum_axis = dims[projected_dimension]["sum_axes"]
    h = np.sum(np.reshape(histogram, reshape_shape), axis=sum_axis)
    return np.flip(h, axis=0) if flip else h


def plot_histogram(ax, histogram_dict, det_config, plot_dimension, binning, dims,
                   draw_style="stairs", label="Label", color="black", **kwargs):
    flip = dims[plot_dimension]["flip"]
    h = get_histogram_projection(
        histogram_dict["histograms"][det_config], binning, dims, plot_dimension, flip
    )
    if histogram_dict.get("fluctuations") is None:
        err = np.sqrt(h)
    else:
        err = get_histogram_projection(
            np.sqrt(histogram_dict["fluctuations"][det_config]), binning, dims, plot_dimension, flip
        )
    if draw_style == "stairs":
        ax.stairs(h, binning[plot_dimension], label=label, color=color, **kwargs)
    elif draw_style == "errors":
        centers = np.diff(binning[plot_dimension]) / 2 + binning[plot_dimension][:-1]
        ax.errorbar(centers, h, yerr=err, fmt=".", label=label, color=color, **kwargs)


def compute_chi2(mc_dict, data_dict, det_config, binning, dims, plot_dimension):
    """Pearson chi-squared with combined data + MC statistical uncertainty.

    Returns (chi2, ndf) where ndf = number of bins with non-zero variance.
    """
    reshape_shape = tuple(binning[dim].shape[0] - 1 for dim in binning)
    sum_axis = dims[plot_dimension]["sum_axes"]
    flip = dims[plot_dimension]["flip"]

    mc_h   = np.sum(np.reshape(mc_dict["histograms"][det_config],   reshape_shape), axis=sum_axis)
    data_h = np.sum(np.reshape(data_dict["histograms"][det_config], reshape_shape), axis=sum_axis)
    if flip:
        mc_h, data_h = np.flip(mc_h), np.flip(data_h)

    if mc_dict.get("fluctuations") is not None:
        mc_ssq = np.sum(np.reshape(mc_dict["fluctuations"][det_config], reshape_shape), axis=sum_axis)
        if flip:
            mc_ssq = np.flip(mc_ssq)
    else:
        mc_ssq = mc_h

    variance = data_h + mc_ssq
    mask = variance > 0
    chi2 = float(np.sum((data_h[mask] - mc_h[mask]) ** 2 / variance[mask]))
    ndf  = int(np.sum(mask))
    return chi2, ndf


def compute_ks(mc_dict, data_dict, det_config, binning, dims, plot_dimension):
    """Two-sample KS test comparing the shape of data and MC distributions.

    Computes CDFs from the normalized (count-independent) histograms, so this
    is purely a shape comparison — normalization differences do not affect D.

    Returns (D, p_value) where D is the KS statistic and p_value uses the
    asymptotic two-sample formula with N_eff = sqrt(n_data * n_mc / (n_data + n_mc)).
    """
    reshape_shape = tuple(binning[dim].shape[0] - 1 for dim in binning)
    sum_axis = dims[plot_dimension]["sum_axes"]
    flip = dims[plot_dimension]["flip"]

    mc_h   = np.sum(np.reshape(mc_dict["histograms"][det_config],   reshape_shape), axis=sum_axis)
    data_h = np.sum(np.reshape(data_dict["histograms"][det_config], reshape_shape), axis=sum_axis)
    if flip:
        mc_h, data_h = np.flip(mc_h), np.flip(data_h)

    n_mc   = float(np.sum(mc_h))
    n_data = float(np.sum(data_h))
    if n_mc == 0 or n_data == 0:
        return float("nan"), float("nan")

    mc_cdf   = np.cumsum(mc_h)   / n_mc
    data_cdf = np.cumsum(data_h) / n_data

    D = float(np.max(np.abs(data_cdf - mc_cdf)))
    n_eff = np.sqrt(n_data * n_mc / (n_data + n_mc))
    p_value = float(kstwobign.sf(D * n_eff))
    return D, p_value


def plot_ratio(ax, mc_dict, data_dict, det_config, plot_dimension, binning, dims,
               include_mc_err=True, label="Ratio", color="black",
               capsize=2, markeredgecolor="black", **kwargs):
    reshape_shape = tuple(binning[dim].shape[0] - 1 for dim in binning)
    sum_axis = dims[plot_dimension]["sum_axes"]
    flip     = dims[plot_dimension]["flip"]

    mc_h   = np.sum(np.reshape(mc_dict["histograms"][det_config],   reshape_shape), axis=sum_axis)
    data_h = np.sum(np.reshape(data_dict["histograms"][det_config], reshape_shape), axis=sum_axis)
    if flip:
        mc_h, data_h = np.flip(mc_h), np.flip(data_h)

    if include_mc_err:
        mc_ssq = np.sum(
            np.reshape(mc_dict["fluctuations"][det_config], reshape_shape), axis=sum_axis
        )
        if flip:
            mc_ssq = np.flip(mc_ssq)
        mc_err = np.sqrt(mc_ssq)
    else:
        mc_err = np.zeros_like(mc_h)

    ratio = data_h / mc_h
    ratio_err = ratio * np.sqrt((np.sqrt(data_h) / data_h)**2 + (mc_err / mc_h)**2)

    centers = np.diff(binning[plot_dimension]) / 2 + binning[plot_dimension][:-1]
    ax.errorbar(
        centers, ratio, yerr=ratio_err, fmt=".",
        label=label, color=color, elinewidth=1, capsize=capsize,
        markeredgecolor=markeredgecolor, **kwargs,
    )


# ---------------------------------------------------------------------------
# High-level plot driver
# ---------------------------------------------------------------------------

def _render_plot(plot_cfg, histogram_collection, save_path, show=True):
    """Render and save one figure described by `plot_cfg`."""
    det_config      = plot_cfg["det_config"]
    scans           = plot_cfg["scans"]
    binning         = plot_cfg["binning"]
    dims            = plot_cfg["dim_info"]
    plot_data       = plot_cfg.get("plot_data", True)
    show_counts     = plot_cfg.get("show_counts", False)
    plot_components = plot_cfg.get("plot_components", False)
    plot_flavor     = plot_cfg.get("plot_flavor", False)
    show_chi2       = plot_cfg.get("show_chi2", False)
    show_ks         = plot_cfg.get("show_ks", False)

    color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    fig, axes = RatioPlot(pad=0.1, vert_pad=0.35).create(ncols=2, dpi=200)

    # data points
    if plot_data:
        n_data = int(np.sum(histogram_collection[scans[0][0]]["data"]["histograms"][det_config]))
        data_label = f"Data ({n_data})" if show_counts else "Data"
        for col, dim in enumerate(dims):
            plot_histogram(
                axes[0][col], histogram_collection[scans[0][0]]["data"],
                det_config, dim, binning, dims,
                draw_style="errors", label=data_label, color="black",
            )

    # MC and ratio per scan
    for i, (scan_name, label) in enumerate(scans):
        hcoll = histogram_collection[scan_name]
        n_mc  = np.sum(hcoll["mc"]["histograms"][det_config])
        mc_label = f"{label} ({n_mc:.1f})" if show_counts else label

        for col, dim in enumerate(dims):
            plot_histogram(axes[0][col], hcoll["mc"], det_config, dim, binning, dims,
                           draw_style="stairs", label=mc_label, color="black")
            if plot_data:
                plot_ratio(axes[1][col], hcoll["mc"], hcoll["data"],
                           det_config, dim, binning, dims,
                           label=mc_label, color="black")

        # component overlays
        if plot_components:
            if plot_flavor:
                components_to_draw = list(FLAVOR_COMPONENT_COLORS.items()) + [
                    ("Conv", COMPONENT_COLORS["Conv"]),
                    ("Muon", COMPONENT_COLORS["Muon"]),
                ]
            else:
                components_to_draw = list(COMPONENT_COLORS.items())
            for component, comp_color in components_to_draw:
                if component not in hcoll:
                    continue
                if component == "Muon" and ("Double" in det_config or "Cascade" in det_config or "Combined" in det_config):
                    continue
                n_comp = np.sum(hcoll[component]["histograms"][det_config])
                display_name = component.replace("_", " ")
                comp_label = f"{display_name} ({n_comp:.1f})" if show_counts else display_name
                for col, dim in enumerate(dims):
                    plot_histogram(axes[0][col], hcoll[component], det_config, dim,
                                   binning, dims, draw_style="stairs",
                                   label=comp_label, color=comp_color)

    # goodness-of-fit annotations (chi2 and/or KS)
    if (show_chi2 or show_ks) and plot_data:
        for col, dim in enumerate(dims):
            lines = []
            for scan_name, label in scans:
                mc_dict   = histogram_collection[scan_name]["mc"]
                data_dict = histogram_collection[scans[0][0]]["data"]
                scan_lines = []
                if show_chi2:
                    chi2, ndf = compute_chi2(mc_dict, data_dict, det_config, binning, dims, dim)
                    scan_lines.append(f"$\\chi^2$/ndf = {chi2:.1f}/{ndf}")
                if show_ks:
                    D, p = compute_ks(mc_dict, data_dict, det_config, binning, dims, dim)
                    scan_lines.append(f"KS D={D:.3f}, p={p:.3f}")
                lines.append(f"{label}: " + ", ".join(scan_lines))
            axes[1][col].text(
                0.03, 1.0, "\n".join(lines),
                transform=axes[1][col].transAxes,
                fontsize=6, va="bottom", ha="left",
                clip_on=False,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7),
            )

    # axis formatting
    axes[0][-1].legend(loc="upper right", fontsize=5, ncol=2,
                       handlelength=1.0, handletextpad=0.2, columnspacing=0.5)
    for col, dim in enumerate(dims):
        info = dims[dim]
        bins = binning[dim]
        if info["log_x"]:
            axes[0][col].set_xscale("log")
            axes[1][col].set_xscale("log")
        if info["log_y"]:
            axes[0][col].set_yscale("log")
        axes[0][col].set_xlim(bins.min(), bins.max())
        axes[1][col].set_xlim(bins.min(), bins.max())
        axes[1][col].set_ylim(0.0, 3.0)
        axes[1][col].set_xlabel(info["x_label"])
        axes[1][col].axhline(1, color="grey", linestyle="--", zorder=-10)
        if ylim := info.get("ylim"):
            axes[0][col].set_ylim(ylim)

    axes[0][0].set_ylabel("Count")
    axes[1][0].set_ylabel("Data / MC")
    fig.suptitle(plot_cfg["title"])

    scan_name = scans[0][0]
    scan_save_path = os.path.join(save_path, scan_name)
    os.makedirs(scan_save_path, exist_ok=True)
    plt.savefig(os.path.join(scan_save_path, f"{plot_cfg['key']}.png"), bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


def make_all_plots(plots, histogram_collection, save_path, show=True):
    """Render every figure in `plots`, saving PNGs under `save_path`."""
    for plot in plots:
        _render_plot(plot, histogram_collection, save_path, show=show)
