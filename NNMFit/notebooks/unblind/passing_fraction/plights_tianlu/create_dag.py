#!/usr/bin/env python3
"""
Create a HTCondor DAGMan file for the nuVeto passing-fraction grid calculation
using depth-dependent prpl files from plights_tianlu/prpl_output/.

One job per (depth, cos_theta) grid point; all 8 neutrino kinds per job.
Set submit_jobs = True to actually submit after writing the DAG.

Usage:
    python create_dag.py
"""

import os
import pickle
import shutil
import subprocess

import numpy as np

# ── Grid definition ────────────────────────────────────────────────────────────
DEPTH_GRID     = np.linspace(1e3, 3e3, 11)    # metres, same as nlad's HESE grid
COS_THETA_GRID = np.linspace(0.05, 1.0, 21)

NEUTRINO_KIND = (
    "conv_nu_mu,conv_nu_mubar,conv_nu_e,conv_nu_ebar,"
    "pr_nu_mu,pr_nu_mubar,pr_nu_e,pr_nu_ebar"
)

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR = "/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/unblind/passing_fraction/plights_tianlu"
PRPL_DIR   = os.path.join(SCRIPT_DIR, "prpl_output")

RESULTS_TAG = "hese_plight_11dep_21cth_51ene"
OUTPUT_DIR  = os.path.join(SCRIPT_DIR, "pf_grid", RESULTS_TAG)
SCRATCH_DIR = f"/scratch/tvaneede/nuveto_plight/{RESULTS_TAG}"
LOG_DIR     = os.path.join(SCRATCH_DIR, "logs")

JOB_FILE    = os.path.join(SCRIPT_DIR, "submit_nuveto.sub")

# ── Control ────────────────────────────────────────────────────────────────────
submit_jobs = False   # set True to condor_submit_dag after writing

# ── Setup directories ──────────────────────────────────────────────────────────
os.makedirs(OUTPUT_DIR,  exist_ok=True)
os.makedirs(LOG_DIR,     exist_ok=True)

print(f"Output dir : {OUTPUT_DIR}")
print(f"Log dir    : {LOG_DIR}")
print(f"Jobs       : {len(DEPTH_GRID) * len(COS_THETA_GRID)}")
print()

# ── Save grid info for pf_grid_fitter.py ──────────────────────────────────────
info_dict = {"depth_grid": DEPTH_GRID, "cos_theta_grid": COS_THETA_GRID}
with open(os.path.join(OUTPUT_DIR, "info.pickle"), "wb") as fh:
    pickle.dump(info_dict, fh)
print("Saved info.pickle")

# ── Copy submit file to scratch (DAG needs it co-located or absolute path) ─────
job_file_local = os.path.join(SCRATCH_DIR, os.path.basename(JOB_FILE))
shutil.copy(JOB_FILE, job_file_local)
print(f"Copied submit file → {job_file_local}")

# ── Write DAG ─────────────────────────────────────────────────────────────────
dag_path = os.path.join(SCRATCH_DIR, "submit.dag")
with open(dag_path, "w") as dag:
    for depth in DEPTH_GRID:
        for cos_theta in COS_THETA_GRID:

            name = f"depth_{depth:.0f}_cos_theta_{cos_theta:.2f}"

            output_file = os.path.join(OUTPUT_DIR, f"{name}.pickle")

            pars  = f'jobid="$(JOB)" '
            pars += f'cos_theta="{cos_theta}" '
            pars += f'output_file="{output_file}" '
            pars += f'neutrino_kind="{NEUTRINO_KIND}" '
            pars += f'depth="{depth}" '
            pars += f'prpl_dir="{PRPL_DIR}" '
            pars += f'logdir="{LOG_DIR}" '
            pars += f'outdir="{LOG_DIR}" '

            dag.write(f"JOB {name} {job_file_local}\n")
            dag.write(f"VARS {name} {pars}\n")
            dag.write("\n")

print(f"DAG written → {dag_path}")

# ── Submit ─────────────────────────────────────────────────────────────────────
if submit_jobs:
    print("Submitting …")
    subprocess.run(["condor_submit_dag", dag_path], check=True)
else:
    print()
    print("submit_jobs=False — to submit, run:")
    print(f"  condor_submit_dag {dag_path}")
