import sys, os, glob
import subprocess
import re

# Append the custom module path
sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")

# Import the datasets module
from datasets import datasets

# set the inputs
reco_version = "muongun"

# Dynamically select the desired dataset
simulation_datasets = getattr(datasets, reco_version)

# fixed paths
dag_base_path = "/scratch/tvaneede/reco/run_taupede_muon"
work_path = "/data/user/tvaneede/GlobalFit/reco_processing/muons/cascade"

submit_jobs = True # actually submit the dag jobs

# fixed dag paths
dag_name = f"reco_dag_{reco_version}_cascade"

dag_path      = f"{dag_base_path}/{reco_version}/{dag_name}"
log_dir       = f"{dag_path}/logs"

# creating folders and copying scripts
print("creating", dag_path)
os.system(f"mkdir -p {dag_path}")
os.system(f"mkdir -p {log_dir}")
os.system(f"cp run_taupede.sub {dag_path}")

# create the dag job
outfile = open(f"{dag_path}/submit.dag", 'w')

JOBS = []

for simulation_name in ["MuonGun_lowE", "MuonGun_midE", "MuonGun_highE"]:
    
    simulation_subfolders = simulation_datasets[simulation_name]['subfolders']
    simulation_flavor = simulation_datasets[simulation_name]["flavor"]
    simulation_dataset = simulation_datasets[simulation_name]['dataset']
    cascade_finallevel_path = simulation_datasets[simulation_name]['cascade_finallevel_path']
    cascade_reco_path = simulation_datasets[simulation_name]['cascade_reco_path']

    for simulation_subfolder in simulation_subfolders:

        for subclass in ["final_cascade", "final_hybrid", "final_muon"]:

            # fixed paths
            reco_input_path = f"{cascade_finallevel_path}/{simulation_dataset}/{simulation_subfolder}/{subclass}"

            reco_out_path = f"{cascade_reco_path}/{simulation_dataset}/{simulation_subfolder}/{subclass}"

            infiles_list = glob.glob(f"{reco_input_path}/*.i3.zst")

            filename = f"Finallevel_IC86.2016_MuonGun.{simulation_dataset}.{simulation_subfolder}.i3.zst"
            JOBID = f'{simulation_dataset}.{simulation_subfolder}.{subclass}'

            outfile.write(f"JOB {JOBID} run_taupede.sub\n")
            outfile.write(f'VARS {JOBID} LOGDIR="{log_dir}"\n')
            outfile.write(f'VARS {JOBID} JOBID="{JOBID}"\n')
            outfile.write(f'VARS {JOBID} INPATH="{reco_input_path}"\n')
            outfile.write(f'VARS {JOBID} INFILE="{filename}"\n')
            outfile.write(f'VARS {JOBID} OUTPATH="{reco_out_path}"\n')

            JOBS.append(JOBID)

    #         break
    #     break
    # break

print(f"creating {len(JOBS)}")

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
