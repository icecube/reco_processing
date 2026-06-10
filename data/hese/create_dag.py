import sys, os, glob
import subprocess

# Append the custom module path
sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")

# fixed paths
dag_base_path = "/scratch/tvaneede/reco/hese_data"
work_path = "/data/user/tvaneede/GlobalFit/reco_processing/data/hese"

submit_jobs = True # actually submit the dag jobs

# data processing version
version = "v2_2016"

# fixed dag paths
dag_name = f"reco_dag_hese_data_{version}_2016_clean"

dag_path      = f"{dag_base_path}/{dag_name}"
log_dir       = f"{dag_path}/logs"

# creating folders and copying scripts
print("creating", dag_path)
os.system(f"mkdir -p {dag_path}")
os.system(f"mkdir -p {log_dir}")
os.system(f"cp reco.sub {dag_path}")

# create the dag job
outfile = open(f"{dag_path}/submit.dag", 'w')

JOBS = []

data_path = "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/data/hese/filter/output/v2/"

# Load livetime table
runs = {
    # "IC79_2010" : data_path,
    # "IC86_2011" : data_path,
    # "IC86_2012" : data_path,
    # "IC86_2013" : data_path,
    # "IC86_2014" : data_path,
    # "IC86_2015" : data_path,
    "IC86_2016" : data_path,
    # "IC86_2017" : data_path,
    # "IC86_2018" : data_path,
    # "IC86_2019" : data_path,
    # "IC86_2020" : data_path,
    # "IC86_2021" : data_path,
    # "IC86_2022" : data_path,
}

for data_year, data_path_tmp in runs.items():

    infile_path = f"{data_path_tmp}/{data_year}"
    infiles = sorted(glob.glob(f"{infile_path}/*.i3.zst"))

    reco_out_path = f"{work_path}/output/{version}/{data_year}"
    os.system(f"mkdir -p {reco_out_path}")

    for infile in infiles:
        file_stem = os.path.basename(infile).replace('.i3.zst', '')

        # DAGMan job IDs cannot contain dots
        safe_stem = file_stem.replace('.', '_')
        JOBID = f'{data_year}_{safe_stem}'

        outfile.write(f"JOB {JOBID} reco.sub\n")
        outfile.write(f'VARS {JOBID} LOGDIR="{log_dir}"\n')
        outfile.write(f'VARS {JOBID} JOBID="{JOBID}"\n')
        outfile.write(f'VARS {JOBID} INFILE="{infile}"\n')
        outfile.write(f'VARS {JOBID} OUTPATH="{reco_out_path}"\n')

        JOBS.append(JOBID)

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
