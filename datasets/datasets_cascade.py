
###
### v0 analysis
###

# number of files per level taken from print_files_per_hdf_dataset.py

cascade_iceprod_v0 = {}

cascade_iceprod_v0["MuonGun_highE_taureco"] = { # 100 TeV - 1 EeV
    "dataset" : "21315",
    "subfolders" : ["all"],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level7_cascade_MuonGun" : 0
    },
}

cascade_iceprod_v0["MuonGun_midE_taureco"] = { # 10 TeV - 100 TeV
    "dataset" : "21316",
    "subfolders" : ["all"],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level7_cascade_MuonGun" : 0
    },
}

cascade_iceprod_v0["MuonGun_lowE_taureco"] = { # 5 TeV - 10 TeV
    "dataset" : "21317",
    "subfolders" : ["all"],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level7_cascade_MuonGun" : 0
    },
}

cascade_iceprod_v0["MuonGun_highE"] = { # 100 TeV - 1 EeV
    "dataset" : "21315",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level6_cascade_MuonGun" : 0, "level6_muon_MuonGun" : 0, "level6_hybrid_MuonGun" : 0,
    },
}

cascade_iceprod_v0["MuonGun_midE"] = { # 10 TeV - 100 TeV
    "dataset" : "21316",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 40000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level6_cascade_MuonGun" : 0, "level6_muon_MuonGun" : 0, "level6_hybrid_MuonGun" : 0,
    },
}

cascade_iceprod_v0["MuonGun_lowE"] = { # 5 TeV - 10 TeV
    "dataset" : "21317",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level6_cascade_MuonGun" : 0, "level6_muon_MuonGun" : 0, "level6_hybrid_MuonGun" : 0, 
    },
}

cascade_iceprod_v0["MuonGun_lowlowE"] = { # 1 TeV - 5 TeV
    "dataset" : "21318",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 100000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level6_cascade_MuonGun" : 0, "level6_muon_MuonGun" : 0, "level6_hybrid_MuonGun" : 0
    },
}

cascade_iceprod_v0["MuonGun_lowlowlowE"] = { # 700 GeV - 1 TeV
    "dataset" : "21319",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 100000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level6_cascade_MuonGun" : 0, "level6_muon_MuonGun" : 0, "level6_hybrid_MuonGun" : 0
    },
}

cascade_iceprod_v0["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 19913, "level6_muon" : 19913, "level6_hybrid" : 19913, "level7_cascade" : 19850
    },
}

cascade_iceprod_v0["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 3974, "level6_muon" : 3974, "level6_hybrid" : 3974, "level7_cascade" : 3962
    },
}

cascade_iceprod_v0["NuE_lowE"] = {
    "dataset" : "22614",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 999, "level6_muon" : 999, "level6_hybrid" : 999
    },
}


cascade_iceprod_v0["NuTau_lowE"] = {
    "dataset" : "22633",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 1000, "level6_muon" : 1000, "level6_hybrid" : 1000
    },
}

cascade_iceprod_v0["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 4000, "level6_muon" : 4000, "level6_hybrid" : 4000, "level7_cascade" : 3993
    },
}

cascade_iceprod_v0["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 19994, "level6_muon" : 19994, "level6_hybrid" : 19994, "level7_cascade" : 19932
    },
}


cascade_iceprod_v0["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 14996, "level6_muon" : 14996, "level6_hybrid" : 14996, "level7_cascade" : 14972
    },
}

cascade_iceprod_v0["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 5000, "level6_muon" : 5000, "level6_hybrid" : 5000, "level7_cascade" : 4992
    },
}

cascade_iceprod_v0["NuMu_lowE"] = {
    "dataset" : "22646",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 8000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 7635, "level6_muon" : 7635, "level6_hybrid" : 7635
    },
}
