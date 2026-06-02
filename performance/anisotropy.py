import sys, os
from collections import defaultdict
import tables
from utils import *
import numpy as np
import matplotlib.pyplot as plt
from common import calculator # tianlu
from copy import deepcopy

plt.style.use("style.mplstyle")

plotting_main_path = f"/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/anisotropy"

# hdf path
reco_version_spice = "spice_tau_reco"
hdf_path_spice = f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/{reco_version_spice}"

reco_version_ftp = "hese_iceprod_v7"
hdf_path_ftp = f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/{reco_version_ftp}/merged"

reco_version_ftp_snowstorm = "ftp_ensemble_ani_v1"
hdf_path_ftp_snowstorm = f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/{reco_version_ftp_snowstorm}/merged"


os.system(f"mkdir -p {plotting_main_path}")

datasets_spice = {}
datasets_ftp = {}
datasets_ftp_snowstorm = {}

# neutrino datasets
flavors = ["NuE","NuMu","NuTau"]

for flavor in flavors:
    datasets_spice[flavor] = {}
    datasets_spice[flavor]["hdf_file_path"] = f"{hdf_path_spice}/{flavor}.h5"

    datasets_ftp[flavor] = {}
    datasets_ftp[flavor]["hdf_file_path"] = f"{hdf_path_ftp}/HESE_{flavor}.h5"

    datasets_ftp_snowstorm[flavor] = {}
    datasets_ftp_snowstorm[flavor]["hdf_file_path"] = f"{hdf_path_ftp_snowstorm}/HESE_evtgen_{flavor}.h5"

##
## Normal reco
##

from plot_dicts_anisotropy import plots_spice
from plot_dicts_anisotropy import plots_ftp


for flavor_key, plots_spice, plots_ftp, ylim in zip(["NuTau","NuE"], 
                                              [plots_spice, plots_spice],
                                              [plots_ftp, plots_ftp],
                                              [[-5,10], [-5,20]]):

    print(10*"-", flavor_key, 10*"-")

    hdf_file_path_spice = datasets_spice[flavor_key]["hdf_file_path"]
    hdf_file_path_ftp = datasets_ftp[flavor_key]["hdf_file_path"]

    ### general plots
    for plot_name,plot in plots_spice.items(): 
        print("plotting spice")
        if flavor_key == "Nue": plot["ylim"] = ylim
        x = plot_median_quartiles( [hdf_file_path_spice],[plot], 
                                    plotting_main_path=f"{plotting_main_path}/{flavor_key}" )

    ### compare with ftp
    for i, (plot_name_spice, plot_name_ftp) in enumerate(zip(plots_spice.keys(), plots_ftp.keys())):
        plot_spice = plots_spice[plot_name_spice]
        plot_ftp = plots_ftp[plot_name_ftp]

        plot_spice["label"] = "Previous analysis"
        plot_ftp["label"] = "New analysis"


        if flavor_key == "Nue": plot_spice["ylim"] = ylim

        x = plot_median_quartiles( [hdf_file_path_spice,hdf_file_path_ftp],
                                   [plot_spice,plot_ftp],
                                    plotting_main_path=f"{plotting_main_path}/compare/{flavor_key}" )


###
### snowstorm
###

