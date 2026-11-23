"""Plot configuration for reco_space_bdt_plots.ipynb — step1_hese_flux_reunblind.

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

# best fit with the PassingHESE passing fractions
_SCAN = "nbestfit50_all_param_2sigma_1D_10steps_PassingHESE"
# graphs with the crystal density scaling (ice_crystal) fixed by hand
_CRYSTAL_VALUES = [0.9, 1.0, 1.1, 1.2]

# (graph name, human-readable title suffix, plot_flavor)
#   - graph with the astro parametrization of the fit: component plots
#   - graph with the equivalent 3-flavor parametrization (1:1:1): astro split into NuE/NuMu/NuTau
#   - graph with the fit parametrization, old passing fractions (data_v3 datasets, old Snowstorm gradients)
#   - graphs with the fit parametrization, ice_crystal fixed by hand
_SEPARATE_SCANS = [
    (_SCAN,                            "step1 re-unblinding best fit",                    False),
    (f"{_SCAN}_3flavor",               "step1 best fit, 3-flavor parametrization (1:1:1)", True),
    (f"{_SCAN}_old_passing_fractions", "step1 best fit, old passing fractions",          False),
] + [
    (f"{_SCAN}_ice_crystal_{v}",       f"step1 best fit, ice_crystal = {v}",              False)
    for v in _CRYSTAL_VALUES
]

_separate_plots = []
for _scan_name, _title_suffix, _plot_flavor in _SEPARATE_SCANS:
    for _chan_key, _chan_label, _spec in _CHAN_SPECS:
        for _show_count in [True, False]:
            for _plot_data in [True, False]:
                # no_syst: same best fit, but without the Snowstorm gradient shift
                for _no_syst in [False, True]:
                    _flavor_key   = "_flavor" if _plot_flavor else ""
                    _flavor_title = " (flavors)" if _plot_flavor else ""
                    _syst_key     = "_nosyst" if _no_syst else ""
                    _syst_title   = " (no SnowStorm syst.)" if _no_syst else ""
                    _separate_plots.append({
                        "key":             f"name-{_scan_name}_channel-{_chan_key}_count-{_show_count}_data-{_plot_data}{_flavor_key}{_syst_key}",
                        "det_config":      _spec["det_config"],
                        "title":           f"HESE {_chan_label}{_flavor_title} — {_title_suffix}{_syst_title}",
                        "scans":           [(_scan_name, "MC")],
                        "binning":         _spec["binning"],
                        "dim_info":        _spec["dim_info"],
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
# component plots, old passing fractions
GROUP_OLD_PASSING_FRACTIONS        = _group(f"{_SCAN}_old_passing_fractions", "")
GROUP_OLD_PASSING_FRACTIONS_NOSYST = _group(f"{_SCAN}_old_passing_fractions", "_nosyst")

# component plots, ice_crystal fixed by hand (the nosyst plots are identical to GROUP_SEPARATE_NOSYST,
# ice_crystal only enters the Snowstorm shift, so they are not part of GROUP_ALL)
GROUP_ICE_CRYSTAL        = [k for v in _CRYSTAL_VALUES for k in _group(f"{_SCAN}_ice_crystal_{v}", "")]
GROUP_ICE_CRYSTAL_NOSYST = [k for v in _CRYSTAL_VALUES for k in _group(f"{_SCAN}_ice_crystal_{v}", "_nosyst")]

GROUP_ALL = (GROUP_SEPARATE_PLOTTING + GROUP_SEPARATE_FLAVOR + GROUP_SEPARATE_NOSYST + GROUP_SEPARATE_FLAVOR_NOSYST
             + GROUP_OLD_PASSING_FRACTIONS + GROUP_OLD_PASSING_FRACTIONS_NOSYST + GROUP_ICE_CRYSTAL)
