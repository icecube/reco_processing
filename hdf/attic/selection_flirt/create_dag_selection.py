import sys, os, glob
import subprocess
import re

# Append the custom module path
sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")

# Import the datasets module
from datasets import datasets_hese as datasets

# set the inputs
simulation_level = "HESE"
selection = "noLengthEnergy"
reco_version = f"hese_{selection}"
channels = {
    1 : "cascade",
    2 : "double",
    3 : "track"
}

# Dynamically select the desired dataset
simulation_datasets = getattr(datasets, reco_version)

# fixed paths
dag_base_path = "/scratch/tvaneede/reco/hdf_iceprod"
work_path = "/data/user/tvaneede/GlobalFit/reco_processing/hdf"
hdf_outpath = f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/{reco_version}"

os.system(f"mkdir -p {hdf_outpath}")
for channel_id,channel_name in channels.items(): os.system(f"mkdir -p {hdf_outpath}/{channel_name}")

submit_jobs = True # actually submit the dag jobs

# fixed dag paths
dag_path      = f"{dag_base_path}/{reco_version}"
log_dir       = f"{dag_path}/logs"

# creating folders and copying scripts
print("creating", dag_path)
os.system(f"mkdir -p {dag_path}")
os.system(f"mkdir -p {log_dir}")
os.system(f"mkdir -p {hdf_outpath}")
os.system(f"cp to_hdf5_selection.sub {dag_path}")

outfile = open(f"{dag_path}/submit.dag", 'w')

def get_reco_file_path(level, year, dataset, subfolder):
    if level == "generated": return f"/data/sim/IceCube/{year}/generated/neutrino-generator/{dataset}/{subfolder}/"
    if level == "level2": return f"/data/sim/IceCube/{year}/filtered/level2/neutrino-generator/{dataset}/{subfolder}/"
    if level == "HESE": return f"/data/sim/IceCube/{year}/filtered/HESE/neutrino-generator/{dataset}/{subfolder}/"
    if level == "HESE_taupede": return f"/data/sim/IceCube/{year}/filtered/HESE/neutrino-generator/taupede/{dataset}/{subfolder}/"
    if level == "HESE_evtgen": return f"/data/sim/IceCube/{year}/filtered/HESE/neutrino-generator/evtgen/{dataset}/{subfolder}"
    if level == "level3_cascade": return f"/data/sim/IceCube/{year}/filtered/level3/cascade/neutrino-generator/{dataset}/{subfolder}/"
    if level == "level3_muon": return f"/data/sim/IceCube/{year}/filtered/level3/muon/neutrino-generator/{dataset}/{subfolder}/"
    if level == "level6_cascade": return f"/data/sim/IceCube/{year}/filtered/level6/cascade/neutrino-generator/cascade/{dataset}/{subfolder}/"
    if level == "level6_muon": return f"/data/sim/IceCube/{year}/filtered/level6/cascade/neutrino-generator/muon/{dataset}/{subfolder}/"
    if level == "level6_hybrid": return f"/data/sim/IceCube/{year}/filtered/level6/cascade/neutrino-generator/hybrid/{dataset}/{subfolder}/"
    if level == "level7_cascade": return f"/data/sim/IceCube/{year}/filtered/level7/cascade/neutrino-generator/cascade/{dataset}/{subfolder}/"
    if level == "level8_cascade": return f"/data/sim/IceCube/{year}/filtered/level8/cascade/neutrino-generator/cascade/{dataset}/{subfolder}/"
    # MuonGun
    if level == "level6_cascade_MuonGun": return f"/data/ana/analyses/diffuse/cascades/pass2/sim/mgun/finallevel/{dataset}/{subfolder}/final_cascade/"
    if level == "level6_muon_MuonGun": return f"/data/ana/analyses/diffuse/cascades/pass2/sim/mgun/finallevel/{dataset}/{subfolder}/final_muon/"
    if level == "level6_hybrid_MuonGun": return f"/data/ana/analyses/diffuse/cascades/pass2/sim/mgun/finallevel/{dataset}/{subfolder}/final_hybrid/"
    if level == "HESE_MuonGun": return f"/data/user/tvaneede/GlobalFit/reco_processing/muons/hese/output/{dataset}/EvtGen/"
    if level == "level7_cascade_MuonGun": return f"/data/user/tvaneede/GlobalFit/reco_processing/muons/cascade/output/{dataset}/final_cascade/EvtGen/"


for simulation_name in simulation_datasets:
    
    simulation_subfolders = simulation_datasets[simulation_name]['subfolders']
    simulation_flavor = simulation_datasets[simulation_name]["flavor"]
    simulation_dataset = simulation_datasets[simulation_name]['dataset']
    simulation_year = simulation_datasets[simulation_name]['year']
    simulation_levels = simulation_datasets[simulation_name]['levels']

    for simulation_subfolder in simulation_subfolders:

        for channel_id, channel_name in channels.items():

            outfile_path = f"{hdf_outpath}/{channel_name}/{simulation_level}_{simulation_flavor}_{simulation_dataset}_{simulation_subfolder}.h5"
            reco_input_path = get_reco_file_path(simulation_level, simulation_year, simulation_dataset, simulation_subfolder)

            # create the dag job
            JOBID = f"{simulation_level}_{simulation_flavor}_{simulation_dataset}_{simulation_subfolder}_{channel_name}"

            outfile.write(f"JOB {JOBID} to_hdf5_selection.sub\n")
            outfile.write(f'VARS {JOBID} LOGDIR="{log_dir}"\n')
            outfile.write(f'VARS {JOBID} JOBID="{JOBID}"\n')
            outfile.write(f'VARS {JOBID} INPATH="{reco_input_path}"\n')
            outfile.write(f'VARS {JOBID} OUTFILE="{outfile_path}"\n')
            outfile.write(f'VARS {JOBID} FLAVOR="{simulation_flavor}"\n')
            outfile.write(f'VARS {JOBID} SELECTION="{selection}"\n')
            outfile.write(f'VARS {JOBID} CHANNEL="{channel_id}"\n')
    
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
