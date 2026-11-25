"""Plot configuration for reco_space_bdt_plots.ipynb — step2_hese_flavor_reunblind.

All plot keys use the format:
  name-{scan_name}_channel-{channel}_count-{bool}_data-{bool}[_flavor][_nosyst]
where _flavor plots split the astro component into NuE/NuMu/NuTau and _nosyst plots
show the best fit without the Snowstorm gradient shift.

Import PLOTS and GROUP_* constants from this module.
"""
import numpy as np

# draw the conv/prompt parts of the combined muon template (tracks only),
# can be overridden per plot via the "plot_muon_split" key
PLOT_MUON_SPLIT = True

# ---------------------------------------------------------------------------
# Separate-detector plots (cascades / tracks / dc)
# ---------------------------------------------------------------------------

_CASCADES_SPEC = {
    "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Cascades",
    "binning": {
        "reco_energy": np.geomspace(10**4.778, 10**7.1, 24),
        "reco_zenith": np.linspace(-1, 1, 11),
    },
    "dim_info": {
        "reco_energy": {"log_x": True,  "log_y": True, "x_label": r"$E_{\mathrm{reco}}$ [GeV]",      "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e2)},
        "reco_zenith": {"log_x": False, "log_y": True, "x_label": r"$\cos(\theta_{\mathrm{reco}})$", "sum_axes": 0, "flip": True,  "ylim": (1e-2, 1e2)},
    },
    "plot_components": True,
}

_TRACKS_SPEC = {
    "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Tracks",
    "binning": {
        "reco_energy": np.geomspace(10**4.778, 10**7.1, 24),
        "reco_zenith": np.linspace(-1, 1, 11),
    },
    "dim_info": {
        "reco_energy": {"log_x": True,  "log_y": True, "x_label": r"$E_{\mathrm{reco}}$ [GeV]",      "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e2)},
        "reco_zenith": {"log_x": False, "log_y": True, "x_label": r"$\cos(\theta_{\mathrm{reco}})$", "sum_axes": 0, "flip": True,  "ylim": (1e-2, 5e2)},
    },
    "plot_components": True,
}

_DC_SPEC = {
    "det_config": "IC86_pass2_SnowStorm_FTP_HESE_DoubleCascades",
    "binning": {
        "reco_energy": np.geomspace(10**4.778, 10**7.1, 14),
        "bdt_product": np.linspace(0.122222211111, 1, 11),
    },
    "dim_info": {
        "reco_energy": {"log_x": True,  "log_y": True, "x_label": r"$E_{\mathrm{reco}}$ [GeV]", "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e2)},
        "bdt_product": {"log_x": False, "log_y": True, "x_label": "BDT product",                "sum_axes": 0, "flip": False, "ylim": (1e-2, 1e2)},
    },
    "plot_components": True,
}

_CHAN_SPECS = [
    ("cascades", "Cascades",        _CASCADES_SPEC),
    ("tracks",   "Tracks",          _TRACKS_SPEC),
    ("dc",       "Double Cascades", _DC_SPEC),
]

# best fit with the PassingHESE passing fractions, with the detector priors applied (fixed `prior` key)
# (previous fit without detector priors: nbestfit50_all_param_2sigma_1D_10steps_PassingHESE)
_SCAN = "nbestfit50_all_param_2sigma_1D_10steps_PassingHESE_fixedprior"

# (graph name, plot_flavor); plots have no title, the graph name is in the folder and file name
#   - graph with the astro parametrization of the fit: component plots
#   - graph with the equivalent 3-flavor parametrization (best-fit composition): astro split into NuE/NuMu/NuTau
_SEPARATE_SCANS = [
    (_SCAN,              False),
    (f"{_SCAN}_3flavor", True),
]

# graphs with one detector systematic at a time scanned over its fit range (5 steps + its best fit),
# all other detector systematics at nominal (values written by run_post_fit_scripts.ipynb)
import json
_DETSYST_FILE = ("/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/configs/flavor_globalfit/analysis_configs/data/hese/"
                 f"step2_hese_flavor_reunblind/plotting/{_SCAN}/{_SCAN}_detsyst_values.json")
with open(_DETSYST_FILE) as _f:
    _detsyst = json.load(_f)
_DETSYST_VALUES  = _detsyst["values"]

# the detsyst graphs use the 3-flavor parametrization: component plots and flavor plots from the same graph
_SEPARATE_SCANS += [
    (f"{_SCAN}_detsyst_{p}_{v:.4g}", plot_flavor)
    for p, values in _DETSYST_VALUES.items() for v in values for plot_flavor in (False, True)
]

def _lower_ylim(dim_info, decades=2):
    """Copy of dim_info with the lower y limit of every dimension lowered by `decades` decades."""
    return {dim: {**info, "ylim": (info["ylim"][0] / 10**decades, info["ylim"][1])} if "ylim" in info else info
            for dim, info in dim_info.items()}

_separate_plots = []
for _scan_name, _plot_flavor in _SEPARATE_SCANS:
    for _chan_key, _chan_label, _spec in _CHAN_SPECS:
        # all step2 plots: small components visible down to two decades lower
        _dim_info = _lower_ylim(_spec["dim_info"])
        for _show_count in [True, False]:
            for _plot_data in [True, False]:
                # no_syst: same best fit, but without the Snowstorm gradient shift
                for _no_syst in [False, True]:
                    _flavor_key   = "_flavor" if _plot_flavor else ""
                    _syst_key     = "_nosyst" if _no_syst else ""
                    _separate_plots.append({
                        "key":             f"name-{_scan_name}_channel-{_chan_key}_count-{_show_count}_data-{_plot_data}{_flavor_key}{_syst_key}",
                        "det_config":      _spec["det_config"],
                        "title":           "",
                        "scans":           [(_scan_name, "MC")],
                        "binning":         _spec["binning"],
                        "dim_info":        _dim_info,
                        "show_counts":     _show_count,
                        "plot_data":       _plot_data,
                        "plot_components": _spec["plot_components"],
                        "plot_flavor":     _plot_flavor,
                        "plot_muon_split": PLOT_MUON_SPLIT,
                        "no_syst":         _no_syst,
                        "show_chi2":       False,
                        "show_ks":         False,
                    })

# ---------------------------------------------------------------------------
# Full plots list
# ---------------------------------------------------------------------------

PLOTS = _separate_plots

# ---------------------------------------------------------------------------
# Convenience key groups
# ---------------------------------------------------------------------------

def _group(scan_name, suffix):
    return [
        f"name-{scan_name}_channel-{c}_count-{s}_data-{d}{suffix}"
        for c in ("cascades", "tracks", "dc")
        for s in (True, False)
        for d in (True, False)
    ]

# component plots, graph with the fit parametrization
GROUP_SEPARATE_PLOTTING      = _group(_SCAN, "")
GROUP_SEPARATE_NOSYST        = _group(_SCAN, "_nosyst")
# flavor plots, graph with the 3-flavor parametrization
GROUP_SEPARATE_FLAVOR        = _group(f"{_SCAN}_3flavor", "_flavor")
GROUP_SEPARATE_FLAVOR_NOSYST = _group(f"{_SCAN}_3flavor", "_flavor_nosyst")
# one detector systematic scanned: component and flavor plots, with and without the Snowstorm shift
# (the nosyst plots are the same for every value, the detector systematics only enter the Snowstorm shift)
GROUP_DETSYST = [k for p, values in _DETSYST_VALUES.items() for v in values
                 for suffix in ("", "_nosyst", "_flavor", "_flavor_nosyst")
                 for k in _group(f"{_SCAN}_detsyst_{p}_{v:.4g}", suffix)]
# variant graphs (detector systematic scans) are only built with MAKE_VARIANT_GRAPHS = True in
# reco_space_graphs.ipynb, so they are not part of GROUP_ALL
GROUP_VARIANTS = GROUP_DETSYST
GROUP_ALL = GROUP_SEPARATE_PLOTTING + GROUP_SEPARATE_FLAVOR + GROUP_SEPARATE_NOSYST + GROUP_SEPARATE_FLAVOR_NOSYST
