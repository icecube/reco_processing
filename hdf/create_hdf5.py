import sys, os, glob
import subprocess
import re

sys.path.append('/data/user/tvaneede/GlobalFit/reco_processing')
from simulation_datasets import simulation_datasets

reco_version = "v7.0"

hdf_outpath = f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/{reco_version}"

os.system(f"mkdir -p {hdf_outpath}")

for simulation_name in simulation_datasets:

    print("Lets do", simulation_name)
    
    simulation_subfolders = simulation_datasets[simulation_name]['subfolders']
    simulation_flavor = simulation_datasets[simulation_name]["flavor"]
    simulation_dataset = simulation_datasets[simulation_name]['dataset']

    cmd = f"python /data/user/tvaneede/GlobalFit/reco_processing/hdf/to_hdf5.py -o {hdf_outpath}/{simulation_flavor}_{simulation_dataset}.h5 "

    for simulation_subfolder in simulation_subfolders:

        reco_inpath = f"/data/user/tvaneede/GlobalFit/reco_processing/output/{reco_version}/{simulation_dataset}/{simulation_subfolder}"

        infiles_list = glob.glob(f"{reco_inpath}/Reco_{simulation_flavor}_*.i3.bz2")
        print(f"found {len(infiles_list)} files")

        for infile in infiles_list: cmd += f"{infile} "

    print("finished")
    os.system(cmd)

