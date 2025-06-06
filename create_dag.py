import sys, os, glob
import subprocess
import re
from simulation_datasets import simulation_datasets

# set the inputs
reco_version = "v1"
filter_version = "v1"
icemodel = "ftp-v3"

# fixed paths
dag_base_path = "/scratch/tvaneede/reco/run_taupede_tianlu"
work_path = "/data/user/tvaneede/GlobalFit/reco_processing/"

nfiles = 1000 # process x files per subfolder
submit_jobs = True # actually submit the dag jobs

for simulation_name in simulation_datasets:
    
    simulation_subfolders = simulation_datasets[simulation_name]['subfolders']
    simulation_flavor = simulation_datasets[simulation_name]["flavor"]
    simulation_dataset = simulation_datasets[simulation_name]['dataset']

    for simulation_subfolder in simulation_subfolders:

        # fixed paths
        reco_input_path = f"/data/user/tvaneede/GlobalFit/reco_processing/filtering/output/{filter_version}/{simulation_dataset}/{simulation_subfolder}"

        reco_out_path = f"{work_path}/output/{reco_version}/{simulation_dataset}/{simulation_subfolder}"

        # fixed dag paths
        dag_name = f"reco_dag_{reco_version}_{simulation_dataset}_{simulation_subfolder}"

        dag_path      = f"{dag_base_path}/{reco_version}/{dag_name}"
        log_dir       = f"{dag_path}/logs"
        backup_path   = f"{work_path}/backup_scripts/{reco_version}"

        # creating folders and copying scripts
        print("creating", dag_path)
        os.system(f"mkdir -p {dag_path}")
        os.system(f"mkdir -p {log_dir}")
        os.system(f"mkdir -p {reco_out_path}")
        os.system(f"mkdir -p {backup_path}")
        os.system(f"cp reco.sub {dag_path}")

        # backup scripts
        os.system(f"cp {work_path}/reco.sub {backup_path}")
        os.system(f"cp {work_path}/wrapper.sh {backup_path}")

        # create the dag job
        outfile = open(f"{dag_path}/submit.dag", 'w')

        infiles_list = glob.glob(f"{reco_input_path}/Level3_{simulation_flavor}_*.i3.zst")
        print(f"found {len(infiles_list)} files")

        infiles_list = sorted(infiles_list, key=lambda x: int(re.search(r'\.(\d{6})\.i3\.zst$', x).group(1)))

        i = 0
        for INFILES in infiles_list:

            filename = os.path.basename(INFILES)
            JOBID = filename.split("_")[2] # gives the run number
            OUTFILE = f"{reco_out_path}/Reco_{simulation_flavor}_{JOBID}_out.i3.bz2"

            outfile.write(f"JOB {JOBID} reco.sub\n")
            outfile.write(f'VARS {JOBID} LOGDIR="{log_dir}"\n')
            outfile.write(f'VARS {JOBID} JOBID="{JOBID}"\n')
            outfile.write(f'VARS {JOBID} INFILES="{INFILES}"\n')
            outfile.write(f'VARS {JOBID} OUTFILE="{OUTFILE}"\n')

            i+=1
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
