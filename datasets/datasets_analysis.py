
###
### v0 analysis
###

taureco_iceprod_v0 = {}

taureco_iceprod_v0["NuTau_lowE"] = {
    "dataset" : "22633",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level6_cascade", "level6_muon", "level6_hybrid"]
}

taureco_iceprod_v0["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level6_cascade", "level6_muon", "level6_hybrid","HESE","level7_cascade"]
}

taureco_iceprod_v0["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level6_cascade", "level6_muon", "level6_hybrid","HESE","level7_cascade"]
}

taureco_iceprod_v0["NuE_lowE"] = {
    "dataset" : "22614",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level6_cascade", "level6_muon", "level6_hybrid"]
}

taureco_iceprod_v0["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level6_cascade", "level6_muon", "level6_hybrid","HESE","level7_cascade"]
}

taureco_iceprod_v0["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level6_cascade", "level6_muon", "level6_hybrid","HESE","level7_cascade"]
}

taureco_iceprod_v0["NuMu_lowE"] = {
    "dataset" : "22646",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 8000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level6_cascade", "level6_muon", "level6_hybrid"]
}

taureco_iceprod_v0["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level6_cascade", "level6_muon", "level6_hybrid","HESE","level7_cascade"]
}

taureco_iceprod_v0["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level6_cascade", "level6_muon", "level6_hybrid","HESE","level7_cascade"]
}