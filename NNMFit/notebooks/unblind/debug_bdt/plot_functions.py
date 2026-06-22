"""Plotting functions for reco-space BDT diagnostic plots."""
import os
import glob

import numpy as np
import matplotlib.pyplot as plt

from unifigs.figures import RatioPlot
from NNMFit.utilities import load_pickle

from plot_configs import COMPONENT_COLORS, COMPONENTS


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_histograms(step0_path, plots):
    """Load MC, data, and component histograms for every scan referenced in `plots`.

    Returns a dict  {scan_name: {"data": ..., "mc": ..., "Astro": ..., ...}}.
    Missing component files are silently skipped.
    """
    scan_names = list(dict.fromkeys(
        scan_name for plot in plots for scan_name, _ in plot["scans"]
    ))
    collection = {}
    for scan_name in scan_names:
        print(scan_name)
        collection[scan_name] = {}

        data_paths = glob.glob(os.path.join(step0_path, scan_name, "Data_Histogram.pickle"))
        if len(data_paths) != 1:
            raise FileNotFoundError(
                f"Expected one Data_Histogram.pickle for '{scan_name}', found {len(data_paths)} "
                f"in {step0_path}"
            )
        collection[scan_name]["data"] = load_pickle(data_paths[0])

        mc_paths = glob.glob(os.path.join(step0_path, scan_name, "MC_Histogram.pickle"))
        if not mc_paths:
            raise FileNotFoundError(
                f"No MC_Histogram.pickle found for '{scan_name}' in {step0_path}"
            )
        collection[scan_name]["mc"] = load_pickle(mc_paths[0])

        for component in COMPONENTS:
            comp_paths = glob.glob(
                os.path.join(step0_path, scan_name, f"MC_Histogram_{component}.pickle")
            )
            if comp_paths:
                collection[scan_name][component] = load_pickle(comp_paths[0])

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

def _render_plot(plot_cfg, histogram_collection, save_path, show=True, show_chi2=False):
    """Render and save one figure described by `plot_cfg`."""
    det_config      = plot_cfg["det_config"]
    scans           = plot_cfg["scans"]
    binning         = plot_cfg["binning"]
    dims            = plot_cfg["dim_info"]
    plot_data       = plot_cfg.get("plot_data", True)
    show_counts     = plot_cfg.get("show_counts", False)
    plot_components = plot_cfg.get("plot_components", False)

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
                           draw_style="stairs", label=mc_label, color=color_cycle[i])
            if plot_data:
                plot_ratio(axes[1][col], hcoll["mc"], hcoll["data"],
                           det_config, dim, binning, dims,
                           label=mc_label, color=color_cycle[i])

        # component overlays
        if plot_components:
            for component, comp_color in COMPONENT_COLORS.items():
                if component not in hcoll:
                    continue
                if component == "Muon" and ("Double" in det_config or "Cascade" in det_config or "Combined" in det_config):
                    continue
                n_comp = np.sum(hcoll[component]["histograms"][det_config])
                comp_label = f"{component} ({n_comp:.1f})" if show_counts else component
                for col, dim in enumerate(dims):
                    plot_histogram(axes[0][col], hcoll[component], det_config, dim,
                                   binning, dims, draw_style="stairs",
                                   label=comp_label, color=comp_color)

    # chi-squared annotations
    if show_chi2 and plot_data:
        for col, dim in enumerate(dims):
            lines = []
            for scan_name, label in scans:
                chi2, ndf = compute_chi2(
                    histogram_collection[scan_name]["mc"],
                    histogram_collection[scans[0][0]]["data"],
                    det_config, binning, dims, dim,
                )
                lines.append(f"{label}: $\\chi^2$/ndf = {chi2:.1f}/{ndf}")
            axes[0][col].text(
                0.03, 0.97, "\n".join(lines),
                transform=axes[0][col].transAxes,
                fontsize=6, va="top", ha="left",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7),
            )

    # axis formatting
    axes[0][-1].legend(loc="upper right", fontsize=7, ncol=2,
                       handlelength=1.2, handletextpad=0.2, columnspacing=0.8)
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

    subfolder = os.path.join(save_path, scans[0][0])
    os.makedirs(subfolder, exist_ok=True)
    plt.savefig(os.path.join(subfolder, f"{det_config}.png"), bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


def make_all_plots(plots, histogram_collection, save_path, show=True, show_chi2=False):
    """Render every figure in `plots`, saving PNGs under `save_path`."""
    for plot in plots:
        _render_plot(plot, histogram_collection, save_path, show=show, show_chi2=show_chi2)
