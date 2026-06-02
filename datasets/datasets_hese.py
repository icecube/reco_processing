
###
### v0 analysis
###

# number of files per level taken from print_files_per_hdf_dataset.py

hese_iceprod_v0 = {}

hese_iceprod_v0["MuonGun_highE"] = { # 100 TeV - 1 EeV
    "dataset" : "21315",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level6_cascade_MuonGun" : 0, "level6_muon_MuonGun" : 0, "level6_hybrid_MuonGun" : 0, "HESE_MuonGun" : 0, "level7_cascade_MuonGun" : 0
    },
}

hese_iceprod_v0["MuonGun_midE"] = { # 10 TeV - 100 TeV
    "dataset" : "21316",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 40000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level6_cascade_MuonGun" : 0, "level6_muon_MuonGun" : 0, "level6_hybrid_MuonGun" : 0, "HESE_MuonGun" : 0, "level7_cascade_MuonGun" : 0
    },
}

hese_iceprod_v0["MuonGun_lowE"] = { # 5 TeV - 10 TeV
    "dataset" : "21317",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level6_cascade_MuonGun" : 0, "level6_muon_MuonGun" : 0, "level6_hybrid_MuonGun" : 0, "HESE_MuonGun" : 0, "level7_cascade_MuonGun" : 0
    },
}

hese_iceprod_v0["MuonGun_lowlowE"] = { # 1 TeV - 5 TeV
    "dataset" : "21318",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 100000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level6_cascade_MuonGun" : 0, "level6_muon_MuonGun" : 0, "level6_hybrid_MuonGun" : 0
    },
}

hese_iceprod_v0["MuonGun_lowlowlowE"] = { # 700 GeV - 1 TeV
    "dataset" : "21319",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 100000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level6_cascade_MuonGun" : 0, "level6_muon_MuonGun" : 0, "level6_hybrid_MuonGun" : 0
    },
}


hese_iceprod_v0["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 19913, "level6_muon" : 19913, "level6_hybrid" : 19913, "HESE" : 12828, "level7_cascade" : 18738
    },
}

hese_iceprod_v0["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 3974, "level6_muon" : 3974, "level6_hybrid" : 3974, "HESE" : 2964, "level7_cascade" : 3800
    },
}

hese_iceprod_v0["NuE_lowE"] = {
    "dataset" : "22614",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 999, "level6_muon" : 999, "level6_hybrid" : 999
    },
}


hese_iceprod_v0["NuTau_lowE"] = {
    "dataset" : "22633",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 1000, "level6_muon" : 1000, "level6_hybrid" : 1000
    },
}

hese_iceprod_v0["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 4000, "level6_muon" : 4000, "level6_hybrid" : 4000, "HESE" : 3011, "level7_cascade" : 3858
    },
}

hese_iceprod_v0["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 19994, "level6_muon" : 19994, "level6_hybrid" : 19994, "HESE" : 12637, "level7_cascade" : 19143
    },
}


hese_iceprod_v0["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 14996, "level6_muon" : 14996, "level6_hybrid" : 14996, "HESE" : 10322, "level7_cascade" : 14563
    },
}

hese_iceprod_v0["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 5000, "level6_muon" : 5000, "level6_hybrid" : 5000, "HESE" : 3779, "level7_cascade" : 4856
    },
}

hese_iceprod_v0["NuMu_lowE"] = {
    "dataset" : "22646",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 8000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 7635, "level6_muon" : 7635, "level6_hybrid" : 7635
    },
}

###
### v1, same as v0, almost same number of files (one batch missing because the iceprod jobs started again), just more variables needed for cascade analysis
### still HESE millipede missing, already added to the hdf_keys list
###
hese_iceprod_v1 = {}

hese_iceprod_v1["MuonGun_highE"] = { # 100 TeV - 1 EeV
    "dataset" : "21315",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level6_cascade_MuonGun" : 0, "level6_muon_MuonGun" : 0, "level6_hybrid_MuonGun" : 0, "HESE_MuonGun" : 0, "level7_cascade_MuonGun" : 0
    },
}

hese_iceprod_v1["MuonGun_midE"] = { # 10 TeV - 100 TeV
    "dataset" : "21316",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 40000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level6_cascade_MuonGun" : 0, "level6_muon_MuonGun" : 0, "level6_hybrid_MuonGun" : 0, "HESE_MuonGun" : 0, "level7_cascade_MuonGun" : 0
    },
}

