import sys, os, glob
import subprocess
import re

# Append the custom module path
sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")

# Import the datasets module
from datasets import datasets

# set the inputs
reco_version = "evtgen_v1_rec_v2"

# Dynamically select the desired dataset
simulation_datasets = getattr(datasets, reco_version)

for simulation_name in simulation_datasets:
    
    simulation_subfolders = simulation_datasets[simulation_name]['subfolders']
    simulation_flavor = simulation_datasets[simulation_name]["flavor"]
    simulation_dataset = simulation_datasets[simulation_name]['dataset']
    simulation_reco_base_path = simulation_datasets[simulation_name]['reco_base_out_path']

    print(50*"-")
    print(simulation_name,simulation_dataset)

    total_files = 0

    for simulation_subfolder in simulation_subfolders:
        reco_input_path = f"{simulation_reco_base_path}/{simulation_dataset}/{simulation_subfolder}"
        files = glob.glob(f"{reco_input_path}/*.i3.*")
        nfiles = len(files)
        print(simulation_subfolder, nfiles)
        total_files += nfiles

    print(simulation_name,simulation_dataset, total_files)