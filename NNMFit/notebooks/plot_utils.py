import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

x_labels = {
    "reco_energy" : r"Reco $E_{\rm dep}$ [GeV]",
    "reco_length" : r"Reco $L_{\tau}$ [m]",
    "reco_zenith" : r"Reco $\theta$ [rad]",
    "reco_dir" : r"Reco $\theta$ [rad]",
    "bdt_product" : "BDT score 1 x BDT score 2"
}

def plot_histogram_2D(hist_graph_hdl, det_config, input_variable, ax=None, title=None,savepath=None):

    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 4))
    else:
        fig = ax.figure

    binnings = hist_graph_hdl.get_binning(det_config=det_config)
    var_names = list(binnings.keys())
    x_var, y_var = var_names
    x_bins, y_bins = binnings[x_var], binnings[y_var]

    res = hist_graph_hdl.get_evaled_histogram(input_variables=input_variable, det_config=det_config, reshape=True)
    hist = res["mu"]
    livetime = hist_graph_hdl.get_livetime(det_config)/(3600*24*365.25)

    data = hist.T / livetime
    # data = np.ma.masked_where(data == 0, data)
    # data[data == 0] = np.nan

    cmap = plt.cm.viridis.copy()
    cmap.set_bad("white")

    mesh = ax.pcolormesh(x_bins, y_bins, data, shading="auto", cmap=cmap)

    ax.set_xlabel(x_labels[x_var])
    ax.set_ylabel(x_labels[y_var])
    ax.set_xlim(min(x_bins), max(x_bins))
    ax.set_ylim(min(y_bins), max(y_bins))
    if "energy" in x_var or "length" in x_var: ax.set_xscale("log")
    if "energy" in y_var or "length" in y_var: ax.set_yscale("log")



    cbar = plt.colorbar(mesh, ax=ax)
    cbar.set_label(f"Rate / {livetime:.2f} yr")

    ax.set_title(det_config) if not title else ax.set_title(title)
    if savepath: 
        plt.tight_layout()
        plt.savefig(savepath)
        plt.show()

def plot_2d_ssq_and_relerr(hist_graph_hdl, det_config, input_variable, zlog=None, title = None, savepath=None):

    print(det_config)
    binnings = hist_graph_hdl.get_binning(det_config=det_config)
    var_names = list(binnings.keys())
    x_var, y_var = var_names
    x_bins, y_bins = binnings[x_var], binnings[y_var]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    res = hist_graph_hdl.get_evaled_histogram(input_variables=input_variable, det_config=det_config, reshape=True)

    ssq = res["ssq"]
    mu = res["mu"]
    relerr = np.sqrt(ssq)/mu

    m0 = axes[0].pcolormesh(x_bins, y_bins, ssq.T, shading="auto", norm=plt.LogNorm() if zlog else None)
    m1 = axes[1].pcolormesh(x_bins, y_bins, relerr.T, shading="auto", norm=plt.LogNorm() if zlog else None)

    for ax in axes:
        ax.set_xlabel(x_labels[x_var])
        ax.set_ylabel(x_labels[y_var])
        ax.set_xlim(min(x_bins), max(x_bins))
        ax.set_ylim(min(y_bins), max(y_bins))
        if "energy" in x_var or "length" in x_var: ax.set_xscale("log")
        if "energy" in y_var or "length" in y_var: ax.set_yscale("log")

    plt.colorbar(m0, ax=axes[0], label="ssq")
    plt.colorbar(m1, ax=axes[1], label=r"$\sqrt{\mathrm{ssq}}/\mu$")

    plt.suptitle(det_config) if not title else plt.suptitle(title)
    plt.tight_layout()
    if savepath: plt.savefig(savepath)
    plt.show()