hese_iceprod_v1["MuonGun_lowE"] = { # 5 TeV - 10 TeV
    "dataset" : "21317",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level6_cascade_MuonGun" : 0, "level6_muon_MuonGun" : 0, "level6_hybrid_MuonGun" : 0, "HESE_MuonGun" : 0, "level7_cascade_MuonGun" : 0
    },
}

hese_iceprod_v1["MuonGun_lowlowE"] = { # 1 TeV - 5 TeV
    "dataset" : "21318",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 100000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level6_cascade_MuonGun" : 0, "level6_muon_MuonGun" : 0, "level6_hybrid_MuonGun" : 0
    },
}

hese_iceprod_v1["MuonGun_lowlowlowE"] = { # 700 GeV - 1 TeV
    "dataset" : "21319",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 100000, 1000)],
    "flavor" : "MuonGun",
    "year" : "2016",
    "levels"  : {
        "level6_cascade_MuonGun" : 0, "level6_muon_MuonGun" : 0, "level6_hybrid_MuonGun" : 0
    },
}


hese_iceprod_v1["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 19913, "level6_muon" : 19913, "level6_hybrid" : 19913, "HESE" : 12828, "level7_cascade" : 18738
    },
}

hese_iceprod_v1["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : { #     0003000-0003999: 272 files missing from here: /scratch/tvaneede/reco/hdf_iceprod/hese_iceprod_v1/logs/HESE_NuE_22613_0003000-0003999.err
        "level6_cascade" : 3974, "level6_muon" : 3974, "level6_hybrid" : 3974, "HESE" : 2964-272, "level7_cascade" : 3800
    },
}

hese_iceprod_v1["NuE_lowE"] = {
    "dataset" : "22614",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 999, "level6_muon" : 999, "level6_hybrid" : 999
    },
}


hese_iceprod_v1["NuTau_lowE"] = {
    "dataset" : "22633",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 1000, "level6_muon" : 1000, "level6_hybrid" : 1000
    },
}

hese_iceprod_v1["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 4000, "level6_muon" : 4000, "level6_hybrid" : 4000, "HESE" : 3011, "level7_cascade" : 3858
    },
}

hese_iceprod_v1["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 19994, "level6_muon" : 19994, "level6_hybrid" : 19994, "HESE" : 12637, "level7_cascade" : 19143
    },
}


hese_iceprod_v1["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 14996, "level6_muon" : 14996, "level6_hybrid" : 14996, "HESE" : 10322, "level7_cascade" : 14563
    },
}

hese_iceprod_v1["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 5000, "level6_muon" : 5000, "level6_hybrid" : 5000, "HESE" : 3779, "level7_cascade" : 4856
    },
}

hese_iceprod_v1["NuMu_lowE"] = {
    "dataset" : "22646",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 8000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 7635, "level6_muon" : 7635, "level6_hybrid" : 7635
    },
}


###
### v2, same as v0, v1, just redo hese with all the millipede, nehas variables etc
###
hese_iceprod_v2 = {}

# hese_iceprod_v2["MuonGun"] = { #all
#     "dataset" : "21315-21317",
#     "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v2/merged/HESE_MuonGun_MuonGun.h5",
#     "nfiles" : 1,
# }

# hese_iceprod_v2["MuonGun_highE"] = { # 100 TeV - 1 EeV
#     "dataset" : "21315",
#     "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
#     "flavor" : "MuonGun",
#     "year" : "2016",
#     "levels"  : {
#         "HESE_MuonGun" : 0
#     },
# }

# hese_iceprod_v2["MuonGun_midE"] = { # 10 TeV - 100 TeV
#     "dataset" : "21316",
#     "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 40000, 1000)],
#     "flavor" : "MuonGun",
#     "year" : "2016",
#     "levels"  : {
#         "HESE_MuonGun" : 0
#     },
# }

# hese_iceprod_v2["MuonGun_lowE"] = { # 5 TeV - 10 TeV
#     "dataset" : "21317",
#     "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
#     "flavor" : "MuonGun",
#     "year" : "2016",
#     "levels"  : {
#         "HESE_MuonGun" : 0
#     },
# }

hese_iceprod_v2["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "HESE" : 14854 # # my tools script find 15739, but if i count separate entries in run id i get 
    },
    "nfiles" : 14854,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v2/merged/HESE_NuE_22612.h5"
}

