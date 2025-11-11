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
reco_version = "test_crystal_density_high_2"

# Dynamically select the desired dataset
simulation_datasets = getattr(datasets, reco_version)

flavor_datasets = {
    "NuE" : {},
    "NuMu" : {},
    "NuTau" : {},
    # "MuonGun" : [],
}

hdf_path = f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/{reco_version}"
os.system(f"mkdir -p {hdf_path}")

for simulation_name in simulation_datasets:

    dataset = simulation_datasets[simulation_name]["dataset"]
    flavor = simulation_datasets[simulation_name]["flavor"]
    subfolders = simulation_datasets[simulation_name]["subfolders"]
    levels = simulation_datasets[simulation_name]["levels"]
    # hdf_path = simulation_datasets[simulation_name]["hdf_path"]

    for level in levels:

        hdf_out_path = f"{hdf_path}/{level}_{flavor}_{dataset}.h5"

        if level not in flavor_datasets[flavor]: flavor_datasets[flavor][level] = [hdf_out_path]
        else: flavor_datasets[flavor][level].append( hdf_out_path )

        cmd = f"python merge.py -o {hdf_out_path}"

        for subfolder in subfolders:
            cmd += f" {hdf_path}/{level}_{flavor}_{dataset}_{subfolder}.h5"

        print(simulation_name, dataset)
        print("creating", hdf_out_path)
        print(cmd)

        os.system(cmd)
    
    # break
    

print(flavor_datasets)

# combine flavors
for flavor in flavor_datasets:
    
    for level in flavor_datasets[flavor]:

        hdf_out_path = f"{hdf_path}/{level}_{flavor}.h5"

        cmd = f"python merge.py -o {hdf_out_path}"

        for file_path in flavor_datasets[flavor][level]:
            cmd += f" {file_path}"

        print(flavor)
        print("creating", hdf_out_path)
        # print(cmd)
        os.system(cmd)
