
bins_settings = {}

# traditional binning
bins_settings["13logE_10logL"] = { # 130 bins
    "<BINS>" : """- ["log10_reco_energy", "linear", [4.778, 7.1, 14]]
        - ["log10_reco_length", "linear", [1, 3, 11]]"""
}

bins_settings["10logE_10logL"] = { # 100 bins
    "<BINS>" : """- ["log10_reco_energy", "linear", [4.778, 7.1, 11]]
        - ["log10_reco_length", "linear", [1, 3, 11]]"""
}

# 3D binning
bins_settings["13logE_4bdt1_4bdt2"] = { # 208 bins
    "<BINS>" : """- ["log10_reco_energy", "linear", [4.778, 7.1, 14]]
        - ["bdt_scores1", "linear", [<BDT1_THRESHOLD>, 1, 5]]
        - ["bdt_scores2", "linear", [<BDT2_THRESHOLD>, 1, 5]]"""
}

bins_settings["8logE_5bdt1_5bdt2"] = { # 200 bins
    "<BINS>" : """- ["log10_reco_energy", "linear", [4.778, 7.1, 9]]
        - ["bdt_scores1", "linear", [<BDT1_THRESHOLD>, 1, 6]]
        - ["bdt_scores2", "linear", [<BDT2_THRESHOLD>, 1, 6]]"""
}

bins_settings["5logE_5bdt1_5bdt2"] = { # 208 bins
    "<BINS>" : """- ["log10_reco_energy", "linear", [4.778, 7.1, 6]]
        - ["bdt_scores1", "linear", [<BDT1_THRESHOLD>, 1, 6]]
        - ["bdt_scores2", "linear", [<BDT2_THRESHOLD>, 1, 6]]"""
}

# 2D with bdt product
bins_settings["13logE_10bdtprod"] = { # 130 bins
    "<BINS>" : """- ["log10_reco_energy", "linear", [4.778, 7.1, 14]]
        - ["bdt_product", "linear", [<BDTPRODUCT_THRESHOLD>, 1, 11]]"""
}

bins_settings["10logE_10bdtprod"] = { # 100 bins
    "<BINS>" : """- ["log10_reco_energy", "linear", [4.778, 7.1, 11]]
        - ["bdt_product", "linear", [<BDTPRODUCT_THRESHOLD>, 1, 11]]"""
}

bins_settings["10logE_20bdtprod"] = { # 200 bins
    "<BINS>" : """- ["log10_reco_energy", "linear", [4.778, 7.1, 11]]
        - ["bdt_product", "linear", [<BDTPRODUCT_THRESHOLD>, 1, 21]]"""
}

