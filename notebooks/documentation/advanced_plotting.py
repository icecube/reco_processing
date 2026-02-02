import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
import numpy as np
from weights import *

def compare_snowstorm_ensemble_flavor(simulation_datasets, 
                               base_key = "ftp_ensemble_ani_v1",
                               level = "level6_cascade",
                               base_var_key1 = "I3MCWeightDict", 
                               base_var_key2 = "PrimaryNeutrinoEnergy",
                               variable_name = "PrimaryNeutrinoEnergy [GeV]",
                               syst_param    = "CrystalDensityParameterScaling",
                               syst_upper    = 1.0,
                               syst_lower    = 1.0,
                               bins = np.geomspace(1e4, 1e6, 20),
                               xscale = "log", yscale = "log", 
                               livetime_yr = 11.687,
                               flux_gamma = 2.87,
                               flux_norm  = 2.12,
                               plotting_path = None):
    
    # weight for event rate per livetime_s
    fluxmodel = create_AstroFluxModel(per_flavor_norm=flux_norm, gamma_astro=flux_gamma)
    livetime_s = livetime_yr * 365.25 * 24 * 3600

    bin_centers = (bins[:-1] + bins[1:]) / 2 # Compute bin centers for plotting

    fig = plt.figure(figsize=(18, 8)) 
    gs = GridSpec(2, 3, height_ratios=[3, 1], hspace=0.05, wspace=0.3)
    fig.suptitle(rf"Variable {variable_name}, {level}", fontsize=16)

    # 3 axes for separate NuE, NuMu, NuTau
    axes = [fig.add_subplot(gs[0, i]) for i in range(3)]        
    axes_ratio = [fig.add_subplot(gs[1, i], sharex=axes[i]) for i in range(3)]  

    for ax, ax_ratio, flavor in zip(axes, axes_ratio, ["NuE", "NuMu", "NuTau"]):
        ax.set_title(rf"{flavor} astro, $\gamma = {flux_gamma}$, $\phi_0={flux_norm}$")
        ax.set_xscale(xscale)
        ax.set_yscale(yscale)
        ax.set_ylabel(f"Rate / {livetime_yr} yr") 

        ax_ratio.set_xscale(xscale)
        ax_ratio.set_ylabel(f"Ratio high / low")
        ax_ratio.set_xlabel(variable_name)
        ax_ratio.axhline(1, color="gray", linestyle="--", linewidth=1)

        var = simulation_datasets[base_key][flavor]["weighters"][level].get_column(base_var_key1, base_var_key2)
        systematic_scaling = simulation_datasets[base_key][flavor]["weighters"][level].get_column("SnowstormParameterDict", syst_param)

        weights = simulation_datasets[base_key][flavor]["weighters"][level].get_weights(fluxmodel) * livetime_s

        # split dataset based on snowstorm systematic
        mask_low = systematic_scaling < syst_upper
        mask_high = systematic_scaling > syst_lower

        var_low = var[mask_low]
        weights_low = weights[mask_low]

        var_high = var[mask_high]
        weights_high = weights[mask_high]

        hist_low, _  = np.histogram(var_low,weights=weights_low,bins=bins )
        hist_high, _  = np.histogram(var_high,weights=weights_high,bins=bins )

        hist_low_error, _ = error_cal(bin_edges=bins,weights=weights_low, data=var_low)
        hist_high_error, _ = error_cal(bin_edges=bins,weights=weights_high, data=var_high)

        ratio = hist_high / hist_low

        ax_ratio.plot(bin_centers, ratio, drawstyle="steps-mid", color="black")

        # upper plot: histograms
        ax.hist(var_low, 
                weights=weights_low, 
                bins=bins, histtype="step", color="black", linestyle="-",label = f"< {syst_upper}")
        ax.hist(var_high, 
                weights=weights_high, 
                bins=bins, histtype="step", color="C3", linestyle="-",label = f"> {syst_lower}")

        ax.errorbar(x=bin_centers, y=hist_low,yerr=hist_low_error, color="black",fmt='o', markersize=2,capsize=5)
        ax.errorbar(x=bin_centers, y=hist_high,yerr=hist_high_error, color="C3",fmt='o', markersize=2,capsize=5)

        # error of the ratio
        ratio_error = ratio * np.sqrt(
                (hist_low_error / hist_low)**2 + (hist_high_error / hist_high)**2
        )
        ratio_error[~np.isfinite(ratio_error)] = 0  # Set ratio error to 0 where hist1 or hist2 is 0
        ax_ratio.errorbar(bin_centers, ratio, yerr=ratio_error,fmt='o', color='black', markersize=2, capsize=5)

        plt.setp(ax.get_xticklabels(), visible=False)
        ax_ratio.set_ylim(0.8, 1.2)  # adjust as needed
        ax_ratio.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.5)
        ax.set_xlim(bins[0], bins[-1])
        ax.set_ylim(0.8 * np.min([hist_low.min(), hist_high.min()]),
                    1.2 * np.max([hist_low.max(), hist_high.max()]))
        ax.legend(title=syst_param)

    if plotting_path: plt.savefig(plotting_path)

    plt.show()
    plt.close() 

