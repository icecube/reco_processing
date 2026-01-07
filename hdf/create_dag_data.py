import sys, os, glob
import subprocess
import re

# Append the custom module path
sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")

# Import the datasets module
from datasets import datasets_data as datasets

# set the inputs
reco_version = "burnsample"
simulation_name = "v0"

# Dynamically select the desired dataset
simulation_datasets = getattr(datasets, reco_version)

# fixed paths
dag_base_path = "/scratch/tvaneede/reco/hdf_iceprod"
work_path = "/data/user/tvaneede/GlobalFit/reco_processing/hdf"
hdf_outpath = f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/{reco_version}_{simulation_name}"

os.system(f"mkdir -p {hdf_outpath}")

submit_jobs = True # actually submit the dag jobs

# fixed dag paths
dag_path      = f"{dag_base_path}/{reco_version}_{simulation_name}"
log_dir       = f"{dag_path}/logs"

# creating folders and copying scripts
print("creating", dag_path)
os.system(f"mkdir -p {dag_path}")
os.system(f"mkdir -p {log_dir}")
os.system(f"mkdir -p {hdf_outpath}")
os.system(f"cp to_hdf5.sub {dag_path}")

outfile = open(f"{dag_path}/submit.dag", 'w')

def get_reco_file_path(level, subfolder):
    if level == "level3_cascade_Taupede": return f"/data/user/tvaneede/GlobalFit/reco_processing/burn/output/{subfolder}/Taupede_ibr_idc"

simulation_subfolders = simulation_datasets[simulation_name]['subfolders']
simulation_flavor = simulation_datasets[simulation_name]["flavor"] # data
simulation_dataset = simulation_datasets[simulation_name]['dataset'] # v_x
simulation_levels = simulation_datasets[simulation_name]['levels']

for simulation_subfolder in simulation_subfolders:

    for simulation_level in simulation_levels:

        outfile_path = f"{hdf_outpath}/{simulation_level}_{simulation_flavor}_{simulation_dataset}_{simulation_subfolder}.h5"
        reco_input_path = get_reco_file_path(simulation_level, simulation_subfolder)

        # create the dag job
        JOBID = f"{simulation_level}_{simulation_flavor}_{simulation_dataset}_{simulation_subfolder}"

        outfile.write(f"JOB {JOBID} to_hdf5.sub\n")
        outfile.write(f'VARS {JOBID} LOGDIR="{log_dir}"\n')
        outfile.write(f'VARS {JOBID} JOBID="{JOBID}"\n')
        outfile.write(f'VARS {JOBID} INPATH="{reco_input_path}"\n')
        outfile.write(f'VARS {JOBID} OUTFILE="{outfile_path}"\n')
        outfile.write(f'VARS {JOBID} FLAVOR="{simulation_flavor}"\n')
    
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
