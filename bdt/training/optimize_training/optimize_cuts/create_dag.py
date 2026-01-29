import sys, os, glob
import subprocess
import re

# version
version_name = "900steps_100fits_ibr_idc"

# fixed paths
dag_base_path = "/scratch/tvaneede/optimize_cuts"
work_path = "/data/user/tvaneede/GlobalFit/reco_processing/bdt/training/optimize_training/optimize_cuts"

submit_jobs = True # actually submit the dag jobs

# fixed dag paths
dag_path      = f"{dag_base_path}/{version_name}"
log_dir       = f"{dag_path}/logs"

# creating folders and copying scripts
print("creating", dag_path)
os.system(f"mkdir -p {dag_path}")
os.system(f"mkdir -p {log_dir}")
os.system(f"cp optimize_cuts.sub {dag_path}")

outfile = open(f"{dag_path}/submit.dag", 'w')

sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing/bdt/training/optimize_training")
from features_list_dict import features_list_dict
from flux_model_dict import flux_model_dict
from model_configs_dict import model_configs_dict

for model_configs_name in model_configs_dict:
    for flux_model_name in flux_model_dict:
        for features_list_name in features_list_dict:

            JOBID = f"mcd-{model_configs_name}_flux-{flux_model_name}_feat-{features_list_name}"

            outdir = f"{work_path}/output/{version_name}/{JOBID}"

            # create the dag job
            outfile.write(f"JOB {JOBID} optimize_cuts.sub\n")
            outfile.write(f'VARS {JOBID} LOGDIR="{log_dir}"\n')
            outfile.write(f'VARS {JOBID} JOBID="{JOBID}"\n')
            outfile.write(f'VARS {JOBID} OUTDIR="{outdir}"\n')
            outfile.write(f'VARS {JOBID} MCD="{model_configs_name}"\n')
            outfile.write(f'VARS {JOBID} FLUX="{flux_model_name}"\n')
            outfile.write(f'VARS {JOBID} FEAT="{features_list_name}"\n')

    #         break
    #     break
    # break

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
