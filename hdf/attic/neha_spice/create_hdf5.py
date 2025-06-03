import sys, os, glob
import subprocess
import re
from simulation_datasets_neha import simulation_datasets

reco_version = "neha_spice"

hdf_outpath = f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/{reco_version}"

os.system(f"mkdir -p {hdf_outpath}")

for simulation_name in simulation_datasets:

    print("Lets do", simulation_name)
    
    simulation_subfolders = simulation_datasets[simulation_name]['subfolders']
    simulation_flavor = simulation_datasets[simulation_name]["flavor"]
    simulation_dataset = simulation_datasets[simulation_name]['dataset']

    cmd = ["python", "/data/user/tvaneede/GlobalFit/reco_processing/hdf/to_hdf5.py", "-o", f"{hdf_outpath}/{simulation_flavor}_{simulation_dataset}.h5"]

    print("subfolders", simulation_subfolders)

    for simulation_subfolder in simulation_subfolders:

        reco_inpath = f"/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline/{simulation_dataset}/{simulation_subfolder}"

        infiles_list = glob.glob(f"{reco_inpath}/Reco_{simulation_flavor}_*.i3.bz2")
        print(f"found {len(infiles_list)} files")

        for infile in infiles_list: 
            cmd += [f"{infile}"]

    print("finished, running cmd")
    result = subprocess.run(cmd, capture_output=True, text=True)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

