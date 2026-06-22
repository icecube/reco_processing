"""
Plot configuration for reco_space_bdt_plots.ipynb.

Scan names follow the pattern  `{model}_{suffix}`  matching the directories
produced by reco_space_graphs.ipynb under  graphs/{model}/.

Call `get_plots(model)` to obtain a list of plot dicts with all scan names
resolved.  Each dict has:
    key              : short string for selecting plot subsets (see GROUP_* below)
    det_config       : detector config name
    title            : figure title
    scans            : list of (scan_name, label)
    binning          : {var_name: edges_array}
    dim_info         : {var_name: {log_x, log_y, x_label, sum_axes, flip, ylim}}
    show_counts      : bool (default False)
    plot_components  : bool (default False)
    plot_data        : bool (default True)
"""
import numpy as np

COMPONENT_COLORS = {"Astro": "tab:red", "Conv": "tab:green", "Muon": "tab:orange"}
COMPONENTS = ["Astro", "Conv", "Muon"]

# ---------------------------------------------------------------------------
# Plot templates — use "{model}" as placeholder; resolved by get_plots(model)
# ---------------------------------------------------------------------------

_PLOT_TEMPLATES = [

    # ---- Best-fit: separate detector channels (energy / zenith) ----
    {
        "key": "cascades_syst",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Cascades",
        "title": "HESE Cascades With Systematics",
        "scans": [("{model}", "MC")],
        "binning": {
            "reco_energy": np.geomspace(10**4.778, 10**7.1, 24),
            "reco_zenith": np.linspace(-1, 1, 11),
        },
        "dim_info": {
            "reco_energy": {"log_x": True,  "log_y": True, "x_label": r"$E_{\mathrm{reco}}$ [GeV]",      "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e2)},
            "reco_zenith": {"log_x": False, "log_y": True, "x_label": r"$\cos(\theta_{\mathrm{reco}})$", "sum_axes": 0, "flip": True,  "ylim": (1e-2, 1e2)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "tracks_syst",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Tracks",
        "title": "HESE Tracks With Systematics",
        "scans": [("{model}", "MC")],
        "binning": {
            "reco_energy": np.geomspace(10**4.778, 10**7.1, 24),
            "reco_zenith": np.linspace(-1, 1, 11),
        },
        "dim_info": {
            "reco_energy": {"log_x": True,  "log_y": True, "x_label": r"$E_{\mathrm{reco}}$ [GeV]",      "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e2)},
            "reco_zenith": {"log_x": False, "log_y": True, "x_label": r"$\cos(\theta_{\mathrm{reco}})$", "sum_axes": 0, "flip": True,  "ylim": (1e-2, 5e2)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "dc_syst",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_DoubleCascades",
        "title": "HESE Double Cascades With Systematics",
        "scans": [("{model}", "MC")],
        "binning": {
            "reco_energy": np.geomspace(10**4.778, 10**7.1, 14),
            "bdt_product": np.linspace(0.122222211111, 1, 11),
        },
        "dim_info": {
            "reco_energy": {"log_x": True,  "log_y": True, "x_label": r"$E_{\mathrm{reco}}$ [GeV]", "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e2)},
            "bdt_product": {"log_x": False, "log_y": True, "x_label": "BDT product",                "sum_axes": 0, "flip": False, "ylim": (1e-2, 1e2)},
        },
        "show_counts": True, "plot_components": True, "plot_data": False,
    },

    # ---- Combined dataset — BDT variables, no systematics ----
    {
        "key": "combined_bdt_scores",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "HESE Combined BDT Scores — No Systematics",
        "scans": [("{model}_NoSystematics_bdt1_bdt2", "MC")],
        "binning": {
            "bdt_scores1": np.linspace(0.0, 1, 11),
            "bdt_scores2": np.linspace(0.0, 1, 11),
        },
        "dim_info": {
            "bdt_scores1": {"log_x": False, "log_y": True, "x_label": "BDT Score 1", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "bdt_scores2": {"log_x": False, "log_y": True, "x_label": "BDT Score 2", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_energy_length",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "HESE Combined Energy vs Length — No Systematics",
        "scans": [("{model}_NoSystematics_energy_length_analysis", "MC")],
        "binning": {
            "reco_energy": np.geomspace(10**4.778, 10**7.1, 14),
            "reco_length": np.geomspace(1e1, 1e3, 11),
        },
        "dim_info": {
            "reco_energy": {"log_x": True, "log_y": True, "x_label": r"$E_{\mathrm{reco}}$ [GeV]", "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e2)},
            "reco_length": {"log_x": True, "log_y": True, "x_label": r"$L_{\tau}$ [m]",            "sum_axes": 0, "flip": False, "ylim": (1e-2, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_len_easym",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "Taupede Length vs Asymmetry — No Systematics",
        "scans": [("{model}_NoSystematics_len_easym", "MC")],
        "binning": {
            "Taupede_Distance":  np.geomspace(10**0.1360, 10**3.0133, 11),
            "Taupede_Asymmetry": np.linspace(-1.001, 1.001, 11),
        },
        "dim_info": {
            "Taupede_Distance":  {"log_x": True,  "log_y": True, "x_label": "Taupede Length",    "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "Taupede_Asymmetry": {"log_x": False, "log_y": True, "x_label": "Taupede Asymmetry", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_e1_e2",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "Taupede Particle Energies — No Systematics",
        "scans": [("{model}_NoSystematics_e1_e2", "MC")],
        "binning": {
            "Taupede1_Particles_energy": np.geomspace(10**1.9875, 10**10.3972, 11),
            "Taupede2_Particles_energy": np.geomspace(10**0.5207, 10**8.0231, 11),
        },
        "dim_info": {
            "Taupede1_Particles_energy": {"log_x": True, "log_y": True, "x_label": "Taupede Energy 1", "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e3)},
            "Taupede2_Particles_energy": {"log_x": True, "log_y": True, "x_label": "Taupede Energy 2", "sum_axes": 0, "flip": False, "ylim": (1e-2, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_mono_energy_zenith",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "MonopodFit Energy vs Zenith — No Systematics",
        "scans": [("{model}_NoSystematics_mono_energy_zenith", "MC")],
        "binning": {
            "MonopodFit_iMIGRAD_PPB0_energy":  np.geomspace(10**4.4758, 10**8.2502, 11),
            "cscdSBU_MonopodFit4_noDC_zenith": np.linspace(0.0317, 3.1400, 11),
        },
        "dim_info": {
            "MonopodFit_iMIGRAD_PPB0_energy":  {"log_x": True,  "log_y": True, "x_label": "MonopodFit Energy", "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e2)},
            "cscdSBU_MonopodFit4_noDC_zenith": {"log_x": False, "log_y": True, "x_label": "Monopod Zenith",    "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_mono_delay_qmax",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "MonopodFit Delay vs Q Max DOMs — No Systematics",
        "scans": [("{model}_NoSystematics_mono_delay_qmax", "MC")],
        "binning": {
            "MonopodFit_iMIGRAD_PPB0_Delay_ice": np.linspace(-15011.9669, 1120.3790, 11),
            "CVStatistics_q_max_doms":            np.linspace(-712.6985, 22417.2985, 11),
        },
        "dim_info": {
            "MonopodFit_iMIGRAD_PPB0_Delay_ice": {"log_x": False, "log_y": True, "x_label": "Delay Ice",  "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "CVStatistics_q_max_doms":            {"log_x": False, "log_y": True, "x_label": "Q Max DOMs", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_vtxdist_qtot",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "Vertex Reco Dist vs Qtot HLC — No Systematics",
        "scans": [("{model}_NoSystematics_vtxdist_qtot", "MC")],
        "binning": {
            "cscdSBU_VertexRecoDist_CscdLLh": np.linspace(-18.1670, 462.2055, 11),
            "cscdSBU_Qtot_HLC_log":           np.linspace(3.7310, 5.5967, 11),
        },
        "dim_info": {
            "cscdSBU_VertexRecoDist_CscdLLh": {"log_x": False, "log_y": True, "x_label": "Vertex Reco Dist Cscd", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "cscdSBU_Qtot_HLC_log":           {"log_x": False, "log_y": True, "x_label": "log10(Qtot HLC)",       "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_taumono_econf",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "TauMono rlogl vs Econfinement — No Systematics",
        "scans": [("{model}_NoSystematics_taumono_econf", "MC")],
        "binning": {
            "TauMonoDiff_rlogl": np.linspace(-8.8396, 0.4251, 11),
            "econfinement":      np.linspace(-0.001, 1.001, 11),
        },
        "dim_info": {
            "TauMonoDiff_rlogl": {"log_x": False, "log_y": True, "x_label": "Tau-Mono rlogl", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "econfinement":      {"log_x": False, "log_y": True, "x_label": "Econfinement",   "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_tauspe_taumilli",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "TauSPE vs TauMono Milli rlogl — No Systematics",
        "scans": [("{model}_NoSystematics_tauspe_taumilli", "MC")],
        "binning": {
            "TauSPEMilliDiff_rlogl":  np.linspace(-7.0223, 1.1643, 11),
            "TauMonoMilliDiff_rlogl": np.linspace(-4.5702, 0.2189, 11),
        },
        "dim_info": {
            "TauSPEMilliDiff_rlogl":  {"log_x": False, "log_y": True, "x_label": "Tau-SPE Milli rlogl",  "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "TauMonoMilliDiff_rlogl": {"log_x": False, "log_y": True, "x_label": "Tau-Mono Milli rlogl", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_evtgen_recoeratio",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "EventGenerator Length vs E Ratio — No Systematics",
        "scans": [("{model}_NoSystematics_evtgen_recoeratio", "MC")],
        "binning": {
            "EventGeneratorDC_Thijs_length":   np.linspace(-446.7254, 838.6997, 11),
            "RecoERatio_EventGeneratorDC_Max": np.linspace(-1.1000, 1.0984, 11),
        },
        "dim_info": {
            "EventGeneratorDC_Thijs_length":   {"log_x": False, "log_y": True, "x_label": "EventGen Length", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "RecoERatio_EventGeneratorDC_Max": {"log_x": False, "log_y": True, "x_label": "EvtGen E Ratio",  "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },

    # ---- Combined dataset — BDT variables, no systematics (zoom) ----
    {
        "key": "combined_e1_e2_zoom",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "Taupede Particle Energies Zoom — No Systematics",
        "scans": [("{model}_NoSystematics_e1_e2_zoom", "MC")],
        "binning": {
            "Taupede1_Particles_energy": np.geomspace(10**2, 10**7, 11),
            "Taupede2_Particles_energy": np.geomspace(10**2, 10**7, 11),
        },
        "dim_info": {
            "Taupede1_Particles_energy": {"log_x": True, "log_y": True, "x_label": "Taupede Energy 1", "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e3)},
            "Taupede2_Particles_energy": {"log_x": True, "log_y": True, "x_label": "Taupede Energy 2", "sum_axes": 0, "flip": False, "ylim": (1e-2, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_mono_delay_qmax_zoom",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "MonopodFit Delay vs Q Max DOMs Zoom — No Systematics",
        "scans": [("{model}_NoSystematics_mono_delay_qmax_zoom", "MC")],
        "binning": {
            "MonopodFit_iMIGRAD_PPB0_Delay_ice": np.linspace(-2000, 1000, 11),
            "CVStatistics_q_max_doms":            np.linspace(0, 10000, 11),
        },
        "dim_info": {
            "MonopodFit_iMIGRAD_PPB0_Delay_ice": {"log_x": False, "log_y": True, "x_label": "Delay Ice",  "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "CVStatistics_q_max_doms":            {"log_x": False, "log_y": True, "x_label": "Q Max DOMs", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_vtxdist_qtot_zoom",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "Vertex Reco Dist vs Qtot HLC Zoom — No Systematics",
        "scans": [("{model}_NoSystematics_vtxdist_qtot_zoom", "MC")],
        "binning": {
            "cscdSBU_VertexRecoDist_CscdLLh": np.linspace(0, 150, 11),
            "cscdSBU_Qtot_HLC_log":           np.linspace(3.7310, 5.5967, 11),
        },
        "dim_info": {
            "cscdSBU_VertexRecoDist_CscdLLh": {"log_x": False, "log_y": True, "x_label": "Vertex Reco Dist Cscd", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "cscdSBU_Qtot_HLC_log":           {"log_x": False, "log_y": True, "x_label": "log10(Qtot HLC)",       "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_taumono_econf_zoom",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "TauMono rlogl vs Econfinement Zoom — No Systematics",
        "scans": [("{model}_NoSystematics_taumono_econf_zoom", "MC")],
        "binning": {
            "TauMonoDiff_rlogl": np.linspace(-2.5, 0.2, 11),
            "econfinement":      np.linspace(0.75, 1.0010, 11),
        },
        "dim_info": {
            "TauMonoDiff_rlogl": {"log_x": False, "log_y": True, "x_label": "Tau-Mono rlogl", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "econfinement":      {"log_x": False, "log_y": True, "x_label": "Econfinement",   "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_tauspe_taumilli_zoom",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "TauSPE vs TauMono Milli rlogl Zoom — No Systematics",
        "scans": [("{model}_NoSystematics_tauspe_taumilli_zoom", "MC")],
        "binning": {
            "TauSPEMilliDiff_rlogl":  np.linspace(-2, 1, 11),
            "TauMonoMilliDiff_rlogl": np.linspace(-1.5, 0.2, 11),
        },
        "dim_info": {
            "TauSPEMilliDiff_rlogl":  {"log_x": False, "log_y": True, "x_label": "Tau-SPE Milli rlogl",  "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "TauMonoMilliDiff_rlogl": {"log_x": False, "log_y": True, "x_label": "Tau-Mono Milli rlogl", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_evtgen_recoeratio_zoom",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "EventGenerator Length vs E Ratio Zoom — No Systematics",
        "scans": [("{model}_NoSystematics_evtgen_recoeratio_zoom", "MC")],
        "binning": {
            "EventGeneratorDC_Thijs_length":   np.geomspace(10**0, 10**3, 11),
            "RecoERatio_EventGeneratorDC_Max": np.linspace(-1.1000, 1.0984, 11),
        },
        "dim_info": {
            "EventGeneratorDC_Thijs_length":   {"log_x": True,  "log_y": True, "x_label": "EventGen Length", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "RecoERatio_EventGeneratorDC_Max": {"log_x": False, "log_y": True, "x_label": "EvtGen E Ratio",  "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },

    # ---- Combined dataset — BDT variables, with systematics ----
    {
        "key": "combined_syst_bdt_scores",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "HESE Combined BDT Scores — With Systematics",
        "scans": [("{model}_bdt1_bdt2", "MC")],
        "binning": {
            "bdt_scores1": np.linspace(0.0, 1, 11),
            "bdt_scores2": np.linspace(0.0, 1, 11),
        },
        "dim_info": {
            "bdt_scores1": {"log_x": False, "log_y": True, "x_label": "BDT Score 1", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "bdt_scores2": {"log_x": False, "log_y": True, "x_label": "BDT Score 2", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_syst_len_easym",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "Taupede Length vs Asymmetry — With Systematics",
        "scans": [("{model}_len_easym", "MC")],
        "binning": {
            "Taupede_Distance":  np.geomspace(10**0.1360, 10**3.0133, 11),
            "Taupede_Asymmetry": np.linspace(-1.001, 1.001, 11),
        },
        "dim_info": {
            "Taupede_Distance":  {"log_x": True,  "log_y": True, "x_label": "Taupede Length",    "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "Taupede_Asymmetry": {"log_x": False, "log_y": True, "x_label": "Taupede Asymmetry", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_syst_taumono_econf",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "TauMono rlogl vs Econfinement — With Systematics",
        "scans": [("{model}_taumono_econf", "MC")],
        "binning": {
            "TauMonoDiff_rlogl": np.linspace(-8.8396, 0.4251, 11),
            "econfinement":      np.linspace(-0.001, 1.001, 11),
        },
        "dim_info": {
            "TauMonoDiff_rlogl": {"log_x": False, "log_y": True, "x_label": "Tau-Mono rlogl", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "econfinement":      {"log_x": False, "log_y": True, "x_label": "Econfinement",   "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_syst_vtxdist_qtot",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "Vertex Reco Dist vs Qtot HLC — With Systematics",
        "scans": [("{model}_vtxdist_qtot", "MC")],
        "binning": {
            "cscdSBU_VertexRecoDist_CscdLLh": np.linspace(-18.1670, 462.2055, 11),
            "cscdSBU_Qtot_HLC_log":           np.linspace(3.7310, 5.5967, 11),
        },
        "dim_info": {
            "cscdSBU_VertexRecoDist_CscdLLh": {"log_x": False, "log_y": True, "x_label": "Vertex Reco Dist Cscd", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "cscdSBU_Qtot_HLC_log":           {"log_x": False, "log_y": True, "x_label": "log10(Qtot HLC)",       "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_syst_evtgen_recoeratio",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "EventGenerator Length vs E Ratio — With Systematics",
        "scans": [("{model}_evtgen_recoeratio", "MC")],
        "binning": {
            "EventGeneratorDC_Thijs_length":   np.linspace(-446.7254, 838.6997, 11),
            "RecoERatio_EventGeneratorDC_Max": np.linspace(-1.1000, 1.0984, 11),
        },
        "dim_info": {
            "EventGeneratorDC_Thijs_length":   {"log_x": False, "log_y": True, "x_label": "EventGen Length", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "RecoERatio_EventGeneratorDC_Max": {"log_x": False, "log_y": True, "x_label": "EvtGen E Ratio",  "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_syst_tauspe_taumilli",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "TauSPE vs TauMono Milli rlogl — With Systematics",
        "scans": [("{model}_tauspe_taumilli", "MC")],
        "binning": {
            "TauSPEMilliDiff_rlogl":  np.linspace(-7.0223, 1.1643, 11),
            "TauMonoMilliDiff_rlogl": np.linspace(-4.5702, 0.2189, 11),
        },
        "dim_info": {
            "TauSPEMilliDiff_rlogl":  {"log_x": False, "log_y": True, "x_label": "Tau-SPE Milli rlogl",  "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "TauMonoMilliDiff_rlogl": {"log_x": False, "log_y": True, "x_label": "Tau-Mono Milli rlogl", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_syst_mono_energy_zenith",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "MonopodFit Energy vs Zenith — With Systematics",
        "scans": [("{model}_mono_energy_zenith", "MC")],
        "binning": {
            "MonopodFit_iMIGRAD_PPB0_energy":  np.geomspace(10**4.4758, 10**8.2502, 11),
            "cscdSBU_MonopodFit4_noDC_zenith": np.linspace(0.0317, 3.1400, 11),
        },
        "dim_info": {
            "MonopodFit_iMIGRAD_PPB0_energy":  {"log_x": True,  "log_y": True, "x_label": "MonopodFit Energy", "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e2)},
            "cscdSBU_MonopodFit4_noDC_zenith": {"log_x": False, "log_y": True, "x_label": "Monopod Zenith",    "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_syst_mono_delay_qmax",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "MonopodFit Delay vs Q Max DOMs — With Systematics",
        "scans": [("{model}_mono_delay_qmax", "MC")],
        "binning": {
            "MonopodFit_iMIGRAD_PPB0_Delay_ice": np.linspace(-15011.9669, 1120.3790, 11),
            "CVStatistics_q_max_doms":            np.linspace(-712.6985, 22417.2985, 11),
        },
        "dim_info": {
            "MonopodFit_iMIGRAD_PPB0_Delay_ice": {"log_x": False, "log_y": True, "x_label": "Delay Ice",  "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "CVStatistics_q_max_doms":            {"log_x": False, "log_y": True, "x_label": "Q Max DOMs", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_syst_e1_e2",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "Taupede Particle Energies — With Systematics",
        "scans": [("{model}_e1_e2", "MC")],
        "binning": {
            "Taupede1_Particles_energy": np.geomspace(10**1.9875, 10**10.3972, 11),
            "Taupede2_Particles_energy": np.geomspace(10**0.5207, 10**8.0231, 11),
        },
        "dim_info": {
            "Taupede1_Particles_energy": {"log_x": True, "log_y": True, "x_label": "Taupede Energy 1", "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e3)},
            "Taupede2_Particles_energy": {"log_x": True, "log_y": True, "x_label": "Taupede Energy 2", "sum_axes": 0, "flip": False, "ylim": (1e-2, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_syst_e1_e2_zoom",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "Taupede Particle Energies Zoom — With Systematics",
        "scans": [("{model}_e1_e2_zoom", "MC")],
        "binning": {
            "Taupede1_Particles_energy": np.geomspace(10**2, 10**7, 11),
            "Taupede2_Particles_energy": np.geomspace(10**2, 10**7, 11),
        },
        "dim_info": {
            "Taupede1_Particles_energy": {"log_x": True, "log_y": True, "x_label": "Taupede Energy 1", "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e3)},
            "Taupede2_Particles_energy": {"log_x": True, "log_y": True, "x_label": "Taupede Energy 2", "sum_axes": 0, "flip": False, "ylim": (1e-2, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_syst_energy_length",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "HESE Combined Energy vs Length — With Systematics",
        "scans": [("{model}_energy_length_analysis", "MC")],
        "binning": {
            "reco_energy": np.geomspace(10**4.778, 10**7.1, 14),
            "reco_length": np.geomspace(10**1, 10**3, 11),
        },
        "dim_info": {
            "reco_energy": {"log_x": True, "log_y": True, "x_label": r"$E_{\mathrm{reco}}$ [GeV]", "sum_axes": 1, "flip": False, "ylim": (1e-2, 1e2)},
            "reco_length": {"log_x": True, "log_y": True, "x_label": r"$L_{\tau}$ [m]",            "sum_axes": 0, "flip": False, "ylim": (1e-2, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_syst_mono_delay_qmax_zoom",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "MonopodFit Delay vs Q Max DOMs Zoom — With Systematics",
        "scans": [("{model}_mono_delay_qmax_zoom", "MC")],
        "binning": {
            "MonopodFit_iMIGRAD_PPB0_Delay_ice": np.linspace(-2000, 1000, 11),
            "CVStatistics_q_max_doms":            np.linspace(0, 10000, 11),
        },
        "dim_info": {
            "MonopodFit_iMIGRAD_PPB0_Delay_ice": {"log_x": False, "log_y": True, "x_label": "Delay Ice",  "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "CVStatistics_q_max_doms":            {"log_x": False, "log_y": True, "x_label": "Q Max DOMs", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_syst_vtxdist_qtot_zoom",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "Vertex Reco Dist vs Qtot HLC Zoom — With Systematics",
        "scans": [("{model}_vtxdist_qtot_zoom", "MC")],
        "binning": {
            "cscdSBU_VertexRecoDist_CscdLLh": np.linspace(0, 150, 11),
            "cscdSBU_Qtot_HLC_log":           np.linspace(3.7310, 5.5967, 11),
        },
        "dim_info": {
            "cscdSBU_VertexRecoDist_CscdLLh": {"log_x": False, "log_y": True, "x_label": "Vertex Reco Dist Cscd", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "cscdSBU_Qtot_HLC_log":           {"log_x": False, "log_y": True, "x_label": "log10(Qtot HLC)",       "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_syst_taumono_econf_zoom",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "TauMono rlogl vs Econfinement Zoom — With Systematics",
        "scans": [("{model}_taumono_econf_zoom", "MC")],
        "binning": {
            "TauMonoDiff_rlogl": np.linspace(-2.5, 0.2, 11),
            "econfinement":      np.linspace(0.75, 1.0010, 11),
        },
        "dim_info": {
            "TauMonoDiff_rlogl": {"log_x": False, "log_y": True, "x_label": "Tau-Mono rlogl", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "econfinement":      {"log_x": False, "log_y": True, "x_label": "Econfinement",   "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_syst_tauspe_taumilli_zoom",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "TauSPE vs TauMono Milli rlogl Zoom — With Systematics",
        "scans": [("{model}_tauspe_taumilli_zoom", "MC")],
        "binning": {
            "TauSPEMilliDiff_rlogl":  np.linspace(-2, 1, 11),
            "TauMonoMilliDiff_rlogl": np.linspace(-1.5, 0.2, 11),
        },
        "dim_info": {
            "TauSPEMilliDiff_rlogl":  {"log_x": False, "log_y": True, "x_label": "Tau-SPE Milli rlogl",  "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "TauMonoMilliDiff_rlogl": {"log_x": False, "log_y": True, "x_label": "Tau-Mono Milli rlogl", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "combined_syst_evtgen_recoeratio_zoom",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "EventGenerator Length vs E Ratio Zoom — With Systematics",
        "scans": [("{model}_evtgen_recoeratio_zoom", "MC")],
        "binning": {
            "EventGeneratorDC_Thijs_length":   np.geomspace(10**0, 10**3, 11),
            "RecoERatio_EventGeneratorDC_Max": np.linspace(-1.1000, 1.0984, 11),
        },
        "dim_info": {
            "EventGeneratorDC_Thijs_length":   {"log_x": True,  "log_y": True, "x_label": "EventGen Length", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "RecoERatio_EventGeneratorDC_Max": {"log_x": False, "log_y": True, "x_label": "EvtGen E Ratio",  "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },

    # ---- BDT scores: feature set comparison — no systematics ----
    {
        "key": "bdt_feature_nosyst_full",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "BDT Scores — 11feat+rlogl+econf+evtgen — No Systematics",
        "scans": [("{model}_NoSystematics_bdt1_bdt2_11features_plus_rloglmilli_econf_evtgen", "MC")],
        "binning": {
            "bdt_scores1": np.linspace(0.0, 1, 11),
            "bdt_scores2": np.linspace(0.0, 1, 11),
        },
        "dim_info": {
            "bdt_scores1": {"log_x": False, "log_y": True, "x_label": "BDT Score 1", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "bdt_scores2": {"log_x": False, "log_y": True, "x_label": "BDT Score 2", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "bdt_feature_nosyst_base",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "BDT Scores — 11feat (base) — No Systematics",
        "scans": [("{model}_NoSystematics_bdt1_bdt2_11features", "MC")],
        "binning": {
            "bdt_scores1": np.linspace(0.0, 1, 11),
            "bdt_scores2": np.linspace(0.0, 1, 11),
        },
        "dim_info": {
            "bdt_scores1": {"log_x": False, "log_y": True, "x_label": "BDT Score 1", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "bdt_scores2": {"log_x": False, "log_y": True, "x_label": "BDT Score 2", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "bdt_feature_nosyst_milli",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "BDT Scores — 11feat+rloglmilli — No Systematics",
        "scans": [("{model}_NoSystematics_bdt1_bdt2_11features_plus_rloglmilli", "MC")],
        "binning": {
            "bdt_scores1": np.linspace(0.0, 1, 11),
            "bdt_scores2": np.linspace(0.0, 1, 11),
        },
        "dim_info": {
            "bdt_scores1": {"log_x": False, "log_y": True, "x_label": "BDT Score 1", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "bdt_scores2": {"log_x": False, "log_y": True, "x_label": "BDT Score 2", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "bdt_feature_nosyst_econf",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "BDT Scores — 11feat+econf — No Systematics",
        "scans": [("{model}_NoSystematics_bdt1_bdt2_11features_plus_econf", "MC")],
        "binning": {
            "bdt_scores1": np.linspace(0.0, 1, 11),
            "bdt_scores2": np.linspace(0.0, 1, 11),
        },
        "dim_info": {
            "bdt_scores1": {"log_x": False, "log_y": True, "x_label": "BDT Score 1", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "bdt_scores2": {"log_x": False, "log_y": True, "x_label": "BDT Score 2", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "bdt_feature_nosyst_evtgen",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "BDT Scores — 11feat+evtgen — No Systematics",
        "scans": [("{model}_NoSystematics_bdt1_bdt2_11features_plus_evtgen", "MC")],
        "binning": {
            "bdt_scores1": np.linspace(0.0, 1, 11),
            "bdt_scores2": np.linspace(0.0, 1, 11),
        },
        "dim_info": {
            "bdt_scores1": {"log_x": False, "log_y": True, "x_label": "BDT Score 1", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "bdt_scores2": {"log_x": False, "log_y": True, "x_label": "BDT Score 2", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },

    # ---- BDT scores: feature set comparison — with systematics ----
    {
        "key": "bdt_feature_syst_full",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "BDT Scores — 11feat+rlogl+econf+evtgen — With Systematics",
        "scans": [("{model}_bdt1_bdt2_11features_plus_rloglmilli_econf_evtgen", "MC")],
        "binning": {
            "bdt_scores1": np.linspace(0.0, 1, 11),
            "bdt_scores2": np.linspace(0.0, 1, 11),
        },
        "dim_info": {
            "bdt_scores1": {"log_x": False, "log_y": True, "x_label": "BDT Score 1", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "bdt_scores2": {"log_x": False, "log_y": True, "x_label": "BDT Score 2", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "bdt_feature_syst_base",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "BDT Scores — 11feat (base) — With Systematics",
        "scans": [("{model}_bdt1_bdt2_11features", "MC")],
        "binning": {
            "bdt_scores1": np.linspace(0.0, 1, 11),
            "bdt_scores2": np.linspace(0.0, 1, 11),
        },
        "dim_info": {
            "bdt_scores1": {"log_x": False, "log_y": True, "x_label": "BDT Score 1", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "bdt_scores2": {"log_x": False, "log_y": True, "x_label": "BDT Score 2", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "bdt_feature_syst_milli",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "BDT Scores — 11feat+rloglmilli — With Systematics",
        "scans": [("{model}_bdt1_bdt2_11features_plus_rloglmilli", "MC")],
        "binning": {
            "bdt_scores1": np.linspace(0.0, 1, 11),
            "bdt_scores2": np.linspace(0.0, 1, 11),
        },
        "dim_info": {
            "bdt_scores1": {"log_x": False, "log_y": True, "x_label": "BDT Score 1", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "bdt_scores2": {"log_x": False, "log_y": True, "x_label": "BDT Score 2", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "bdt_feature_syst_econf",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "BDT Scores — 11feat+econf — With Systematics",
        "scans": [("{model}_bdt1_bdt2_11features_plus_econf", "MC")],
        "binning": {
            "bdt_scores1": np.linspace(0.0, 1, 11),
            "bdt_scores2": np.linspace(0.0, 1, 11),
        },
        "dim_info": {
            "bdt_scores1": {"log_x": False, "log_y": True, "x_label": "BDT Score 1", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "bdt_scores2": {"log_x": False, "log_y": True, "x_label": "BDT Score 2", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
    {
        "key": "bdt_feature_syst_evtgen",
        "det_config": "IC86_pass2_SnowStorm_FTP_HESE_Combined",
        "title": "BDT Scores — 11feat+evtgen — With Systematics",
        "scans": [("{model}_bdt1_bdt2_11features_plus_evtgen", "MC")],
        "binning": {
            "bdt_scores1": np.linspace(0.0, 1, 11),
            "bdt_scores2": np.linspace(0.0, 1, 11),
        },
        "dim_info": {
            "bdt_scores1": {"log_x": False, "log_y": True, "x_label": "BDT Score 1", "sum_axes": 1, "flip": False, "ylim": (1e-1, 1e3)},
            "bdt_scores2": {"log_x": False, "log_y": True, "x_label": "BDT Score 2", "sum_axes": 0, "flip": False, "ylim": (1e-1, 1e3)},
        },
        "show_counts": False, "plot_components": True,
    },
]


def get_plots(model):
    """Return the full PLOTS list with `{model}` substituted in all scan names."""
    import copy
    plots = []
    for tmpl in _PLOT_TEMPLATES:
        p = copy.deepcopy(tmpl)
        p["scans"] = [(s.replace("{model}", model), lbl) for s, lbl in p["scans"]]
        plots.append(p)
    return plots


# ---- Convenience key groups ----
GROUP_SEPARATE = ["cascades_syst", "tracks_syst", "dc_syst"]
GROUP_COMBINED_NOSYST = [
    "combined_bdt_scores", "combined_energy_length",
    "combined_len_easym",
    "combined_e1_e2", "combined_e1_e2_zoom",
    "combined_mono_energy_zenith",
    "combined_mono_delay_qmax", "combined_mono_delay_qmax_zoom",
    "combined_vtxdist_qtot", "combined_vtxdist_qtot_zoom",
    "combined_taumono_econf", "combined_taumono_econf_zoom",
    "combined_tauspe_taumilli", "combined_tauspe_taumilli_zoom",
    "combined_evtgen_recoeratio", "combined_evtgen_recoeratio_zoom",
]
GROUP_COMBINED_SYST = [
    "combined_syst_bdt_scores",
    "combined_syst_energy_length",
    "combined_syst_len_easym",
    "combined_syst_e1_e2", "combined_syst_e1_e2_zoom",
    "combined_syst_mono_energy_zenith",
    "combined_syst_mono_delay_qmax", "combined_syst_mono_delay_qmax_zoom",
    "combined_syst_vtxdist_qtot", "combined_syst_vtxdist_qtot_zoom",
    "combined_syst_taumono_econf", "combined_syst_taumono_econf_zoom",
    "combined_syst_tauspe_taumilli", "combined_syst_tauspe_taumilli_zoom",
    "combined_syst_evtgen_recoeratio", "combined_syst_evtgen_recoeratio_zoom",
]
GROUP_FEATURE_BDT = [
    "bdt_feature_nosyst_full", "bdt_feature_nosyst_base", "bdt_feature_nosyst_milli",
    "bdt_feature_nosyst_econf", "bdt_feature_nosyst_evtgen",
    "bdt_feature_syst_full", "bdt_feature_syst_base", "bdt_feature_syst_milli",
    "bdt_feature_syst_econf", "bdt_feature_syst_evtgen",
]
GROUP_ALL = GROUP_SEPARATE + GROUP_COMBINED_NOSYST + GROUP_COMBINED_SYST + GROUP_FEATURE_BDT