def compare_dataset_flavor(simulation_datasets, 
                           base_key = "ftp_ensemble_ani_v1",
                           base_level = "level6_cascade",
                           base_var_key1 = "I3MCWeightDict", 
                           base_var_key2 = "PrimaryNeutrinoEnergy",
                           alt_key = "ftp_ensemble_ani_v1",
                           alt_level = "level6_cascade",
                           alt_var_key1 = "I3MCWeightDict", 
                           alt_var_key2 = "PrimaryNeutrinoEnergy",
                           variable_name = "PrimaryNeutrinoEnergy [GeV]",
                               bins = np.geomspace(1e4, 1e6, 20),
                               xscale = "log", yscale = "log", 
                               livetime_yr = 11.687,
                               flux_gamma = 2.87,
                               flux_norm  = 2.12,
                               plotting_path = None):
    
    # weight for event rate per livetime_s
    fluxmodel = create_AstroFluxModel(per_flavor_norm=flux_norm, gamma_astro=flux_gamma)
    livetime_s = livetime_yr * 365.25 * 24 * 3600

    bin_centers = (bins[:-1] + bins[1:]) / 2 # Compute bin centers for plotting

    fig = plt.figure(figsize=(18, 8)) 
    gs = GridSpec(2, 3, height_ratios=[3, 1], hspace=0.05, wspace=0.3)
    fig.suptitle(rf"{base_level}, {base_key}, {alt_key}", fontsize=16)

    # 3 axes for separate NuE, NuMu, NuTau
    axes = [fig.add_subplot(gs[0, i]) for i in range(3)]        
    axes_ratio = [fig.add_subplot(gs[1, i], sharex=axes[i]) for i in range(3)]  

    for ax, ax_ratio, flavor in zip(axes, axes_ratio, ["NuE", "NuMu", "NuTau"]):
        ax.set_title(rf"{flavor} astro, $\gamma = {flux_gamma}$, $\phi_0={flux_norm}$")
        ax.set_xscale(xscale)
        ax.set_yscale(yscale)
        ax.set_ylabel(f"Rate / {livetime_yr} yr") 

        ax_ratio.set_xscale(xscale)
        ax_ratio.set_ylabel(f"Ratio high / low")
        ax_ratio.set_xlabel(variable_name)
        ax_ratio.axhline(1, color="gray", linestyle="--", linewidth=1)

        var_base = simulation_datasets[base_key][flavor]["weighters"][base_level].get_column(base_var_key1, base_var_key2)
        weights_base = simulation_datasets[base_key][flavor]["weighters"][base_level].get_weights(fluxmodel) * livetime_s

        var_alt = simulation_datasets[alt_key][flavor]["weighters"][alt_level].get_column(alt_var_key1, alt_var_key2)
        weights_alt = simulation_datasets[alt_key][flavor]["weighters"][alt_level].get_weights(fluxmodel) * livetime_s

        hist_base, _  = np.histogram(var_base,weights=weights_base,bins=bins )
        hist_alt, _  = np.histogram(var_alt,weights=weights_alt,bins=bins )

        hist_base_error, _ = error_cal(bin_edges=bins,weights=weights_base, data=var_base)
        hist_alt_error, _ = error_cal(bin_edges=bins,weights=weights_alt, data=var_alt)

        ratio = hist_alt / hist_base

        ax_ratio.plot(bin_centers, ratio, drawstyle="steps-mid", color="black")

        # upper plot: histograms
        ax.hist(var_base, 
                weights=weights_base, 
                bins=bins, histtype="step", color="black", linestyle="-",label = base_key)
        ax.hist(var_alt, 
                weights=weights_alt, 
                bins=bins, histtype="step", color="C3", linestyle="-",label = alt_key)

        ax.errorbar(x=bin_centers, y=hist_base,yerr=hist_base_error, color="black",fmt='o', markersize=2,capsize=5)
        ax.errorbar(x=bin_centers, y=hist_alt,yerr=hist_alt_error, color="C3",fmt='o', markersize=2,capsize=5)

        # error of the ratio
        ratio_error = ratio * np.sqrt(
                (hist_base_error / hist_base)**2 + (hist_alt_error / hist_alt)**2
        )
        ratio_error[~np.isfinite(ratio_error)] = 0  # Set ratio error to 0 where hist1 or hist2 is 0
        ax_ratio.errorbar(bin_centers, ratio, yerr=ratio_error,fmt='o', color='black', markersize=2, capsize=5)

        plt.setp(ax.get_xticklabels(), visible=False)
        ax_ratio.set_ylim(0.8, 1.2)  # adjust as needed
        ax_ratio.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.5)
        ax.set_xlim(bins[0], bins[-1])
        ax.set_ylim(0.8 * np.min([hist_base.min(), hist_alt.min()]),
                    1.2 * np.max([hist_base.max(), hist_alt.max()]))
        ax.legend(title="Dataset")

    if plotting_path: plt.savefig(plotting_path)

    plt.show()
    plt.close() 


def error_cal(bin_edges,weights,data):
    errors = []
    bin_centers = []
    
    for bin_index in range(len(bin_edges) - 1):

        # find which data points are inside this bin
        bin_left = bin_edges[bin_index]
        bin_right = bin_edges[bin_index + 1]
        in_bin = np.logical_and(bin_left < data, data <= bin_right)
        

        # filter the weights to only those inside the bin
        weights_in_bin = weights[in_bin]

        # compute the error however you want
        error = np.sqrt(np.sum(weights_in_bin ** 2))
        errors.append(error)

        # save the center of the bins to plot the errorbar in the right place
        bin_center = (bin_right + bin_left) / 2
        bin_centers.append(bin_center)

    errors=np.asarray(errors)
    bin_centers=np.asarray(bin_centers)
    return errors, bin_centers