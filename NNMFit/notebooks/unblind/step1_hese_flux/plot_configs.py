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
    "show_counts": True, "plot_components": True,
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
    "show_counts": True, "plot_components": True,
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
    "show_counts": True, "plot_components": True, 
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
        "11features_plus_rloglmilli_econf_evtgen",
    ),
]

_separate_plots = []
for _scan_name, _title_suffix in _SEPARATE_SCANS:
    for _chan_key, _chan_label, _spec in _CHAN_SPECS:
        for _show_count in [True, False]:
            for _plot_data in [True, False]:
                _entry = {
                    "key":             f"name-{_scan_name}_channel-{_chan_key}_count-{_show_count}_data-{_plot_data}",
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
                _separate_plots.append(_entry)

# ---------------------------------------------------------------------------
# Combined plots — BDT variable space (11features model, with Snowstorm systematics)
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

_combined_plots = []
for _var, _vcfg in _VAR_CONFIGS.items():
    _scan = f"11features_plus_rloglmilli_econf_evtgen_{_var}"
    _combined_plots.append({
        "key":             _scan,
        "det_config":      "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title":           f"HESE Combined {_vcfg['title']} — 11feat+rlogl+econf+evtgen",
        "scans":           [(_scan, "MC")],
        "binning":         _vcfg["binning"],
        "dim_info":        _vcfg["dim_info"],
        "show_counts":     False,
        "plot_components": True,
        "show_chi2":       False,
        "show_ks":         False,
    })

# ---------------------------------------------------------------------------
# Full plots list
# ---------------------------------------------------------------------------

PLOTS = _separate_plots + _combined_plots

# ---------------------------------------------------------------------------
# Convenience key groups
# ---------------------------------------------------------------------------

_VARS = list(_VAR_CONFIGS.keys())

GROUP_SEPARATE_PLOTTING = [
    f"name-11features_plus_rloglmilli_econf_evtgen_channel-{c}_count-{s}_data-{d}"
    for c in ("cascades", "tracks", "dc")
    for s in (True, False)
    for d in (True, False)
]

GROUP_BDT_VARS = [f"11features_plus_rloglmilli_econf_evtgen_{v}" for v in _VARS]

GROUP_ALL = GROUP_SEPARATE_PLOTTING + GROUP_BDT_VARS
