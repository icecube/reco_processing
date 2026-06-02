#!/usr/bin/env python3
import sys, os, glob
import subprocess

sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing/data/hese")
from sum_livetimes import get_level, get_config

RUNINFO_BASE = "/data/exp/IceCube"


def parse_runinfo(path):
    """Return list of (run_num, out_dir) for good runs (Good_i3 == 1)."""
    runs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or not line[0].isdigit():
                continue
            parts = line.split()
            if len(parts) < 8:
                continue
            run = int(parts[0])
            good_i3 = int(parts[1])
            out_dir = parts[7]
            if good_i3 == 1:
                runs.append((run, out_dir))
    return runs


def find_gcd(run_dir):
    """Find the GCD file in a run directory."""
    gcds = glob.glob(os.path.join(run_dir, "*GCD*.i3*"))
    if not gcds:
        return None
    return sorted(gcds)[0]


# fixed paths
filter_version = "v2"
dag_base_path = "/scratch/tvaneede/reco/hese_data_filter"
work_path = "/data/user/tvaneede/GlobalFit/reco_processing/data/hese/filter"

submit_jobs = True  # set to True to actually submit

dag_name = f"filter_dag_hese_data_{filter_version}_2ndbatch"
dag_path = f"{dag_base_path}/{dag_name}"
log_dir = f"{dag_path}/logs"

print("Creating", dag_path)
os.system(f"mkdir -p {dag_path}")
os.system(f"mkdir -p {log_dir}")
os.system(f"cp {work_path}/filter_HESE.sub {dag_path}")

outfile = open(f"{dag_path}/submit.dag", 'w')

JOBS = []

# for year in range(2010, 2023):
# for year in range(2010, 2016):
for year in range(2017, 2023):
    level = get_level(year)
    config = get_config(year)
    ds_year = f"{config}_{year}"

    runinfo_path = os.path.join(
        RUNINFO_BASE, str(year), "filtered", level,
        f"{config}_{year}_GoodRunInfo.txt"
    )
    if not os.path.exists(runinfo_path):
        print(f"WARNING: not found: {runinfo_path}")
        continue

    runs = parse_runinfo(runinfo_path)
    print(f"{ds_year}: {len(runs)} good runs")

    for run_num, out_dir in runs:
        run_dir = out_dir.rstrip('/')

        gcd_file = find_gcd(run_dir)
        if gcd_file is None:
            print(f"WARNING: no GCD found in {run_dir}, skipping")
            continue

        filter_out_dir = f"{work_path}/output/{filter_version}/{ds_year}"
        os.system(f"mkdir -p {filter_out_dir}")
        output_file = f"{filter_out_dir}/Run{run_num:08d}.i3.zst"

        JOBID = f"{ds_year}_Run{run_num:08d}"

        outfile.write(f"JOB {JOBID} filter_HESE.sub\n")
        outfile.write(f'VARS {JOBID} LOGDIR="{log_dir}"\n')
        outfile.write(f'VARS {JOBID} JOBID="{JOBID}"\n')
        outfile.write(f'VARS {JOBID} RUNDIR="{run_dir}"\n')
        outfile.write(f'VARS {JOBID} GCDFILE="{gcd_file}"\n')
        outfile.write(f'VARS {JOBID} OUTPUTFILE="{output_file}"\n')
        outfile.write('\n')

        JOBS.append(JOBID)

outfile.close()
print(f"Created {len(JOBS)} jobs in {dag_path}/submit.dag")

if submit_jobs:
    os.chdir(dag_path)
    process = subprocess.run(
        "condor_submit_dag submit.dag",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print("STDOUT:\n", process.stdout)
    print("STDERR:\n", process.stderr)
    print("Exit Code:", process.returncode)
