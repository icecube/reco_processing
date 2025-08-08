import sys, os, glob
import subprocess
import re

# Append the custom module path
sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")

# Import the datasets module
from datasets import datasets

# set the inputs
reco_input_version = "v5"
evtgen_version = "v2"

# Dynamically select the desired dataset
simulation_datasets = getattr(datasets, reco_input_version)

# fixed paths
dag_base_path = "/scratch/tvaneede/reco/run_evtgen_ftp"
work_path = "/data/user/tvaneede/GlobalFit/reco_processing/evtgen"

nfiles = 10000 # process x files per subfolder
submit_jobs = True # actually submit the dag jobs

for simulation_name in ["NuMu_midE", "NuMu_highE", "NuE_midE", "NuE_highE"]:
# for simulation_name in ["NuTau_midE","NuTau_highE"]:
# for simulation_name in ["NuE_midE","NuE_highE"]:
# for simulation_name in ["NuMu_midE","NuMu_highE"]:
    
    simulation_subfolders = simulation_datasets[simulation_name]['subfolders']
    simulation_flavor = simulation_datasets[simulation_name]["flavor"]
    simulation_dataset = simulation_datasets[simulation_name]['dataset']
    simulation_path = simulation_datasets[simulation_name]['reco_base_out_path']

    for simulation_subfolder in simulation_subfolders:

        # fixed paths
        reco_input_path = f"{simulation_path}/{simulation_dataset}/{simulation_subfolder}"

        reco_out_path = f"{work_path}/output/{evtgen_version}/{simulation_dataset}/{simulation_subfolder}"

        # fixed dag paths
        dag_name = f"reco_evtgen_dag_{evtgen_version}_{simulation_dataset}_{simulation_subfolder}"

        dag_path      = f"{dag_base_path}/{evtgen_version}/{dag_name}"
        log_dir       = f"{dag_path}/logs"
        backup_path   = f"{work_path}/backup_scripts/{evtgen_version}"

        # creating folders and copying scripts
        print("creating", dag_path)
        os.system(f"mkdir -p {dag_path}")
        os.system(f"mkdir -p {log_dir}")
        os.system(f"mkdir -p {reco_out_path}")
        os.system(f"mkdir -p {backup_path}")
        os.system(f"cp run_event_generator.sub {dag_path}")

        # backup scripts
        os.system(f"cp {work_path}/run_event_generator.py {backup_path}")
        os.system(f"cp {work_path}/run_event_generator.sh {backup_path}")
        os.system(f"cp {work_path}/run_event_generator.sub {backup_path}")

        # create the dag job
        outfile = open(f"{dag_path}/submit.dag", 'w')

        infiles_list = glob.glob(f"{reco_input_path}/Reco_{simulation_flavor}_*.i3.bz2")
        print(f"found {len(infiles_list)} files")

        infiles_list = sorted(
            infiles_list,
            key=lambda x: int(re.search(r'\.(\d{6})\.i3\.zst_out\.i3\.bz2$', x).group(1))
        )
        
        for i,INFILES in enumerate(infiles_list):

            filename = os.path.basename(INFILES)
            JOBID = filename.split("_")[2] # gives the run number
            OUTFILE = f"{reco_out_path}/Reco_{simulation_flavor}_{JOBID}_out.i3.bz2"

            outfile.write(f"JOB {JOBID} run_event_generator.sub\n")
            outfile.write(f'VARS {JOBID} LOGDIR="{log_dir}"\n')
            outfile.write(f'VARS {JOBID} JOBID="{JOBID}"\n')
            outfile.write(f'VARS {JOBID} Inputfile="{INFILES}"\n')
            outfile.write(f'VARS {JOBID} Outputfile="{OUTFILE}"\n')

            if i == nfiles: break

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