def plot_2d_relerr(hist_graph_hdl, det_config, input_variable, zlog=None, title = None, savepath=None):

    print(det_config)
    binnings = hist_graph_hdl.get_binning(det_config=det_config)
    var_names = list(binnings.keys())
    x_var, y_var = var_names
    x_bins, y_bins = binnings[x_var], binnings[y_var]

    fig, ax = plt.subplots(1, 1, figsize=(12, 10))

    res = hist_graph_hdl.get_evaled_histogram(input_variables=input_variable, det_config=det_config, reshape=True)

    relerr = np.sqrt(res["ssq"])/res["mu"]

    m = ax.pcolormesh(x_bins, y_bins, relerr.T, shading="auto", norm=plt.LogNorm() if zlog else None)

    ax.set_xlabel(x_labels[x_var], fontsize=14)
    ax.set_ylabel(x_labels[y_var], fontsize=14)
    ax.set_xlim(min(x_bins), max(x_bins))
    ax.set_ylim(min(y_bins), max(y_bins))
    if "energy" in x_var or "length" in x_var: ax.set_xscale("log")
    if "energy" in y_var or "length" in y_var: ax.set_yscale("log")

    x_centers = 0.5*(x_bins[:-1] + x_bins[1:])
    y_centers = 0.5*(y_bins[:-1] + y_bins[1:])
    for ix, x in enumerate(x_centers):
        for iy, y in enumerate(y_centers):
            if np.isfinite(relerr[ix, iy]):
                ax.text(x, y, f"{relerr[ix, iy]:.2g}", ha="center", va="center", color="white", fontsize=8.5)

    nbins_empty = np.sum( res["mu"] == 0 )
    nbins_10perc = np.sum((relerr > 0.1) & (res["mu"] > 0))

    # cbar = plt.colorbar(m, ax=ax, label=r"$\sqrt{\mathrm{ssq}}/\mu$")
    cbar = plt.colorbar(m, ax=ax)
    cbar.set_label(r"$\sqrt{\mathrm{ssq}}/\mu$", fontsize=14)

    plt.suptitle(f"{det_config}, {nbins_empty} empty bins, {nbins_10perc} / {res['mu'].size} bins > 10%") if not title else plt.suptitle(f"{title}, {nbins_empty} empty bins, {nbins_10perc} / {res['mu'].size} bins > 10%")
    plt.tight_layout()
    if savepath: plt.savefig(savepath)
    plt.show()




def plot_histogram(hist_graph_hdl, det_config, input_variables, ylog = None, title = None, savepath = None):

    print(det_config)
    binnings = hist_graph_hdl.get_binning(det_config=det_config)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    for input_name, input_variable in input_variables.items():

        res = hist_graph_hdl.get_evaled_histogram(input_variables=input_variable, det_config=det_config, reshape=True)

        for i, (variable_name, binning) in enumerate(binnings.items()):

            hist = res["mu"].sum(axis=1-i)
            yerror = np.sqrt(res["ssq"].sum(axis=1-i))

            bin_centers = 0.5 * (binning[:-1] + binning[1:])

            axes[i].stairs(hist, binning, label=f"{input_name}: {sum(hist):.2f}+-{sum(yerror):.2f}")
            axes[i].fill_between(binning, np.r_[hist - yerror, (hist - yerror)[-1]], np.r_[hist + yerror, (hist + yerror)[-1]], step="post", alpha=0.4)
            # axes[i].errorbar(bin_centers, hist, yerr=yerror, fmt="none", capsize=2)

            axes[i].set_xlabel(x_labels[variable_name])
            axes[i].set_ylabel(f"Rate / {hist_graph_hdl.get_livetime(det_config)/(3600*24*365.25):.2f} yr")

            axes[i].set_xlim(min(binning), max(binning))

            axes[i].set_yscale("log") if ylog else 0
            if "energy" in variable_name or "length" in variable_name: axes[i].set_xscale("log")
            if not i: axes[i].legend()

    plt.suptitle(det_config) if not title else plt.suptitle(title)
    plt.tight_layout()
    if savepath: plt.savefig(savepath)
    plt.show()

