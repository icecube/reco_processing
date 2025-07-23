import sys, os, glob
import subprocess
import re
import h5py
import shutil
import sys
import os
import argparse

# Append the custom module path
sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")

# Import the datasets module
from datasets import datasets

# set the inputs
reco_version = "spice_tau_reco"

# Dynamically select the desired dataset
simulation_datasets = getattr(datasets, reco_version)

flavor_datasets = {
    "NuE" : [],
    "NuMu" : [],
    "NuTau" : [],
    # "MuonGun" : [],
}

for simulation_name in simulation_datasets:
    
    dataset = simulation_datasets[simulation_name]["dataset"]
    flavor = simulation_datasets[simulation_name]["flavor"]
    hdf_path = simulation_datasets[simulation_name]["hdf_path"] + "_allvar"
    subfolders = simulation_datasets[simulation_name]["subfolders"]

    hdf_out_path = f"{hdf_path}/{flavor}_{dataset}.h5"

    flavor_datasets[flavor].append( hdf_out_path )

    cmd = f"python merge.py -o {hdf_out_path}"

    for subfolder in subfolders:
        cmd += f" {hdf_path}/{flavor}_{dataset}_{subfolder}.h5"

    print(simulation_name, dataset)
    print("creating", hdf_out_path)

    os.system(cmd)

print(flavor_datasets)

# combine flavors
for flavor in flavor_datasets:

    hdf_out_path = f"{hdf_path}/{flavor}.h5"

    cmd = f"python merge.py -o {hdf_out_path}"

    for file_path in flavor_datasets[flavor]:
        cmd += f" {file_path}"

    print(flavor)
    print("creating", hdf_out_path)
    # print(cmd)
    os.system(cmd)
