import sys, os, glob
import subprocess
import re

# path = "/data/ana/analyses/diffuse/cascades-nutau/sim/nugen/taupede/snowstorm/ftp_reco/{dataset}/"

# datasets = ["22644","22645","22646","22614","22613","22612","22633","22634","22635"]
# datasets = ["22684","22685","22686","22687","22688","22689","22690","22691","22692"]

path = "/data/sim/IceCube/2023/filtered/finallevel/northern_tracks/neutrino-generator/{dataset}/"

datasets = ["23520","23521","23522","23523","23524","23525","23526","23527","23528","23529"]

for dataset in datasets:
    subfolder_path = path.format(dataset=dataset)
    print(10*"=",dataset)
    folders = [
        name for name in os.listdir(subfolder_path)
        if os.path.isdir(os.path.join(subfolder_path, name))
    ]
    nfolders = len(folders)
    # print(folders)
    count = 0
    for folder in folders:
        # count += len([f for f in glob.glob(f"{subfolder_path}/{folder}/final_cascade/*.i3.zst") if os.path.isfile(f)])
        count += len([f for f in glob.glob(f"{subfolder_path}/{folder}/*.hdf") if os.path.isfile(f)])
    print("nfolders", nfolders, "count", count)


