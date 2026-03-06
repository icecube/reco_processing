

dag_path       = "/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/dag_scans/flavor_globalfit"
hese_path      = f"{dag_path}/hese/first_try"
globalfit_path = f"{dag_path}/globalfit/debug_minimizer"
globalfit_hese_path = f"{dag_path}/globalfit_hese"

scan_dir_dict = {
    # --- benchmark ---
    "spice_nosyst":           f"{hese_path}/asimov_SAY_HESEBestfit_NoSystematics_spice",
    "hese_oldpid_nosyst":     f"{hese_path}/asimov_SAY_HESEBestfit_NoSystematics_ftp_FinalTopology",

    # --- checks ---
    "globalfit_double_SPL_LBFGSB":           f"{globalfit_path}/globalfit_double_SPL_LBFGSB",
    "globalfit_double_SPL_minuit":           f"{globalfit_path}/globalfit_double_SPL_minuit",
    "globalfit_double_SPL_minuit_philipp":           f"{globalfit_path}/globalfit_double_SPL_minuit_philipp",

    "globalfit_double_no_hybrid_muon_SPL_LBFGSB":           f"{globalfit_path}/globalfit_double_no_hybrid_muon_SPL_LBFGSB",
    "globalfit_double_no_hybrid_muon_SPL_minuit":           f"{globalfit_path}/globalfit_double_no_hybrid_muon_SPL_minuit",
    "globalfit_double_no_hybrid_muon_SPL_minuit_philipp":           f"{globalfit_path}/globalfit_double_no_hybrid_muon_SPL_minuit_philipp",

    "globalfit_double_no_hybrid_muon_SPL_LBFGSB_Poisson":           f"{globalfit_path}/globalfit_double_no_hybrid_muon_SPL_LBFGSB_Poisson",
    "globalfit_double_no_hybrid_muon_SPL_minuit_Poisson":           f"{globalfit_path}/globalfit_double_no_hybrid_muon_SPL_minuit_Poisson",
    "globalfit_double_no_hybrid_muon_SPL_minuit_philipp_Poisson":           f"{globalfit_path}/globalfit_double_no_hybrid_muon_SPL_minuit_philipp_Poisson",

    "globalfit_double_SPL_3flavor_LBFGSB":           f"{globalfit_path}/globalfit_double_SPL_3flavor_LBFGSB",
    "globalfit_double_no_hybrid_muon_SPL_3flavor_LBFGSB":           f"{globalfit_path}/globalfit_double_no_hybrid_muon_SPL_3flavor_LBFGSB",
    "globalfit_double_no_hybrid_muon_SPL_3flavor_LBFGSB_Poisson":           f"{globalfit_path}/globalfit_double_no_hybrid_muon_SPL_3flavor_LBFGSB_Poisson",

    "globalfit_double_no_hybrid_muon_BPL_LBFGSB":           f"{globalfit_path}/globalfit_double_no_hybrid_muon_BPL_LBFGSB",
    "globalfit_double_no_hybrid_muon_BPL_3flavor_LBFGSB":           f"{globalfit_path}/globalfit_double_no_hybrid_muon_BPL_3flavor_LBFGSB",
    "globalfit_double_BPL_LBFGSB":           f"{globalfit_path}/globalfit_double_BPL_LBFGSB",

    "globalfit_double_SPL_LBFGSB_Poisson":           f"{globalfit_path}/globalfit_double_SPL_LBFGSB_Poisson",
    "globalfit_double_nohese_SPL_LBFGSB_Poisson":           f"{globalfit_path}/globalfit_double_nohese_SPL_LBFGSB_Poisson",
    "globalfit_double_nohese_BPL_LBFGSB_Poisson":           f"{globalfit_path}/globalfit_double_nohese_BPL_LBFGSB_Poisson",

    "globalfit_double_no_hybrid_muon_BPL_range_philipp_LBFGSB":           f"{globalfit_path}/globalfit_double_no_hybrid_muon_BPL_range_philipp_LBFGSB",
    "globalfit_double_no_hybrid_muon_BPL_range_philipp_strict_LBFGSB":           f"{globalfit_path}/globalfit_double_no_hybrid_muon_BPL_range_philipp_strict_LBFGSB",


    # --- gbf ---
    "globalfit_double_hese_SPL":           f"{globalfit_hese_path}/globalfit_double_hese_SPL",
    "globalfit_double_hese_BPL":           f"{globalfit_hese_path}/globalfit_double_hese_BPL",

    # --- gbf ---
    "hese_allfeat_bdtprod_combinedBase_Muon":
                              f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features_plus_"
                              f"rloglmilli_econf_evtgen/"
                              f"bdt1_0.333333_bdt2_0.366667_length_10_"
                              f"10bdtprod_threshold_0.122_combinedBaseline_Muon",

    "spice_nosyst":           f"{hese_path}/asimov_SAY_HESEBestfit_NoSystematics_spice",


}
