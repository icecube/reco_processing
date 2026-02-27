

dag_path       = "/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/dag_scans/flavor_globalfit"
hese_path      = f"{dag_path}/hese"
globalfit_path = f"{dag_path}/globalfit"
combined_path  = f"{dag_path}/globalfit_hese"

scan_dir_dict = {
    # --- benchmark ---
    "spice_nosyst":           f"{hese_path}/asimov_SAY_HESEBestfit_NoSystematics_spice",
    "hese_oldpid_nosyst":     f"{hese_path}/asimov_SAY_HESEBestfit_NoSystematics_ftp_FinalTopology",

    # --- Old PID with systematics ---
    "hese_oldpid":            f"{hese_path}/asimov_SAY_HESEBestfit_ftp_FinalTopology",

    "hese_oldpid_combinedBase":  
                              f"{hese_path}/asimov_SAY_HESEBestfit_ftp_FinalTopology_combinedBaseline",

    # # --- 11 feature variants, optimized for different bdt trainings or figures of merit ---
    # "hese_11feat_purity":     f"{hese_path}/mcd-flavor_flux-hese_feat-11features/"
    #                           f"bdt1_0.21_bdt2_0.55_length_10",

    # "hese_11feat_fisher":     f"{hese_path}/mcd-flavor_flux-hese_feat-11features/"
    #                           f"bdt1_0.366667_bdt2_0.433333_length_10",

    # "hese_11feat_simple":     f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features/"
    #                           f"bdt1_0.366667_bdt2_0.433333_length_10",

    # # --- All features (old configs, not yet optimized) ---
    # "hese_allfeat_old":       f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features_plus_"
    #                           f"rloglmilli_econf_evtgen/bdt1_0.4_bdt2_0.45_length_10",

    # "hese_allfeat_bdtprod_old": f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features_plus_"
    #                             f"rloglmilli_econf_evtgen/"
    #                             f"bdt1_0.3_bdt2_0.4_length_10_10bdtprod_threshold_0.12",

    # # --- trying smaller length teaser ---
    # "hese_allfeat_len6":      f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features_plus_"
    #                           f"rloglmilli_econf_evtgen/bdt1_0.4_bdt2_0.45_length_6.31",

    # "hese_allfeat_len8":      f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features_plus_"
    #                           f"rloglmilli_econf_evtgen/bdt1_0.4_bdt2_0.45_length_8",

    # # --- All features (current configs) ---
    # "hese_allfeat":           f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features_plus_"
    #                           f"rloglmilli_econf_evtgen/bdt1_0.366667_bdt2_0.5_length_10",

    # "hese_allfeat_bdtprod":   f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features_plus_"
    #                           f"rloglmilli_econf_evtgen/"
    #                           f"bdt1_0.333333_bdt2_0.366667_length_10_10bdtprod_threshold_0.122",

    "hese_allfeat_bdtprod_combinedBase":
                              f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features_plus_"
                              f"rloglmilli_econf_evtgen/"
                              f"bdt1_0.333333_bdt2_0.366667_length_10_"
                              f"10bdtprod_threshold_0.122_combinedBaseline",

    "hese_allfeat_bdtprod_combinedBase_withSyst":
                              f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features_plus_"
                              f"rloglmilli_econf_evtgen/"
                              f"bdt1_0.333333_bdt2_0.366667_length_10_"
                              f"10bdtprod_threshold_0.122_combinedBaseline_withSyst",

    # --- Adding the muon template ---
    "hese_allfeat_bdtprod_combinedBase_NehaMuon":
                              f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features_plus_"
                              f"rloglmilli_econf_evtgen/"
                              f"bdt1_0.333333_bdt2_0.366667_length_10_"
                              f"10bdtprod_threshold_0.122_combinedBaseline_NehaMuon",

    "hese_allfeat_bdtprod_combinedBase_reproduceNehaMuon":
                              f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features_plus_"
                              f"rloglmilli_econf_evtgen/"
                              f"bdt1_0.333333_bdt2_0.366667_length_10_"
                              f"10bdtprod_threshold_0.122_combinedBaseline_reproduceNehaMuon",
    
    "hese_allfeat_bdtprod_combinedBase_Muon":
                              f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features_plus_"
                              f"rloglmilli_econf_evtgen/"
                              f"bdt1_0.333333_bdt2_0.366667_length_10_"
                              f"10bdtprod_threshold_0.122_combinedBaseline_Muon",

    # --- New flavor parametrization ---
    "hese_allfeat_bdtprod_combinedBase_newflavorparam":
                              f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features_plus_"
                              f"rloglmilli_econf_evtgen/"
                              f"bdt1_0.333333_bdt2_0.366667_length_10_"
                              f"10bdtprod_threshold_0.122_combinedBaseline_newflavorparam",

    # --- BPL ---
    "hese_allfeat_bdtprod_combinedBase_newflavorparam_BPL":
                              f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features_plus_"
                              f"rloglmilli_econf_evtgen/"
                              f"bdt1_0.333333_bdt2_0.366667_length_10_"
                              f"10bdtprod_threshold_0.122_BPL",

    # --- minuit minimizer ---
    "hese_allfeat_bdtprod_combinedBase_minuit":
                              f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features_plus_"
                              f"rloglmilli_econf_evtgen/"
                              f"bdt1_0.333333_bdt2_0.366667_length_10_"
                              f"10bdtprod_threshold_0.122_combinedBaseline_minuit",

    "hese_allfeat_bdtprod_combinedBase_withSyst_minuit":
                              f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features_plus_"
                              f"rloglmilli_econf_evtgen/"
                              f"bdt1_0.333333_bdt2_0.366667_length_10_"
                              f"10bdtprod_threshold_0.122_combinedBaseline_withSyst_minuit",

    # # --- Global fits ---
    # "gf_zheyang":             f"{globalfit_path}/asimov_SAY_globalfit_zheyang",
    # "gf_v0":                  f"{globalfit_path}/asimov_SAY_globalfit_datasets_22612_22644_train_zheyang_bdt1_0.45_bdt2_0.67",
    # "gf_v0_noHESE":           f"{globalfit_path}/asimov_SAY_globalfit_datasets_22612_22644_train_zheyang_bdt1_0.45_bdt2_0.67_noHESE",

    # # --- Combined globalfit HESE
    # "gfh_fluxh_woverlap" :    f"{combined_path}/asimov_SAY_globalfit_hese_flux-hese",
    # "gfh_fluxg_woverlap" :    f"{combined_path}/asimov_SAY_globalfit_hese_flux-globalfit",

    # "gfh_fluxh" :             f"{combined_path}/asimov_SAY_globalfit_hese_flux-hese_22612_22644_train_zheyang_bdt1_0.45_bdt2_0.67_noHESE",
    # "gfh_fluxg" :             f"{combined_path}/asimov_SAY_globalfit_hese_flux-globalfit_22612_22644_train_zheyang_bdt1_0.45_bdt2_0.67_noHESE",

}