# def plot_histogram_astro_flavor(hist_graph_hdl, det_config, gamma_astro = 2.87, astro_norm = 2.1233, ylog = None, title = None,savepath = None):

#     print(det_config)
#     binnings = hist_graph_hdl.get_binning(det_config=det_config)

#     fig, axes = plt.subplots(1, 2, figsize=(10, 4))

#     # calculate astro contributions per flavor
#     res_flavor = {
#         "NuMu" : hist_graph_hdl.get_evaled_histogram(input_variables={"astro_norm" : astro_norm, "gamma_astro" : gamma_astro,"prompt_norm" : 0, "conv_norm" : 0, "astro_nue_ratio" : 0, "astro_nutau_ratio" : 0}, det_config=det_config, reshape=True),
#         "NuMu+NuE" : hist_graph_hdl.get_evaled_histogram(input_variables={"astro_norm" : astro_norm, "gamma_astro" : gamma_astro, "prompt_norm" : 0, "conv_norm" : 0, "astro_nue_ratio" : 1, "astro_nutau_ratio" : 0}, det_config=det_config, reshape=True),
#         "NuMu+NuTau" : hist_graph_hdl.get_evaled_histogram(input_variables={"astro_norm" : astro_norm, "gamma_astro" : gamma_astro, "prompt_norm" : 0, "conv_norm" : 0, "astro_nue_ratio" : 0, "astro_nutau_ratio" : 1}, det_config=det_config, reshape=True),
#         "NuMu+NuE+NuTau" : hist_graph_hdl.get_evaled_histogram(input_variables={"astro_norm" : astro_norm, "gamma_astro" : gamma_astro, "prompt_norm" : 0, "conv_norm" : 0, "astro_nue_ratio" : 1, "astro_nutau_ratio" : 1}, det_config=det_config, reshape=True),
#     }
#     hists = {
#         "NuE" : res_flavor["NuMu+NuE"]["mu"] - res_flavor["NuMu"]["mu"],
#         "NuMu" : res_flavor["NuMu"]["mu"],
#         "NuTau" : res_flavor["NuMu+NuTau"]["mu"] - res_flavor["NuMu"]["mu"],
#         # "All" : res_flavor["NuMu+NuE+NuTau"]["mu"],
#     }
#     errors = {
#         "NuE" : res_flavor["NuMu+NuE"]["ssq"] - res_flavor["NuMu"]["ssq"],
#         "NuMu" : res_flavor["NuMu"]["ssq"],
#         "NuTau" : res_flavor["NuMu+NuTau"]["ssq"] - res_flavor["NuMu"]["ssq"],
#         # "All" : res_flavor["NuMu+NuE+NuTau"]["ssq"],
#     }

#     for input_flavor, hist in hists.items():

#         for i, (variable_name, binning) in enumerate(binnings.items()):

#             hist = hists[input_flavor].sum(axis=1-i)
#             yerror = np.sqrt(errors[input_flavor].sum(axis=1-i))

#             axes[i].stairs(hist, binning, label=f"{input_flavor}: {sum(hist):.2f}+-{sum(yerror):.2f}")
#             axes[i].fill_between(binning, np.r_[hist - yerror, (hist - yerror)[-1]], np.r_[hist + yerror, (hist + yerror)[-1]], step="post", alpha=0.4)

#             axes[i].set_xlabel(x_labels[variable_name])
#             axes[i].set_ylabel(f"Rate / {hist_graph_hdl.get_livetime(det_config)/(3600*24*365.25):.2f} yr")

#             axes[i].set_xlim(min(binning), max(binning))

#             axes[i].set_yscale("log") if ylog else 0
#             if "energy" in variable_name or "length" in variable_name: axes[i].set_xscale("log")
#             if not i: axes[i].legend()

#     plt.suptitle(det_config) if not title else plt.suptitle(title)
#     plt.tight_layout()
#     if savepath: plt.savefig(savepath)
#     plt.show()

