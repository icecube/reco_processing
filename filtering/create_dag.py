import sys, os, glob
import subprocess
import re

sys.path.append('/data/user/tvaneede/GlobalFit/reco_processing')
from simulation_datasets import simulation_datasets

# set the inputs
filter_version = "v1"

# fixed paths
dag_base_path = "/scratch/tvaneede/reco/filtering"
work_path = "/data/user/tvaneede/GlobalFit/reco_processing/filtering"

submit_jobs = True # actually submit the dag jobs

# fixed dag paths
dag_name = f"filter_dag_{filter_version}_numu_22645_22644_nue_22612_22613"

dag_path      = f"{dag_base_path}/{filter_version}/{dag_name}"
log_dir       = f"{dag_path}/logs"
backup_path   = f"{work_path}/backup_scripts/{filter_version}"

# creating folders and copying scripts
print("creating", dag_path)
os.system(f"mkdir -p {dag_path}")
os.system(f"mkdir -p {log_dir}")
os.system(f"mkdir -p {backup_path}")
os.system(f"cp filter_hese.sub {dag_path}")

# backup scripts
os.system(f"cp {work_path}/filter_hese.py {backup_path}")
os.system(f"cp {work_path}/filter_hese.sh {backup_path}")
os.system(f"cp {work_path}/filter_hese.sub {backup_path}")

# create the dag job
outfile = open(f"{dag_path}/submit.dag", 'w')

for simulation_name in simulation_datasets:
    
    simulation_subfolders = simulation_datasets[simulation_name]['subfolders']
    simulation_flavor = simulation_datasets[simulation_name]["flavor"]
    simulation_dataset = simulation_datasets[simulation_name]['dataset']

    for simulation_subfolder in simulation_subfolders:

        JOBID = f"{simulation_dataset}_{simulation_subfolder}"

        # fixed paths
        filter_in_path = f"/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator/{simulation_dataset}/{simulation_subfolder}"

        filter_out_path = f"/data/user/tvaneede/GlobalFit/reco_processing/filtering/output/{filter_version}/{simulation_dataset}/{simulation_subfolder}"

        os.system(f"mkdir -p {filter_out_path}")

        outfile.write(f"JOB {JOBID} filter_hese.sub\n")
        outfile.write(f'VARS {JOBID} LOGDIR="{log_dir}"\n')
        outfile.write(f'VARS {JOBID} JOBID="{JOBID}"\n')
        outfile.write(f'VARS {JOBID} INPUTPATH="{filter_in_path}"\n')
        outfile.write(f'VARS {JOBID} OUTPUTPATH="{filter_out_path}"\n')

if submit_jobs:

    os.chdir(dag_path)
    print(f"Changed directory to: {dag_path}")

    # Run the script and capture both stdout and stderr
    process = subprocess.run(
        "condor_submit_dag submit.dag", 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True  # Ensures output is in string format
    )

    # Log output and errors
    print("STDOUT:\n", process.stdout)
    print("STDERR:\n", process.stderr)
    print("Exit Code:", process.returncode)
