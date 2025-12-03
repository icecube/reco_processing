from copy import deepcopy

###
### base hese class
###

hese = {}

hese["MuonGun_highE"] = { # 100 TeV - 1 EeV
    "dataset" : "21315",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "HESE_MuonGun" : 0
    },
}

hese["MuonGun_midE"] = { # 10 TeV - 100 TeV
    "dataset" : "21316",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 40000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "HESE_MuonGun" : 0
    },
}

hese["MuonGun_lowE"] = { # 5 TeV - 10 TeV
    "dataset" : "21317",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "HESE_MuonGun" : 0
    },
}

hese["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "HESE" : 15739
    },
}

hese["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : { 
         "HESE" : 3418
    },
}

hese["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE" : 3515
    },
}

hese["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE" : 15218
    },
}

hese["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE" : 12265
    },
}

hese["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE" : 4371
    },
}

## v0

hese_noLengthEnergy = deepcopy(hese)

hese_withLengthEnergy = deepcopy(hese)