# def plot_histogram_astro_newflavor(hist_graph_hdl, det_config, gamma_astro = 2.87, total_astro_norm = 2.1233, ylog = None, title = None,savepath = None):

#     print(det_config)
#     binnings = hist_graph_hdl.get_binning(det_config=det_config)

#     fig, axes = plt.subplots(1, 2, figsize=(10, 4))

#     # calculate astro contributions per flavor
#     res_flavor = {
#         "NuE" : hist_graph_hdl.get_evaled_histogram(input_variables={"total_astro_norm" : total_astro_norm/3, "gamma_astro" : gamma_astro, "prompt_norm" : 0, "conv_norm" : 0, "a" : flavor_ratios_to_angles(1,0,0)[0], "b" : flavor_ratios_to_angles(1,0,0)[1]}, det_config=det_config, reshape=True),
#         "NuMu" : hist_graph_hdl.get_evaled_histogram(input_variables={"total_astro_norm" : total_astro_norm/3, "gamma_astro" : gamma_astro,"prompt_norm" : 0, "conv_norm" : 0, "a" : flavor_ratios_to_angles(0,1,0)[0], "b" : flavor_ratios_to_angles(0,1,0)[1]}, det_config=det_config, reshape=True),
#         "NuTau" : hist_graph_hdl.get_evaled_histogram(input_variables={"total_astro_norm" : total_astro_norm/3, "gamma_astro" : gamma_astro, "prompt_norm" : 0, "conv_norm" : 0, "a" : flavor_ratios_to_angles(0,0,1)[0], "b" : flavor_ratios_to_angles(0,0,1)[1]}, det_config=det_config, reshape=True),
#     }

#     for input_flavor, res in res_flavor.items():

#         print(input_flavor)

#         for i, (variable_name, binning) in enumerate(binnings.items()):

#             hist = res_flavor[input_flavor]["mu"].sum(axis=1-i)
#             yerror = np.sqrt(res_flavor[input_flavor]["ssq"].sum(axis=1-i))

#             axes[i].stairs(hist, binning, label=f"{input_flavor}: {sum(hist):.2f}+-{sum(yerror):.2f}")
#             axes[i].fill_between(binning, np.r_[hist - yerror, (hist - yerror)[-1]], np.r_[hist + yerror, (hist + yerror)[-1]], step="post", alpha=0.4)

#             axes[i].set_xlabel(x_labels[variable_name])
#             axes[i].set_ylabel(f"Rate / {hist_graph_hdl.get_livetime(det_config)/(3600*24*365.25):.2f} yr")

#             axes[i].set_xlim(min(binning), max(binning))

#             axes[i].set_yscale("log") if ylog else 0
#             if "energy" in variable_name or "length" in variable_name: axes[i].set_xscale("log")
#             if not i: axes[i].legend()

#     plt.suptitle(det_config) if not title else plt.suptitle(title)
#     plt.tight_layout()
#     if savepath: plt.savefig(savepath)
#     plt.show()


# def plot_histogram_flavor_2D(hist_graph_hdl, det_config, gamma_astro=2.87, astro_norm=2.1233, zlog=None, title = None, savepath=None):

#     print(det_config)
#     binnings = hist_graph_hdl.get_binning(det_config=det_config)
#     var_names = list(binnings.keys())
#     x_var, y_var = var_names
#     x_bins, y_bins = binnings[x_var], binnings[y_var]

#     # calculate astro contributions per flavor
#     res_flavor = {
#         "NuMu": hist_graph_hdl.get_evaled_histogram(
#             input_variables={"astro_norm": astro_norm, "gamma_astro": gamma_astro, "prompt_norm": 0, "conv_norm": 0,
#                              "astro_nue_ratio": 0, "astro_nutau_ratio": 0},
#             det_config=det_config, reshape=True
#         ),
#         "NuMu+NuE": hist_graph_hdl.get_evaled_histogram(
#             input_variables={"astro_norm": astro_norm, "gamma_astro": gamma_astro, "prompt_norm": 0, "conv_norm": 0,
#                              "astro_nue_ratio": 1, "astro_nutau_ratio": 0},
#             det_config=det_config, reshape=True
#         ),
#         "NuMu+NuTau": hist_graph_hdl.get_evaled_histogram(
#             input_variables={"astro_norm": astro_norm, "gamma_astro": gamma_astro, "prompt_norm": 0, "conv_norm": 0,
#                              "astro_nue_ratio": 0, "astro_nutau_ratio": 1},
#             det_config=det_config, reshape=True
#         ),
#     }

