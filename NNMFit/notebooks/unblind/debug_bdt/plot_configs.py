"""Plot configuration for reco_space_bdt_plots.ipynb.

All plot keys match the graph directory names produced by reco_space_graphs.ipynb.
Separate-detector plots use {scan_name}_{channel} where channel is cascades/tracks/dc.
Combined plots use the scan name directly as the key.

Import PLOTS and GROUP_* constants from this module.
"""
import numpy as np

COMPONENT_COLORS = {"Astro": "tab:red", "Conv": "tab:green", "Muon": "tab:orange"}
COMPONENTS = ["Astro", "Conv", "Muon"]

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
    "show_counts": False, "plot_components": True,
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
    "show_counts": False, "plot_components": True,
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
    "show_counts": False, "plot_components": True, "plot_data": False,
}

_CHAN_SPECS = [
    ("cascades", "Cascades",        _CASCADES_SPEC),
    ("tracks",   "Tracks",          _TRACKS_SPEC),
    ("dc",       "Double Cascades", _DC_SPEC),
]

# (scan_name, human-readable title suffix)
_SEPARATE_SCANS = [
    (
        "11features_plus_rloglmilli_econf_evtgen",
        "11feat+rlogl+econf+evtgen (bdtprod binning)",
    ),
    (
        "FinalTopology_double_energy_length_binning",
        "FinalTopology (energy×length binning)",
    ),
    (
        "11features_double_energy_bdtprod_binning_bestfit_Finaltopology",
        "11feat (bdtprod binning, FT bestfit)",
    ),
    (
        "11features_plus_rloglmilli_econf_evtgen_double_energy_bdtprod_binning_bestfit_Finaltopology",
        "11feat+rlogl+econf+evtgen (bdtprod binning, FT bestfit)",
    ),
]

_separate_plots = []
for _scan_name, _title_suffix in _SEPARATE_SCANS:
    for _chan_key, _chan_label, _spec in _CHAN_SPECS:
        _entry = {
            "key":             f"{_scan_name}_{_chan_key}",
            "det_config":      _spec["det_config"],
            "title":           f"HESE {_chan_label} — {_title_suffix}",
            "scans":           [(_scan_name, "MC")],
            "binning":         _spec["binning"],
            "dim_info":        _spec["dim_info"],
            "show_counts":     _spec["show_counts"],
            "plot_components": _spec["plot_components"],
            "show_chi2":       False,
            "show_ks":         False,
        }
        if "plot_data" in _spec:
            _entry["plot_data"] = _spec["plot_data"]
        _separate_plots.append(_entry)

# ---------------------------------------------------------------------------
# Combined plots — BDT variable space
# ---------------------------------------------------------------------------

