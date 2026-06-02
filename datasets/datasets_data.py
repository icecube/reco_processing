
###
### v0 analysis
###

# number of files per level taken from print_files_per_hdf_dataset.py

burnsample = {}

burnsample["v0"] = { # 100 TeV - 1 EeV
    "dataset" : "v0",
    "subfolders" : [f"{i}" for i in range(2011, 2023)],
    "flavor" : "Data",
    "levels"  : {
        "level3_cascade_Taupede" : 0,
    },
}

