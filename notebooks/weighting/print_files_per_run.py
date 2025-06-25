import sys, os, glob
import subprocess
import re

# Append the custom module path
sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")

# Import the datasets module
from datasets import datasets

# set the inputs
reco_input_version = "v1_wpid"

# Dynamically select the desired dataset
simulation_datasets = getattr(datasets, reco_input_version)

for simulation_name in simulation_datasets:


    print(10*"-", simulation_name)

    total_files = 0

    for run_number in simulation_datasets[simulation_name]["subfolders"]:

        simulation_path = f"{simulation_datasets[simulation_name]['reco_base_path']}/{ simulation_datasets[simulation_name]['dataset'] }/{ run_number }"

        folders = [f for f in os.listdir(simulation_path) if os.path.isdir(os.path.join(simulation_path, f))]

        total_files += len([f for f in os.listdir(simulation_path) if os.path.isfile(os.path.join(simulation_path, f))])

        print("run_number", run_number, "files", total_files)