hese_iceprod_v2["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : { 
         "HESE" : 2692 # my tools script finds 3418, but if i count separate entries in run id I get 
    },
    "nfiles" : 2692,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v2/merged/HESE_NuE_22613.h5"
}

hese_iceprod_v2["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE" : 3515
    },
    "nfiles" : 3515,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v2/merged/HESE_NuTau_22634.h5"
}

hese_iceprod_v2["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE" : 15008 # 15218
    },
    "nfiles" : 15008,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v2/merged/HESE_NuTau_22635.h5"
}


hese_iceprod_v2["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE" : 11716 # 12265
    },
    "nfiles" : 11716,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v2/merged/HESE_NuMu_22644.h5"
}

hese_iceprod_v2["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE" : 4370 #4371
    },
    "nfiles" : 4370,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v2/merged/HESE_NuMu_22645.h5"
}

###
### v3 i did not have the bdt variables, so i am adding them
###
hese_iceprod_v3 = {}

# hese_iceprod_v3["MuonGun"] = { #all
#     "dataset" : "21315-21317",
#     "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v3/merged/HESE_MuonGun_MuonGun.h5",
#     "nfiles" : 1,
# }

# hese_iceprod_v3["MuonGun_highE"] = { # 100 TeV - 1 EeV
#     "dataset" : "21315",
#     "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
#     "flavor" : "MuonGun",
#     "year" : "2016",
#     "levels"  : {
#         "HESE_MuonGun" : 0
#     },
# }

# hese_iceprod_v3["MuonGun_midE"] = { # 10 TeV - 100 TeV
#     "dataset" : "21316",
#     "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 40000, 1000)],
#     "flavor" : "MuonGun",
#     "year" : "2016",
#     "levels"  : {
#         "HESE_MuonGun" : 0
#     },
# }

# hese_iceprod_v3["MuonGun_lowE"] = { # 5 TeV - 10 TeV
#     "dataset" : "21317",
#     "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
#     "flavor" : "MuonGun",
#     "year" : "2016",
#     "levels"  : {
#         "HESE_MuonGun" : 0
#     },
# }

hese_iceprod_v3["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "HESE" : 17145, # 18136
    },
    "nfiles" : 17145, # 18136,
    "nfiles_logs" : 18136,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v3/merged/HESE_NuE_22612.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v3/"
}

hese_iceprod_v3["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : { 
         "HESE" : 2963 # 3958
    },
    "nfiles" : 2963, # 3958,
    "nfiles_logs" : 3958,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v3/merged/HESE_NuE_22613.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v3/"
}

hese_iceprod_v3["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE" : 3997 # 3997
    },
    "nfiles" : 3997, # 3997
    "nfiles_logs" : 3997,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v3/merged/HESE_NuTau_22634.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v3/"
}

hese_iceprod_v3["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE" : 18230 # 18472 
    },
    "nfiles" : 18230, # 18472,
    "nfiles_logs" : 18472,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v3/merged/HESE_NuTau_22635.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v3/"
}


hese_iceprod_v3["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE" : 13271, # 13875 
    },
    "nfiles" : 13271, #13875
    "nfiles_logs" : 13875,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v3/merged/HESE_NuMu_22644.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v3/"
}

hese_iceprod_v3["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE" : 4978 # 4978 
    },
    "nfiles" : 4978, # 4978,
    "nfiles_logs" : 4978,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v3/merged/HESE_NuMu_22645.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v3/"
}

###
### v4 I have been struggling with how many files go in. Do another check, extra print statements in my hdf script
###
hese_iceprod_v4 = {}

hese_iceprod_v4["MuonGun"] = { #all
    "dataset" : "21315-21317",
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v3/merged/HESE_MuonGun_MuonGun.h5",
    "nfiles" : 1,
}

hese_iceprod_v4["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "HESE" : 1,
    },
    "nfiles" : 19413, # used, but total files in folder 19430,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v4/merged/HESE_NuE_22612.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v4/"
}

hese_iceprod_v4["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : { 
         "HESE" : 1 
    },
    "nfiles" : 3968, # 3970, 
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v4/merged/HESE_NuE_22613.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v4/"
}

hese_iceprod_v4["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE" : 1 
    },
    "nfiles" : 3998, # 3999,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v4/merged/HESE_NuTau_22634.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v4/"
}

hese_iceprod_v4["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE" : 1
    },
    "nfiles" : 19393, # 19411, 
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v4/merged/HESE_NuTau_22635.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v4/"
}


