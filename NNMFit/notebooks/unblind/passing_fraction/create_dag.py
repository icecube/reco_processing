#!/usr/bin/env python3
import os
import subprocess

SCRIPT_DIR = "/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/unblind/passing_fraction"

dag_base_path = "/scratch/tvaneede/passing_fraction"
dag_name      = "compare_pf_dag"
dag_path      = f"{dag_base_path}/{dag_name}"
log_dir       = f"{dag_path}/logs"

submit_jobs = False  # set True to actually submit

COMBOS = [
    ("conv", "nu_mu"),
    ("conv", "nu_mubar"),
    ("conv", "nu_e"),
    ("conv", "nu_ebar"),
    ("pr",   "nu_mu"),
    ("pr",   "nu_mubar"),
    ("pr",   "nu_e"),
    ("pr",   "nu_ebar"),
]

os.makedirs(dag_path, exist_ok=True)
os.makedirs(log_dir,  exist_ok=True)

# Copy the DAG-compatible submit file next to the .dag file
os.system(f"cp {SCRIPT_DIR}/compare_pf_dag.sub {dag_path}/")

dag_file = f"{dag_path}/submit.dag"
with open(dag_file, "w") as f:
    for flux_type, flavor in COMBOS:
        JOBID = f"{flux_type}_{flavor}"
        f.write(f"JOB {JOBID} compare_pf_dag.sub\n")
        f.write(f'VARS {JOBID} LOGDIR="{log_dir}"\n')
        f.write(f'VARS {JOBID} JOBID="{JOBID}"\n')
        f.write(f'VARS {JOBID} flux_type="{flux_type}"\n')
        f.write(f'VARS {JOBID} flavor="{flavor}"\n')
        f.write("\n")

print(f"Created {len(COMBOS)} jobs in {dag_file}")
print(f"Logs will go to: {log_dir}")
print(f"\nTo submit:\n  cd {dag_path} && condor_submit_dag submit.dag")

if submit_jobs:
    os.chdir(dag_path)
    process = subprocess.run(
        "condor_submit_dag submit.dag",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    print("STDOUT:\n", process.stdout)
    print("STDERR:\n", process.stderr)
    print("Exit Code:", process.returncode)