for flavor, ylim in zip(["NuE", "NuTau"], [[-5,20], [-5,10]] ):

  plot_ftp = { "reco_key_y" : "TaupedeFit_iMIGRAD_PPB0", "reco_var_key_y" : "length",
    "true_key_y" : "cc",             "true_var_key_y" : "length",
    "key_x" : "cc",                  "variable_key_x" : "azimuth",
    "bins" : np.linspace(0,6.28318530718,20), "xscale" : "linear", "ylim" : ylim, "normalize" : False,
    "xlabel" : r"Azimuth [rad]",  "ylabel" : r"$L_{\rm reco} - L_{\rm true}$ [m]", 
    "name" : "TaupedeFit_iMIGRAD_PPB0_deltaLength_trueAzimuth",
    "label" : "Baseline"  }

  plot_snowstorm = deepcopy(plot_ftp)
  plot_snowstorm["label"] = "Perturbed"

  hdf_file_path = datasets_ftp[flavor]["hdf_file_path"]
  hdf_file_path_snowstorm = datasets_ftp_snowstorm[flavor]["hdf_file_path"]

  x = plot_median_quartiles( [hdf_file_path,hdf_file_path_snowstorm],
                              [plot_ftp,plot_snowstorm],
                              plotting_main_path=f"{plotting_main_path}/snowstorm/{flavor}" )

  ### crystal

  plot_snowstorm_all = { 
    "reco_key_y" : "TaupedeFit_iMIGRAD_PPB0", "reco_var_key_y" : "length",
    "true_key_y" : "cc",             "true_var_key_y" : "length",
    "key_x" : "cc",                  "variable_key_x" : "azimuth",
    "bins" : np.linspace(0,6.28318530718,20), "xscale" : "linear", "ylim" : ylim, "normalize" : False,
    "xlabel" : r"Azimuth [rad]",  "ylabel" : r"$L_{\rm reco} - L_{\rm true}$ [m]", 
    "name" : "snowstorm_all_crystal_deltaLength_trueAzimuth",
    "label" : "All"  }

  plot_snowstorm_l1 = deepcopy(plot_snowstorm_all)
  plot_snowstorm_l1["label"] = "Ice crystal > 1"
  plot_snowstorm_l1["cut_variables"] = {"ice_crystal": ("SnowstormParameterDict", "CrystalDensityParameterScaling") }
  plot_snowstorm_l1["cut"] = lambda ice_crystal:  (ice_crystal > 1.0)

  plot_snowstorm_l2 = deepcopy(plot_snowstorm_all)
  plot_snowstorm_l2["label"] = "Ice crystal < 1"
  plot_snowstorm_l2["cut_variables"] = {"ice_crystal": ("SnowstormParameterDict", "CrystalDensityParameterScaling") }
  plot_snowstorm_l2["cut"] = lambda ice_crystal:  (ice_crystal < 1.0)

  x = plot_median_quartiles( [hdf_file_path_snowstorm,hdf_file_path_snowstorm, hdf_file_path_snowstorm],
                              [plot_snowstorm_all,plot_snowstorm_l1,plot_snowstorm_l2],
                              plotting_main_path=f"{plotting_main_path}/snowstorm/{flavor}" )

  ### half range

  plot_snowstorm_all = { 
    "reco_key_y" : "TaupedeFit_iMIGRAD_PPB0", "reco_var_key_y" : "length",
    "true_key_y" : "cc",             "true_var_key_y" : "length",
    "key_x" : "cc",                  "variable_key_x" : "azimuth",
    "bins" : np.linspace(0,6.28318530718,20), "xscale" : "linear", "ylim" : ylim, "normalize" : False,
    "xlabel" : r"Azimuth [rad]",  "ylabel" : r"$L_{\rm reco} - L_{\rm true}$ [m]", 
    "name" : "snowstorm_half_crystal_deltaLength_trueAzimuth",
    "label" : "All"  }

  plot_snowstorm_l1 = deepcopy(plot_snowstorm_all)
  plot_snowstorm_l1["label"] = "Ice crystal > 1.1"
  plot_snowstorm_l1["cut_variables"] = {"ice_crystal": ("SnowstormParameterDict", "CrystalDensityParameterScaling") }
  plot_snowstorm_l1["cut"] = lambda ice_crystal:  (ice_crystal > 1.1)

  plot_snowstorm_l2 = deepcopy(plot_snowstorm_all)
  plot_snowstorm_l2["label"] = "Ice crystal < 0.9"
  plot_snowstorm_l2["cut_variables"] = {"ice_crystal": ("SnowstormParameterDict", "CrystalDensityParameterScaling") }
  plot_snowstorm_l2["cut"] = lambda ice_crystal:  (ice_crystal < 0.9)

  x = plot_median_quartiles( [hdf_file_path_snowstorm,hdf_file_path_snowstorm, hdf_file_path_snowstorm],
                              [plot_snowstorm_all,plot_snowstorm_l1,plot_snowstorm_l2],
                              plotting_main_path=f"{plotting_main_path}/snowstorm/{flavor}" )