hese_iceprod_v4["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE" : 1, 
    },
    "nfiles" : 14916, # 14925,
    "nfiles_logs" : 1,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v4/merged/HESE_NuMu_22644.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v4/"
}

hese_iceprod_v4["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE" : 1 
    },
    "nfiles" : 4982, # 4984,
    "nfiles_logs" : 1,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v4/merged/HESE_NuMu_22645.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v4/"
}

###
### v5 same number of files, just adding all the parameters I need
###
hese_iceprod_v5 = {}

# hese_iceprod_v5["MuonGun"] = { #all
#     "dataset" : "21315-21317",
#     "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v3/merged/HESE_MuonGun_MuonGun.h5",
#     "nfiles" : 1,
# }

hese_iceprod_v5["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "HESE" : 1,
    },
    "nfiles" : 19413, # used, but total files in folder 19430,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v5/merged/HESE_NuE_22612.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v5/"
}

hese_iceprod_v5["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : { 
         "HESE" : 1 
    },
    "nfiles" : 3968, # 3970, 
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v5/merged/HESE_NuE_22613.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v5/"
}

hese_iceprod_v5["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE" : 1 
    },
    "nfiles" : 3998, # 3999,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v5/merged/HESE_NuTau_22634.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v5/"
}

hese_iceprod_v5["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE" : 1
    },
    "nfiles" : 19393, # 19411, 
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v5/merged/HESE_NuTau_22635.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v5/"
}


hese_iceprod_v5["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE" : 1, 
    },
    "nfiles" : 14916, # 14925,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v5/merged/HESE_NuMu_22644.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v5/"
}

hese_iceprod_v5["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE" : 1 
    },
    "nfiles" : 4982, # 4984,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v5/merged/HESE_NuMu_22645.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v5/"
}


###
### v6 couple extra files, but adding rlogl differences millipede
###
hese_iceprod_v6 = {}

hese_iceprod_v6["MuonGun"] = { #all
    "dataset" : "21315-21317",
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v6/merged/HESE_MuonGun_MuonGun.h5",
    "nfiles" : 1,
}

hese_iceprod_v6["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "HESE" : 1,
    },
    "nfiles" : 19844, # used, but total files in folder 19861,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v6/merged/HESE_NuE_22612.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v6/"
}

hese_iceprod_v6["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : { 
         "HESE" : 1 
    },
    "nfiles" : 3968, # 3970, 
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v6/merged/HESE_NuE_22613.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v6/"
}

hese_iceprod_v6["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE" : 1 
    },
    "nfiles" : 3998, # 3999,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v6/merged/HESE_NuTau_22634.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v6/"
}

hese_iceprod_v6["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE" : 1
    },
    "nfiles" : 19834, # 19852, 
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v6/merged/HESE_NuTau_22635.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v6/"
}


hese_iceprod_v6["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE" : 1, 
    },
    "nfiles" : 14916, # 14925,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v6/merged/HESE_NuMu_22644.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v6/"
}

hese_iceprod_v6["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE" : 1 
    },
    "nfiles" : 4982, # 4984,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v6/merged/HESE_NuMu_22645.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v6/"
}


###
### v7 adding bdt variables for idc and ibr
###
hese_iceprod_v7 = {}

# hese_iceprod_v7["MuonGun"] = { #all
#     "dataset" : "21315-21317",
#     "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v7/merged/HESE_MuonGun_MuonGun.h5",
#     "nfiles" : 1,
# }

hese_iceprod_v7["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "HESE" : 19844,
    },
    "nfiles" : 19844, # used, but total files in folder 19861,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v7/merged/HESE_NuE_22612.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v7/"
}

hese_iceprod_v7["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : { 
         "HESE" : 3968, 
    },
    "nfiles" : 3968, # 3970, 
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v7/merged/HESE_NuE_22613.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v7/"
}

hese_iceprod_v7["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE" : 3998, 
    },
    "nfiles" : 3998, # 3999,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v7/merged/HESE_NuTau_22634.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v7/"
}

hese_iceprod_v7["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE" : 19834,
    },
    "nfiles" : 19834, # 19852, 
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v7/merged/HESE_NuTau_22635.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v7/"
}


hese_iceprod_v7["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE" : 14916, 
    },
    "nfiles" : 14916, # 14925,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v7/merged/HESE_NuMu_22644.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v7/"
}

hese_iceprod_v7["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE" : 4982, 
    },
    "nfiles" : 4982, # 4984,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v7/merged/HESE_NuMu_22645.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v7/"
}