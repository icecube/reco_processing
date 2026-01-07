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
# from datasets import datasets_hese as datasets
from datasets import datasets_cascade as datasets

# set the inputs
reco_version = "cascade_iceprod_v0"

# Dynamically select the desired dataset
simulation_datasets = getattr(datasets, reco_version)

flavor_datasets = {
    "NuE" : {},
    "NuMu" : {},
    "NuTau" : {},
    "MuonGun" : {},
}

hdf_path = f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/{reco_version}"
hdf_path_merged = f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/{reco_version}/merged"
os.system(f"mkdir -p {hdf_path}")
os.system(f"mkdir -p {hdf_path_merged}")


for simulation_name in simulation_datasets:

    dataset = simulation_datasets[simulation_name]["dataset"]
    flavor = simulation_datasets[simulation_name]["flavor"]
    subfolders = simulation_datasets[simulation_name]["subfolders"]
    levels = simulation_datasets[simulation_name]["levels"]

    for level in levels:

        hdf_out_path = f"{hdf_path_merged}/{level}_{flavor}_{dataset}.h5"

        if level not in flavor_datasets[flavor]: flavor_datasets[flavor][level] = [hdf_out_path]
        else: flavor_datasets[flavor][level].append( hdf_out_path )

        cmd = f"python merge.py -o {hdf_out_path}"

        for subfolder in subfolders:
            cmd += f" {hdf_path}/{level}_{flavor}_{dataset}_{subfolder}.h5"

        print(20*"-", "creating")
        print(simulation_name, dataset, level)
        print("creating", os.path.basename(hdf_out_path))
        print("from", subfolders)

        os.system(cmd)
        

print(flavor_datasets)

# combine flavors
for flavor in flavor_datasets:
    
    for level in flavor_datasets[flavor]:

        hdf_out_path = f"{hdf_path_merged}/{level}_{flavor}.h5"

        cmd = f"python merge.py -o {hdf_out_path}"

        for file_path in flavor_datasets[flavor][level]:
            cmd += f" {file_path}"

        print(20*"-", "creating")
        print(flavor, level)
        print("creating", hdf_out_path)
        # print(cmd)
        os.system(cmd)