#     hists = {
#         "NuE": res_flavor["NuMu+NuE"]["mu"] - res_flavor["NuMu"]["mu"],
#         "NuMu": res_flavor["NuMu"]["mu"],
#         "NuTau": res_flavor["NuMu+NuTau"]["mu"] - res_flavor["NuMu"]["mu"],
#     }

#     fig, axes = plt.subplots(1, 3, figsize=(15, 4))

#     for i, (flavor, hist) in enumerate(hists.items()):
#         mesh = axes[i].pcolormesh(x_bins, y_bins, hist.T, shading="auto", norm=plt.LogNorm() if zlog else None)
#         axes[i].set_xlabel(x_labels[x_var])
#         axes[i].set_ylabel(x_labels[y_var])
#         axes[i].set_xlim(min(x_bins), max(x_bins))
#         axes[i].set_ylim(min(y_bins), max(y_bins))
#         if "energy" in x_var or "length" in x_var: axes[i].set_xscale("log")
#         if "energy" in y_var or "length" in y_var: axes[i].set_yscale("log")
#         axes[i].set_title(flavor)
#         plt.colorbar(mesh, ax=axes[i], label=f"Rate / {hist_graph_hdl.get_livetime(det_config)/(3600*24*365.25):.2f} yr")

#     plt.suptitle(det_config) if not title else plt.suptitle(title)
#     plt.tight_layout()
#     if savepath: plt.savefig(savepath)
#     plt.show()



# def plot_histogram_components_2D(hist_graph_hdl, det_config, gamma_astro=2.87, astro_norm=2.1233, zlog=None, title = None, savepath=None):

#     print(det_config)
#     binnings = hist_graph_hdl.get_binning(det_config=det_config)
#     var_names = list(binnings.keys())
#     x_var, y_var = var_names
#     x_bins, y_bins = binnings[x_var], binnings[y_var]

#     # calculate astro contributions per flavor
#     res_flavor = {
#         "All": hist_graph_hdl.get_evaled_histogram(
#             input_variables={"astro_norm": astro_norm, "gamma_astro": gamma_astro, "prompt_norm": 1, "conv_norm": 1,
#                              "astro_nue_ratio": 1, "astro_nutau_ratio": 1},
#             det_config=det_config, reshape=True
#         ),
#         "Conventional": hist_graph_hdl.get_evaled_histogram(
#             input_variables={"astro_norm": 0.0, "gamma_astro": gamma_astro, "prompt_norm": 0, "conv_norm": 1,
#                              "astro_nue_ratio": 1, "astro_nutau_ratio": 1},
#             det_config=det_config, reshape=True
#         ),
#         "Prompt": hist_graph_hdl.get_evaled_histogram(
#             input_variables={"astro_norm": 0, "gamma_astro": gamma_astro, "prompt_norm": 1, "conv_norm": 0,
#                              "astro_nue_ratio": 1, "astro_nutau_ratio": 1},
#             det_config=det_config, reshape=True
#         ),
#         "NuMu": hist_graph_hdl.get_evaled_histogram(
#             input_variables={"astro_norm": astro_norm, "gamma_astro": gamma_astro, "prompt_norm": 0, "conv_norm": 0,
#                              "astro_nue_ratio": 0, "astro_nutau_ratio": 0},
#             det_config=det_config, reshape=True
#         ),
#         "NuMu+NuE": hist_graph_hdl.get_evaled_histogram(
#             input_variables={"astro_norm": astro_norm, "gamma_astro": gamma_astro, "prompt_norm": 0, "conv_norm": 0,
#                              "astro_nue_ratio": 1, "astro_nutau_ratio": 0},
#             det_config=det_config, reshape=True
#         ),
#         "NuMu+NuTau": hist_graph_hdl.get_evaled_histogram(
#             input_variables={"astro_norm": astro_norm, "gamma_astro": gamma_astro, "prompt_norm": 0, "conv_norm": 0,
#                              "astro_nue_ratio": 0, "astro_nutau_ratio": 1},
#             det_config=det_config, reshape=True
#         ),
#     }

