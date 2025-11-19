import sys, os
from collections import defaultdict
import tables
from utils import *
import numpy as np
import matplotlib.pyplot as plt
from common import calculator # tianlu
from copy import deepcopy

# hdf path
reco_version_spice = "spice_tau_reco"
hdf_path_spice = f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/{reco_version_spice}"
plotting_main_path = f"/data/user/tvaneede/GlobalFit/reco_processing/performance/output/{reco_version_spice}"

reco_version_ftp = "taureco_iceprod_v1"
hdf_path_ftp = f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/{reco_version_ftp}/merged"

os.system(f"mkdir -p {plotting_main_path}")

datasets_spice = {}
datasets_ftp = {}

# neutrino datasets
flavors = ["NuE","NuMu","NuTau"]

for flavor in flavors:
    datasets_spice[flavor] = {}
    datasets_spice[flavor]["hdf_file_path"] = f"{hdf_path_spice}/{flavor}.h5"

    datasets_ftp[flavor] = {}
    datasets_ftp[flavor]["hdf_file_path"] = f"{hdf_path_ftp}/HESE_{flavor}.h5"


###
### Normal reco
###

from plot_dicts_spice import plots_taupede as plots_taupede_spice
from plot_dicts_ftp   import plots_taupede as plots_taupede_ftp

from plot_dicts_spice import plots_monopod as plots_monopod_spice
from plot_dicts_ftp   import plots_monopod as plots_monopod_ftp

for flavor_key, plots_spice, plots_ftp in zip(["NuTau","NuE"], 
                                              [plots_taupede_spice,plots_monopod_spice],
                                              [plots_taupede_ftp, plots_monopod_ftp]):

    hdf_file_path_spice = datasets_spice[flavor_key]["hdf_file_path"]
    hdf_file_path_ftp = datasets_ftp[flavor_key]["hdf_file_path"]

    ### general plots
    for plot_name,plot in plots_spice.items(): 
        x = plot_median_quartiles( [hdf_file_path_spice],[plot], 
                                    plotting_main_path=f"{plotting_main_path}/{flavor_key}" )

    ### compare with ftp
    for i, (plot_name_spice, plot_name_ftp) in enumerate(zip(plots_spice.keys(), plots_ftp.keys())):
        plot_spice = plots_spice[plot_name_spice]
        plot_ftp = plots_ftp[plot_name_ftp]

        plot_spice["label"] = "Previous analysis"
        plot_ftp["label"] = "New analysis"

        x = plot_median_quartiles( [hdf_file_path_spice,hdf_file_path_ftp],
                                   [plot_spice,plot_ftp],
                                    plotting_main_path=f"{plotting_main_path}/compare" )

###
### EventGenerator
###
from plot_dicts_ftp import plots_evtgen

flavor_key = "NuTau"

plot_combinations = [

    [
    [
        datasets_spice[flavor_key]["hdf_file_path"],
        datasets_ftp[flavor_key]["hdf_file_path"],
        datasets_ftp[flavor_key]["hdf_file_path"]
    ],
    [
        plots_taupede_spice["HESETaupedeFit_deltaLength_trueLength"], 
        plots_taupede_ftp["TaupedeFit_iMIGRAD_PPB0_deltaLength_trueLength"],
        plots_evtgen["EventGeneratorDC_Thijs_deltaLength_trueLength"],

    ]
    ],

    [
    [
        datasets_spice[flavor_key]["hdf_file_path"],
        datasets_ftp[flavor_key]["hdf_file_path"],
        datasets_ftp[flavor_key]["hdf_file_path"]
    ],
    [
        plots_taupede_spice["HESETaupedeFit_deltaLength_trueLength_normalised"], 
        plots_taupede_ftp["TaupedeFit_iMIGRAD_PPB0_deltaLength_trueLength_normalised"],
        plots_evtgen["EventGeneratorDC_Thijs_deltaLength_trueLength_normalised"],

    ]
    ],

    [
    [
        datasets_spice[flavor_key]["hdf_file_path"],
        datasets_ftp[flavor_key]["hdf_file_path"],
        datasets_ftp[flavor_key]["hdf_file_path"]
    ],
    [
        plots_taupede_spice["HESETaupedeFit_deltaEasym_trueLength"], 
        plots_taupede_ftp["TaupedeFit_iMIGRAD_PPB0_deltaEasym_trueLength"],
        plots_evtgen["EventGeneratorDC_Max_deltaEasym_trueLength"],

    ]
    ],

]

for plot_quartiles in [True,False]:
    for plot_combination in plot_combinations:
        hdf_files = plot_combination[0]
        plots = plot_combination[1]
        plots[2]["label"] = "EventGenerator"
        x = plot_median_quartiles( hdf_files,
                                    plots,
                                    plotting_main_path=f"{plotting_main_path}/evtgen_quartiles-{plot_quartiles}",
                                    plot_quartiles = plot_quartiles )