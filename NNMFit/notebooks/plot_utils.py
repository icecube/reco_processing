import matplotlib.pyplot as plt
import numpy as np

x_labels = {
    "reco_energy" : r"Reco $E_{\rm dep}$ [GeV]",
    "reco_length" : r"Reco $L_{\tau}$ [m]",
    "reco_zenith" : r"Reco $\theta$ [rad]",
    "reco_dir" : r"Reco $\theta$ [rad]",
    "bdt_product" : "BDT score 1 x BDT score 2"
}

def plot_histogram(hist_graph_hdl, det_config, input_variables, ylog = None, savepath = None):

    print(det_config)
    binnings = hist_graph_hdl.get_binning(det_config=det_config)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    for input_name, input_variable in input_variables.items():

        res = hist_graph_hdl.get_evaled_histogram(input_variables=input_variable, det_config=det_config, reshape=True)

        for i, (variable_name, binning) in enumerate(binnings.items()):

            hist = res["mu"].sum(axis=1-i)
            yerror = np.sqrt(res["ssq"].sum(axis=1-i))

            bin_centers = 0.5 * (binning[:-1] + binning[1:])

            axes[i].stairs(hist, binning, label=f"{input_name}: {sum(hist):.2f}")
            axes[i].fill_between(binning, np.r_[hist - yerror, (hist - yerror)[-1]], np.r_[hist + yerror, (hist + yerror)[-1]], step="post", alpha=0.4)
            # axes[i].errorbar(bin_centers, hist, yerr=yerror, fmt="none", capsize=2)

            axes[i].set_xlabel(x_labels[variable_name])
            axes[i].set_ylabel(f"Rate / {hist_graph_hdl.get_livetime(det_config)/(3600*24*365.25):.2f} yr")

            axes[i].set_xlim(min(binning), max(binning))

            axes[i].set_yscale("log") if ylog else 0
            if "energy" in variable_name or "length" in variable_name: axes[i].set_xscale("log")
            if not i: axes[i].legend()

    plt.suptitle(det_config)
    plt.tight_layout()
    if savepath: plt.savefig(savepath)
    plt.show()

def plot_histogram_astro_flavor(hist_graph_hdl, det_config, gamma_astro = 2.87, astro_norm = 2.1233, ylog = None, savepath = None):

    print(det_config)
    binnings = hist_graph_hdl.get_binning(det_config=det_config)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # calculate astro contributions per flavor
    res_flavor = {
        "NuMu" : hist_graph_hdl.get_evaled_histogram(input_variables={"astro_norm" : astro_norm, "gamma_astro" : gamma_astro,"prompt_norm" : 0, "conv_norm" : 0, "astro_nue_ratio" : 0, "astro_nutau_ratio" : 0}, det_config=det_config, reshape=True),
        "NuMu+NuE" : hist_graph_hdl.get_evaled_histogram(input_variables={"astro_norm" : astro_norm, "gamma_astro" : gamma_astro, "prompt_norm" : 0, "conv_norm" : 0, "astro_nue_ratio" : 1, "astro_nutau_ratio" : 0}, det_config=det_config, reshape=True),
        "NuMu+NuTau" : hist_graph_hdl.get_evaled_histogram(input_variables={"astro_norm" : astro_norm, "gamma_astro" : gamma_astro, "prompt_norm" : 0, "conv_norm" : 0, "astro_nue_ratio" : 0, "astro_nutau_ratio" : 1}, det_config=det_config, reshape=True),
    }
    hists = {
        "NuE" : res_flavor["NuMu+NuE"]["mu"] - res_flavor["NuMu"]["mu"],
        "NuMu" : res_flavor["NuMu"]["mu"],
        "NuTau" : res_flavor["NuMu+NuTau"]["mu"] - res_flavor["NuMu"]["mu"],
    }

    for input_flavor, hist in hists.items():

        for i, (variable_name, binning) in enumerate(binnings.items()):

            hist = hists[input_flavor].sum(axis=1-i)
            # yerror = np.sqrt(res["ssq"].sum(axis=1-i))

            axes[i].stairs(hist, binning, label=f"{input_flavor}: {sum(hist):.2f}")
            # axes[i].fill_between(binning, np.r_[hist - yerror, (hist - yerror)[-1]], np.r_[hist + yerror, (hist + yerror)[-1]], step="post", alpha=0.4)

            axes[i].set_xlabel(x_labels[variable_name])
            axes[i].set_ylabel(f"Rate / {hist_graph_hdl.get_livetime(det_config)/(3600*24*365.25):.2f} yr")

            axes[i].set_xlim(min(binning), max(binning))

            axes[i].set_yscale("log") if ylog else 0
            if "energy" in variable_name or "length" in variable_name: axes[i].set_xscale("log")
            if not i: axes[i].legend()

    plt.suptitle(det_config)
    plt.tight_layout()
    if savepath: plt.savefig(savepath)
    plt.show()