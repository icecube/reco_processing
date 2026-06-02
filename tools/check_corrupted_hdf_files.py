import sys, os, glob
import subprocess
import re
import pandas as pd
import tables

path = "/data/sim/IceCube/2023/filtered/finallevel/northern_tracks/neutrino-generator/{dataset}/"

datasets = ["23520","23521","23522","23523","23524","23525","23526","23527","23528","23529"]

for dataset in datasets:
    corrupted = []
    subfolder_path = path.format(dataset=dataset)
    print(10*"=",dataset)
    folders = [
        name for name in os.listdir(subfolder_path)
        if os.path.isdir(os.path.join(subfolder_path, name))
    ]
    nfolders = len(folders)
    count = 0
    for folder in folders:
        # count += len([f for f in glob.glob(f"{subfolder_path}/{folder}/final_cascade/*.i3.zst") if os.path.isfile(f)])
        files = [f for f in glob.glob(f"{subfolder_path}/{folder}/*.hdf") if os.path.isfile(f)]
        for file in files:
            try: 
                # x = pd.read_hdf(file)
                x = tables.open_file(file,"r")
                x.close()
            except:
                print(file)
                corrupted.append(file)

    print("n corrupted", len(corrupted), "of", len(files))
    print(corrupted)