#     hists = {
#         "All": res_flavor["All"]["mu"],
#         "Conventional": res_flavor["Conventional"]["mu"],
#         "Prompt": res_flavor["Prompt"]["mu"],
#         "Astro NuE": res_flavor["NuMu+NuE"]["mu"] - res_flavor["NuMu"]["mu"],
#         "Astro NuMu": res_flavor["NuMu"]["mu"],
#         "Astro NuTau": res_flavor["NuMu+NuTau"]["mu"] - res_flavor["NuMu"]["mu"],
#     }

#     fig, axes = plt.subplots(2, 3, figsize=(15, 10))
#     axes = axes.flatten()

#     for i, (flavor, hist) in enumerate(hists.items()):
#         mesh = axes[i].pcolormesh(x_bins, y_bins, hist.T, shading="auto", norm=plt.LogNorm() if zlog else None)
#         axes[i].set_xlabel(x_labels[x_var])
#         axes[i].set_ylabel(x_labels[y_var])
#         axes[i].set_xlim(min(x_bins), max(x_bins))
#         axes[i].set_ylim(min(y_bins), max(y_bins))
#         if "energy" in x_var or "length" in x_var: axes[i].set_xscale("log")
#         if "energy" in y_var or "length" in y_var: axes[i].set_yscale("log")
#         axes[i].set_title(flavor)
#         plt.colorbar(mesh, ax=axes[i], label=f"Rate / {hist_graph_hdl.get_livetime(det_config)/(3600*24*365.25):.2f} yr")

#     plt.suptitle(det_config) if not title else plt.suptitle(title)
#     plt.tight_layout()
#     if savepath: plt.savefig(savepath)
#     plt.show()



def flavor_ratios_to_angles(fr0, fr1, fr2):
    """
    Convert flavor ratios to spherical coordinates a and b.
    
    Parameters:
    fr0, fr1, fr2: float
        The flavor ratios for neutrino flavors (e.g., nu_e, nu_mu, nu_tau).
    
    Returns:
    tuple
        (a = sphi4, b = c2psi) angles in.
    """
    # Normalize the flavor ratios
    norm = fr0 + fr1 + fr2
    fr0_n = fr0 / norm
    fr1_n = fr1 / norm
    fr2_n = fr2 / norm
    
    # Compute phi
    sphi4 = (1.0 - fr2_n) ** 2 # from 0 to 1
    
    # Compute psi
    sphi2 = (1.0 - fr2_n)
    if sphi2 == 0.0:
        c2psi = 0.0
        x = np.nan
    else:
        cpsi2 = fr0_n / sphi2
        x = np.sqrt(cpsi2)
        if x > 1: x = 1
        psi = np.arccos(x)
        c2psi = np.cos(2.0 * np.arccos(x)) # from -1 to 1

    return sphi4, c2psi 


def angles_to_flavor_ratios(a, b):
    # Calculate and return the three flavor ratios: E, Mu, and Tau
    return (
        (b + 1.0) * np.sqrt(a) / 2.0,  # Electron flavor ratio (E)
        (-b + 1.0) * np.sqrt(a) / 2.0, # Muon flavor ratio (Mu)
        -np.sqrt(a) + 1.0              # Tau flavor ratio (Tau)
    )