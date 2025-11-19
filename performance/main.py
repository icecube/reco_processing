import sys, os
from collections import defaultdict
import tables
from utils import *
import numpy as np
import matplotlib.pyplot as plt
from common import calculator # tianlu
from copy import deepcopy

colors = ["C0","C3","C5","C4"]

# hdf path
# reco_version = "taureco_iceprod_v0"
reco_version = "taureco_iceprod_v3"
hdf_path = f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/{reco_version}/merged"
plotting_main_path = f"/data/user/tvaneede/GlobalFit/reco_processing/performance/output/{reco_version}"

os.system(f"mkdir -p {plotting_main_path}")

datasets_by_level = {}

# neutrino datasets
flavors = ["NuE","NuMu","NuTau"]
# levels  = ["level6_cascade","level6_hybrid","level6_muon", "level7_cascade", "HESE"]
levels  = ["HESE"]

for level in levels:
    datasets_by_level[level] = {}
    for flavor in flavors:
        datasets_by_level[level][flavor] = {}
        datasets_by_level[level][flavor]["hdf_file_path"] = f"{hdf_path}/{level}_{flavor}.h5"



###
### Separate per level, flavor
###

from plot_dicts_ftp import plots_taupede
from plot_dicts_ftp import plots_monopod

for flavor_key, plots in zip(["NuTau","NuE"],[plots_taupede,plots_monopod]):

    # for i,level_key in enumerate(["HESE", "level7_cascade"]):
    for i,level_key in enumerate(["HESE"]):

        hdf_file_path = datasets_by_level[level_key][flavor_key]["hdf_file_path"]

        for plot_name,plot in plots.items(): 
            x = plot_median_quartiles( [hdf_file_path],[plot], 
                                        plotting_main_path=f"{plotting_main_path}/{level_key}/{flavor_key}" )


###
### compare evtgen
### 
from plot_dicts_ftp import plots_taupede, plots_evtgen
flavor_key = "NuTau"
level_key = "HESE"
hdf_file_path = datasets_by_level[level_key][flavor_key]["hdf_file_path"]
for plot_name,plot in plots_evtgen.items(): 
    x = plot_median_quartiles( [hdf_file_path],[plot], 
                                            plotting_main_path=f"{plotting_main_path}/{level_key}/{flavor_key}" )



# overlay levels
# for plot in plots: 

#     hdf_files = []
#     plot_dicts = []

#     for i,level_key in enumerate(["HESE", "level7_cascade"]):
#         hdf_files.append( datasets_by_level[level_key][flavor_key]["hdf_file_path"] )
#         plot_dicts.append( deepcopy( plot ) )
#         plot_dicts[i]["label"] = level_key

#     x = plot_median_quartiles( hdf_files,plot_dicts )