_VAR_CONFIGS = {
    "bdt1_bdt2": {
        "title": "BDT Scores",
        "binning": {
            "bdt_scores1": np.linspace(0.0, 1, 11),
            "bdt_scores2": np.linspace(0.0, 1, 11),
        },
        "dim_info": {
            "bdt_scores1": {"log_x": False, "log_y": True, "x_label": "BDT Score 1", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "bdt_scores2": {"log_x": False, "log_y": True, "x_label": "BDT Score 2", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
    },
    "energy_length_analysis": {
        "title": "Energy vs Length",
        "binning": {
            "reco_energy": np.geomspace(10**4.778, 10**7.1, 14),
            "reco_length": np.geomspace(1e1, 1e3, 11),
        },
        "dim_info": {
            "reco_energy": {"log_x": True, "log_y": True, "x_label": r"$E_{\mathrm{reco}}$ [GeV]", "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e2)},
            "reco_length": {"log_x": True, "log_y": True, "x_label": r"$L_{\tau}$ [m]",            "sum_axes": 0, "flip": False, "ylim": (1e-2, 1e3)},
        },
    },
    "len_easym": {
        "title": "Taupede Length vs Asymmetry",
        "binning": {
            "Taupede_Distance":  np.geomspace(10**0.1360, 10**3.0133, 11),
            "Taupede_Asymmetry": np.linspace(-1.001, 1.001, 11),
        },
        "dim_info": {
            "Taupede_Distance":  {"log_x": True,  "log_y": True, "x_label": "Taupede Length",    "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "Taupede_Asymmetry": {"log_x": False, "log_y": True, "x_label": "Taupede Asymmetry", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
    },
    "e1_e2": {
        "title": "Taupede Particle Energies",
        "binning": {
            "Taupede1_Particles_energy": np.geomspace(10**1.9875, 10**10.3972, 11),
            "Taupede2_Particles_energy": np.geomspace(10**0.5207, 10**8.0231, 11),
        },
        "dim_info": {
            "Taupede1_Particles_energy": {"log_x": True, "log_y": True, "x_label": "Taupede Energy 1", "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e3)},
            "Taupede2_Particles_energy": {"log_x": True, "log_y": True, "x_label": "Taupede Energy 2", "sum_axes": 0, "flip": False, "ylim": (1e-2, 1e3)},
        },
    },
    "e1_e2_zoom": {
        "title": "Taupede Particle Energies (zoom)",
        "binning": {
            "Taupede1_Particles_energy": np.geomspace(10**2, 10**7, 11),
            "Taupede2_Particles_energy": np.geomspace(10**2, 10**7, 11),
        },
        "dim_info": {
            "Taupede1_Particles_energy": {"log_x": True, "log_y": True, "x_label": "Taupede Energy 1", "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e3)},
            "Taupede2_Particles_energy": {"log_x": True, "log_y": True, "x_label": "Taupede Energy 2", "sum_axes": 0, "flip": False, "ylim": (1e-2, 1e3)},
        },
    },
    "mono_energy_zenith": {
        "title": "MonopodFit Energy vs Zenith",
        "binning": {
            "MonopodFit_iMIGRAD_PPB0_energy":  np.geomspace(10**4.4758, 10**8.2502, 11),
            "cscdSBU_MonopodFit4_noDC_zenith": np.linspace(0.0317, 3.1400, 11),
        },
        "dim_info": {
            "MonopodFit_iMIGRAD_PPB0_energy":  {"log_x": True,  "log_y": True, "x_label": "MonopodFit Energy", "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e2)},
            "cscdSBU_MonopodFit4_noDC_zenith": {"log_x": False, "log_y": True, "x_label": "Monopod Zenith",    "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
    },
    "mono_delay_qmax": {
        "title": "MonopodFit Delay vs Q Max DOMs",
        "binning": {
            "MonopodFit_iMIGRAD_PPB0_Delay_ice": np.linspace(-15011.9669, 1120.3790, 11),
            "CVStatistics_q_max_doms":            np.linspace(-712.6985, 22417.2985, 11),
        },
        "dim_info": {
            "MonopodFit_iMIGRAD_PPB0_Delay_ice": {"log_x": False, "log_y": True, "x_label": "Delay Ice",  "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "CVStatistics_q_max_doms":            {"log_x": False, "log_y": True, "x_label": "Q Max DOMs", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
    },
    "mono_delay_qmax_zoom": {
        "title": "MonopodFit Delay vs Q Max DOMs (zoom)",
        "binning": {
            "MonopodFit_iMIGRAD_PPB0_Delay_ice": np.linspace(-2000, 1000, 11),
            "CVStatistics_q_max_doms":            np.linspace(0, 10000, 11),
        },
        "dim_info": {
            "MonopodFit_iMIGRAD_PPB0_Delay_ice": {"log_x": False, "log_y": True, "x_label": "Delay Ice",  "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "CVStatistics_q_max_doms":            {"log_x": False, "log_y": True, "x_label": "Q Max DOMs", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
    },
    "vtxdist_qtot": {
        "title": "Vertex Reco Dist vs Qtot HLC",
        "binning": {
            "cscdSBU_VertexRecoDist_CscdLLh": np.linspace(-18.1670, 462.2055, 11),
            "cscdSBU_Qtot_HLC_log":           np.linspace(3.7310, 5.5967, 11),
        },
        "dim_info": {
            "cscdSBU_VertexRecoDist_CscdLLh": {"log_x": False, "log_y": True, "x_label": "Vertex Reco Dist Cscd", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "cscdSBU_Qtot_HLC_log":           {"log_x": False, "log_y": True, "x_label": "log10(Qtot HLC)",       "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
    },
    "vtxdist_qtot_zoom": {
        "title": "Vertex Reco Dist vs Qtot HLC (zoom)",
        "binning": {
            "cscdSBU_VertexRecoDist_CscdLLh": np.linspace(0, 150, 11),
            "cscdSBU_Qtot_HLC_log":           np.linspace(3.7310, 5.5967, 11),
        },
        "dim_info": {
            "cscdSBU_VertexRecoDist_CscdLLh": {"log_x": False, "log_y": True, "x_label": "Vertex Reco Dist Cscd", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "cscdSBU_Qtot_HLC_log":           {"log_x": False, "log_y": True, "x_label": "log10(Qtot HLC)",       "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
    },
    "taumono_econf": {
        "title": "TauMono rlogl vs Econfinement",
        "binning": {
            "TauMonoDiff_rlogl": np.linspace(-8.8396, 0.4251, 11),
            "econfinement":      np.linspace(-0.001, 1.001, 11),
        },
        "dim_info": {
            "TauMonoDiff_rlogl": {"log_x": False, "log_y": True, "x_label": "Tau-Mono rlogl", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "econfinement":      {"log_x": False, "log_y": True, "x_label": "Econfinement",   "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
    },
    "taumono_econf_zoom": {
        "title": "TauMono rlogl vs Econfinement (zoom)",
        "binning": {
            "TauMonoDiff_rlogl": np.linspace(-2.5, 0.2, 11),
            "econfinement":      np.linspace(0.75, 1.0010, 11),
        },
        "dim_info": {
            "TauMonoDiff_rlogl": {"log_x": False, "log_y": True, "x_label": "Tau-Mono rlogl", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "econfinement":      {"log_x": False, "log_y": True, "x_label": "Econfinement",   "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
    },
    "tauspe_taumilli": {
        "title": "TauSPE vs TauMono Milli rlogl",
        "binning": {
            "TauSPEMilliDiff_rlogl":  np.linspace(-7.0223, 1.1643, 11),
            "TauMonoMilliDiff_rlogl": np.linspace(-4.5702, 0.2189, 11),
        },
        "dim_info": {
            "TauSPEMilliDiff_rlogl":  {"log_x": False, "log_y": True, "x_label": "Tau-SPE Milli rlogl",  "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "TauMonoMilliDiff_rlogl": {"log_x": False, "log_y": True, "x_label": "Tau-Mono Milli rlogl", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
    },
    "tauspe_taumilli_zoom": {
        "title": "TauSPE vs TauMono Milli rlogl (zoom)",
        "binning": {
            "TauSPEMilliDiff_rlogl":  np.linspace(-2, 1, 11),
            "TauMonoMilliDiff_rlogl": np.linspace(-1.5, 0.2, 11),
        },
        "dim_info": {
            "TauSPEMilliDiff_rlogl":  {"log_x": False, "log_y": True, "x_label": "Tau-SPE Milli rlogl",  "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "TauMonoMilliDiff_rlogl": {"log_x": False, "log_y": True, "x_label": "Tau-Mono Milli rlogl", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
    },
    "evtgen_recoeratio": {
        "title": "EventGenerator Length vs E Ratio",
        "binning": {
            "EventGeneratorDC_Thijs_length":   np.linspace(-446.7254, 838.6997, 11),
            "RecoERatio_EventGeneratorDC_Max": np.linspace(-1.1000, 1.0984, 11),
        },
        "dim_info": {
            "EventGeneratorDC_Thijs_length":   {"log_x": False, "log_y": True, "x_label": "EventGen Length", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "RecoERatio_EventGeneratorDC_Max": {"log_x": False, "log_y": True, "x_label": "EvtGen E Ratio",  "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
    },
    "evtgen_recoeratio_zoom": {
        "title": "EventGenerator Length vs E Ratio (zoom)",
        "binning": {
            "EventGeneratorDC_Thijs_length":   np.geomspace(10**0, 10**3, 11),
            "RecoERatio_EventGeneratorDC_Max": np.linspace(-1.1000, 1.0984, 11),
        },
        "dim_info": {
            "EventGeneratorDC_Thijs_length":   {"log_x": True,  "log_y": True, "x_label": "EventGen Length", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "RecoERatio_EventGeneratorDC_Max": {"log_x": False, "log_y": True, "x_label": "EvtGen E Ratio",  "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
    },
}

# (scan_name prefix, human-readable model label)
_COMBINED_MODELS = [
    ("FinalTopology_double_energy_length_binning", "FinalTopology"),
    ("11features_plus_rloglmilli_econf_evtgen",    "11feat+rlogl+econf+evtgen"),
]

_combined_plots = []
for _model_prefix, _model_label in _COMBINED_MODELS:
    for _var, _vcfg in _VAR_CONFIGS.items():
        for _nosyst, _syst_label in [(True, "No Systematics"), (False, "With Systematics")]:
            _scan = f"{_model_prefix}_NoSystematics_{_var}" if _nosyst else f"{_model_prefix}_{_var}"
            _combined_plots.append({
                "key":             _scan,
                "det_config":      "IC86_pass2_SnowStorm_FTP_HESE_Combined",
                "title":           f"HESE Combined {_vcfg['title']} — {_model_label} — {_syst_label}",
                "scans":           [(_scan, "MC")],
                "binning":         _vcfg["binning"],
                "dim_info":        _vcfg["dim_info"],
                "show_counts":     False,
                "plot_components": True,
                "show_chi2":       True,
                "show_ks":         True,
            })

# ---------------------------------------------------------------------------
# Feature comparison plots (fixed bdt1_bdt2 binning, different feature sets)
# ---------------------------------------------------------------------------

_FEATURE_NAMES = [
    ("11features_plus_rloglmilli_econf_evtgen", "11feat+rlogl+econf+evtgen"),
    ("11features",                              "11feat (base)"),
    ("11features_plus_rloglmilli",              "11feat+rloglmilli"),
    ("11features_plus_econf",                   "11feat+econf"),
    ("11features_plus_evtgen",                  "11feat+evtgen"),
]

_BDT_SCORES_BINNING = {
    "bdt_scores1": np.linspace(0.0, 1, 11),
    "bdt_scores2": np.linspace(0.0, 1, 11),
}
_BDT_SCORES_DIM_INFO = {
    "bdt_scores1": {"log_x": False, "log_y": True, "x_label": "BDT Score 1", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
    "bdt_scores2": {"log_x": False, "log_y": True, "x_label": "BDT Score 2", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
}

_feature_plots = []
for _feat_name, _feat_label in _FEATURE_NAMES:
    for _nosyst, _syst_label in [(True, "No Systematics"), (False, "With Systematics")]:
        if _nosyst:
            _scan = f"NoSystematics_bdt1_bdt2_{_feat_name}_bestfit_FinalTopology_binning_bdt"
        else:
            _scan = f"bdt1_bdt2_{_feat_name}_bestfit_FinalTopology_binning_bdt"
        _feature_plots.append({
            "key":             _scan,
            "det_config":      "IC86_pass2_SnowStorm_FTP_HESE_Combined",
            "title":           f"BDT Scores — {_feat_label} — {_syst_label}",
            "scans":           [(_scan, "MC")],
            "binning":         _BDT_SCORES_BINNING,
            "dim_info":        _BDT_SCORES_DIM_INFO,
            "show_counts":     False,
            "plot_components": True,
            "show_chi2":       True,
            "show_ks":         True,
        })

# ---------------------------------------------------------------------------
# Full plots list
# ---------------------------------------------------------------------------

PLOTS = _separate_plots + _combined_plots + _feature_plots

# ---------------------------------------------------------------------------
# Convenience key groups
# ---------------------------------------------------------------------------

_VARS = list(_VAR_CONFIGS.keys())

GROUP_SEPARATE_11FEAT_PLOTTING = [
    f"11features_plus_rloglmilli_econf_evtgen_{c}" for c in ("cascades", "tracks", "dc")
]
GROUP_SEPARATE_FINALTOPO = [
    f"FinalTopology_double_energy_length_binning_{c}" for c in ("cascades", "tracks", "dc")
]
GROUP_SEPARATE_11FEAT_BDTPROD = [
    f"11features_double_energy_bdtprod_binning_bestfit_Finaltopology_{c}"
    for c in ("cascades", "tracks", "dc")
]
GROUP_SEPARATE_11FEAT_FULL_BDTPROD = [
    f"11features_plus_rloglmilli_econf_evtgen_double_energy_bdtprod_binning_bestfit_Finaltopology_{c}"
    for c in ("cascades", "tracks", "dc")
]
GROUP_SEPARATE = (GROUP_SEPARATE_11FEAT_PLOTTING + GROUP_SEPARATE_FINALTOPO
                  + GROUP_SEPARATE_11FEAT_BDTPROD + GROUP_SEPARATE_11FEAT_FULL_BDTPROD)

GROUP_FINALTOPO_NOSYST = [f"FinalTopology_double_energy_length_binning_NoSystematics_{v}" for v in _VARS]
GROUP_FINALTOPO_SYST   = [f"FinalTopology_double_energy_length_binning_{v}" for v in _VARS]
GROUP_11FEAT_NOSYST    = [f"11features_plus_rloglmilli_econf_evtgen_NoSystematics_{v}" for v in _VARS]
GROUP_11FEAT_SYST      = [f"11features_plus_rloglmilli_econf_evtgen_{v}" for v in _VARS]

GROUP_FEATURE_BDT_NOSYST = [
    f"NoSystematics_bdt1_bdt2_{f}_bestfit_FinalTopology_binning_bdt" for f, _ in _FEATURE_NAMES
]
GROUP_FEATURE_BDT_SYST = [
    f"bdt1_bdt2_{f}_bestfit_FinalTopology_binning_bdt" for f, _ in _FEATURE_NAMES
]
GROUP_FEATURE_BDT = GROUP_FEATURE_BDT_NOSYST + GROUP_FEATURE_BDT_SYST

GROUP_ALL = (GROUP_SEPARATE
             + GROUP_FINALTOPO_NOSYST + GROUP_FINALTOPO_SYST
             + GROUP_11FEAT_NOSYST   + GROUP_11FEAT_SYST
             + GROUP_FEATURE_BDT)
