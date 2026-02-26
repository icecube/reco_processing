import sys, os
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from NNMFit.utilities import ScanHandler

# import plotting utils
sys.path.append( "/data/user/tvaneede/utils" )
from FlavourScansPlotting import get_contour_points

# import scanning points
from flavor_fracs import *
points = pd.read_pickle('/data/user/tvaneede/GlobalFit/custom_scan_flavor/default_custom_scan_points_flavor.pickle')
flavs = flavor_frac(np.asarray(points['astro_nue_ratio']),np.asarray(points['astro_nutau_ratio']))

# import plotting flavor triangle
sys.path.append( "/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks" )
from plot_utils_triangle import *

# dict with all my dag scans
sys.path.append( "/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/flavor_globalfit" )
from scan_dict import scan_dir_dict


plotting_path = "/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/scan_difference_nnmfit_version/"
os.system(f"mkdir -p {plotting_path}")

# load the data
drop_unsuccessful = False

dag_path  = "/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/dag_scans/flavor_globalfit"
hese_path = f"{dag_path}/hese"
scan_dir  =  f"{hese_path}/mcd-simpletopology_flux-hese_feat-11features_plus_rloglmilli_econf_evtgen/bdt1_0.333333_bdt2_0.366667_length_10_10bdtprod_threshold_0.122_combinedBaseline"

name = sys.argv[1]

scan_dict = {  }
scan_dict[name] = ScanHandler(scan_dir,dump=False,drop_unsuccessful=drop_unsuccessful)

scan_df = scan_dict[name].get_scan_df("astro_nue_ratio-astro_nutau_ratio")
scan_df.to_csv(f"scan_df_{name}.csv", index=False)

data = {name : {}}

data[name]["ftau_asimov_poisson"],data[name]["fe_asimov_poisson"],data[name]["ft_grid_asimov_poisson"],data[name]["fe_grid_asimov_poisson"],data[name]["ts_grid_asimov_poisson"] = get_contour_points(scan_dict,name)

C = compare_contours( data = data,
                  names = [name],
                  labels = [name],
                  levels = ["68%"],
                  title = r"$\phi_0 = 2.12,\gamma=2.87$",
                  savepath = f"contour_{name}.png")


C = likelihood_contour( data = data,
                  name = name,
                  labels = [name],
                  levels = ["68%"],
                  title = r"$\phi_0 = 2.12,\gamma=2.87$",
                  savepath = f"likelihood_{name}.png")


fe=data[name]["fe_grid_asimov_poisson"]
ft=data[name]["ft_grid_asimov_poisson"]
ts=data[name]["ts_grid_asimov_poisson"]

FE,FT=np.meshgrid(fe,ft)

df=pd.DataFrame({
    "fe":FE.ravel(),
    "ft":FT.ravel(),
    "ts":ts.ravel()
})

df=df.dropna().reset_index(drop=True)
df.to_csv(f"interpolated_{name}.csv",index=False)
