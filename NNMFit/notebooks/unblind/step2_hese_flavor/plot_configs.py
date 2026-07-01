"""Plot configuration for reco_space_bdt_plots.ipynb — step2_hese_flavor.

All plot keys use the format:
  name-{scan_name}_channel-{channel}_count-{bool}_data-{bool}[_flavor]

Import PLOTS and GROUP_* constants from this module.
"""
import numpy as np

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

# (scan_name, human-readable title suffix)
_SEPARATE_SCANS = [
    ("all_param_2sigma_1D_10steps", "all_param_2sigma_1D_10steps"),
]

_separate_plots = []
_flavor_separate_plots = []
for _scan_name, _title_suffix in _SEPARATE_SCANS:
    for _chan_key, _chan_label, _spec in _CHAN_SPECS:
        for _show_count in [True, False]:
            for _plot_data in [True, False]:
                _base = {
                    "det_config":      _spec["det_config"],
                    "title":           f"HESE {_chan_label} — {_title_suffix}",
                    "scans":           [(_scan_name, "MC")],
                    "binning":         _spec["binning"],
                    "dim_info":        _spec["dim_info"],
                    "show_counts":     _show_count,
                    "plot_data":       _plot_data,
                    "plot_components": _spec["plot_components"],
                    "show_chi2":       False,
                    "show_ks":         False,
                }
                _separate_plots.append({
                    **_base,
                    "key":         f"name-{_scan_name}_channel-{_chan_key}_count-{_show_count}_data-{_plot_data}",
                    "plot_flavor": False,
                })
                _flavor_separate_plots.append({
                    **_base,
                    "key":         f"name-{_scan_name}_channel-{_chan_key}_count-{_show_count}_data-{_plot_data}_flavor",
                    "title":       f"HESE {_chan_label} (flavors) — {_title_suffix}",
                    "plot_flavor": True,
                })

# ---------------------------------------------------------------------------
# Full plots list
# ---------------------------------------------------------------------------

PLOTS = _separate_plots + _flavor_separate_plots

# ---------------------------------------------------------------------------
# Convenience key groups
# ---------------------------------------------------------------------------

GROUP_SEPARATE_PLOTTING = [
    f"name-{_scan_name}_channel-{c}_count-{s}_data-{d}"
    for _scan_name, _ in _SEPARATE_SCANS
    for c in ("cascades", "tracks", "dc")
    for s in (True, False)
    for d in (True, False)
]

GROUP_SEPARATE_FLAVOR = [
    f"name-{_scan_name}_channel-{c}_count-{s}_data-{d}_flavor"
    for _scan_name, _ in _SEPARATE_SCANS
    for c in ("cascades", "tracks", "dc")
    for s in (True, False)
    for d in (True, False)
]

GROUP_ALL = GROUP_SEPARATE_PLOTTING + GROUP_SEPARATE_FLAVOR
