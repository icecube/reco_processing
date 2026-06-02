
###
### v0
###

ftp_ensemble_v0 = {}

# ftp_ensemble_v0["NuMu_lowlowE"] = {
#     "dataset" : "22861",
#     "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
#     "flavor" : "NuMu",
#     "year" : "2020",
#     "levels"  : {
#         "level6_cascade" : 4792, "level6_hybrid" : 4792, "level6_muon" : 4792, # no events in this hdf file?
#     },
# }

ftp_ensemble_v0["NuMu_lowE"] = {
    "dataset" : "22852",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 9000, 1000)],
    "flavor" : "NuMu",
    "year" : "2020",
    "levels"  : {
        "level6_cascade" : 8084, "level6_hybrid" : 8084, "level6_muon" : 8084, 
    },
}

ftp_ensemble_v0["NuMu_midE"] = {
    "dataset" : "22853",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 6000, 1000)], 
    "flavor" : "NuMu",
    "year" : "2020",
    "levels"  : {
        "level6_cascade" : 5400, "level6_hybrid" : 5400, "level6_muon" : 5400, 
    },
}

ftp_ensemble_v0["NuMu_highE"] = {
    "dataset" : "22854",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 18000, 1000)],
    "flavor" : "NuMu",
    "year" : "2020",
    "levels"  : {
        "level6_cascade" : 17992, "level6_hybrid" : 17992, "level6_muon" : 17992, 
    },
}


ftp_ensemble_v0["NuE_lowE"] = {
    "dataset" : "22855",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)],
    "flavor" : "NuE",
    "year" : "2020",
    "levels"  : {
        "level6_cascade" : 1000, "level6_hybrid" : 1000, "level6_muon" : 1000, 
    },
}

ftp_ensemble_v0["NuE_midE"] = {
    "dataset" : "22856",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)], 
    "flavor" : "NuE",
    "year" : "2020",
    "levels"  : {
        "level6_cascade" : 4200, "level6_hybrid" : 4200, "level6_muon" : 4200, 
    },
}

ftp_ensemble_v0["NuE_highE"] = {
    "dataset" : "22857",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 13000, 1000)] + [f"{i:07d}-{i+999:07d}" for i in range(14000, 24000, 1000)],
    "flavor" : "NuE",
    "year" : "2020",
    "levels"  : { # seems that 0013000-0013999 was corrupted, I remove it: 23994 - 1000
        "level6_cascade" : 22994, "level6_hybrid" : 22994, "level6_muon" : 22994,
    },
}

ftp_ensemble_v0["NuTau_lowE"] = {
    "dataset" : "22858",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)],
    "flavor" : "NuTau",
    "year" : "2020",
    "levels"  : {
        "level6_cascade" : 1000, "level6_hybrid" : 1000, "level6_muon" : 1000, 
    },
}

ftp_ensemble_v0["NuTau_midE"] = {
    "dataset" : "22859",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)], 
    "flavor" : "NuTau",
    "year" : "2020",
    "levels"  : {
        "level6_cascade" : 4000, "level6_hybrid" : 4000, "level6_muon" : 4000, 
    },
}

ftp_ensemble_v0["NuTau_highE"] = {
    "dataset" : "22860",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 22000, 1000)],
    "flavor" : "NuTau",
    "year" : "2020",
    "levels"  : {
        "level6_cascade" : 21992, "level6_hybrid" : 21992, "level6_muon" : 21992, 
    },
}


###
### v1
###

# de muons van level3 muon gingen maar niet. Die run ik nu zonder enige functies van mijn hdf script. Hopelijk lekker snel
ftp_ensemble_v1 = {}

ftp_ensemble_v1["NuMu_lowlowE"] = {
    "dataset" : "22861",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
    "flavor" : "NuMu",
    "year" : "2020",
    "levels"  : {
        "level3_muon" : 4796,
    },
}

ftp_ensemble_v1["NuMu_lowE"] = {
    "dataset" : "22852",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 9000, 1000)],
    "flavor" : "NuMu",
    "year" : "2020",
    "levels"  : {
        "level3_muon" : 8093,
    },
}

ftp_ensemble_v1["NuMu_midE"] = {
    "dataset" : "22853",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 6000, 1000)], 
    "flavor" : "NuMu",
    "year" : "2020",
    "levels"  : {
        "level3_muon" : 5400,
    },
}

ftp_ensemble_v1["NuMu_highE"] = {
    "dataset" : "22854",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 18000, 1000)],
    "flavor" : "NuMu",
    "year" : "2020",
    "levels"  : {
        "level3_muon" : 17996,
    },
}


ftp_ensemble_v1["NuE_lowE"] = {
    "dataset" : "22855",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)],
    "flavor" : "NuE",
    "year" : "2020",
    "levels"  : {
        "level3_muon" : 1000,
    },
}

ftp_ensemble_v1["NuE_midE"] = {
    "dataset" : "22856",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)], 
    "flavor" : "NuE",
    "year" : "2020",
    "levels"  : {
        "level3_muon" : 4200,
    },
}

ftp_ensemble_v1["NuE_highE"] = {
    "dataset" : "22857",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 24000, 1000)],
    "flavor" : "NuE",
    "year" : "2020",
    "levels"  : {
        "level3_muon" : 23997,
    },
}


ftp_ensemble_v1["NuTau_lowE"] = {
    "dataset" : "22858",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)],
    "flavor" : "NuTau",
    "year" : "2020",
    "levels"  : {
        "level3_muon" : 1000,
    },
}

ftp_ensemble_v1["NuTau_midE"] = {
    "dataset" : "22859",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)], 
    "flavor" : "NuTau",
    "year" : "2020",
    "levels"  : {
        "level3_muon" : 4000,
    },
}

ftp_ensemble_v1["NuTau_highE"] = {
    "dataset" : "22860",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 22000, 1000)],
    "flavor" : "NuTau",
    "year" : "2020",
    "levels"  : {
        "level3_muon" : 21996,
    },
}


