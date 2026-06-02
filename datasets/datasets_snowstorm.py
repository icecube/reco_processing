
###
### v0
###

# number of files per level taken from print_files_per_hdf_dataset.py

ftp_ensemble_ani_v0 = {}

ftp_ensemble_ani_v0["NuMu_lowlowE"] = {
    "dataset" : "23520",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 0, "level6_muon" : 0, "level6_hybrid" : 0, "level3_muon" : 0,
    },
}

ftp_ensemble_ani_v0["NuMu_lowE"] = {
    "dataset" : "23521",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 8000, 1000)], # should be 9000
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 0, "level6_muon" : 0, "level6_hybrid" : 0, "level3_muon" : 0,
    },
}

ftp_ensemble_ani_v0["NuMu_midE"] = {
    "dataset" : "23522",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)], # should be 6000
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 0, "level6_muon" : 0, "level6_hybrid" : 0, "level3_muon" : 0, "level7_cascade" : 0, "HESE_evtgen" : 0,
    },
}

ftp_ensemble_ani_v0["NuMu_highE"] = {
    "dataset" : "23523",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 14000, 1000)], # should be 18000
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 0, "level6_muon" : 0, "level6_hybrid" : 0, "level3_muon" : 0, "level7_cascade" : 0, "HESE_evtgen" : 0,
    },
}


ftp_ensemble_ani_v0["NuE_lowE"] = {
    "dataset" : "23524",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 0, "level6_muon" : 0, "level6_hybrid" : 0, "level3_muon" : 0,
    },
}

ftp_ensemble_ani_v0["NuE_midE"] = {
    "dataset" : "23525",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)], # should be 5000
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 0, "level6_muon" : 0, "level6_hybrid" : 0, "level3_muon" : 0, "level7_cascade" : 0, "HESE_evtgen" : 0,
    },
}

ftp_ensemble_ani_v0["NuE_highE"] = {
    "dataset" : "23526",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 17000, 1000)], # should be 24000
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 0, "level6_muon" : 0, "level6_hybrid" : 0, "level3_muon" : 0, "level7_cascade" : 0, "HESE_evtgen" : 0,
    },
}


ftp_ensemble_ani_v0["NuTau_lowE"] = {
    "dataset" : "23527",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 0, "level6_muon" : 0, "level6_hybrid" : 0, "level3_muon" : 0,
    },
}

ftp_ensemble_ani_v0["NuTau_midE"] = {
    "dataset" : "23528",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)], 
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 0, "level6_muon" : 0, "level6_hybrid" : 0, "level3_muon" : 0, "level7_cascade" : 0, "HESE_evtgen" : 0,
    },
}

ftp_ensemble_ani_v0["NuTau_highE"] = {
    "dataset" : "23529",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 17000, 1000)], # should be 22000
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 0, "level6_muon" : 0, "level6_hybrid" : 0, "level3_muon" : 0, "level7_cascade" : 0, "HESE_evtgen" : 0,
    },
}


###
### v1
###

# ongeveer klaar, laatste paar nog vast. Ik ga als deze hdf gemaakt is, de memory en cpu verhogen van de laatste jobs
# een stel muon level3 muon gingen niet, die verwijder ik uit deze set, en ik heb v2 gemaakt speciaal voor level3_muon

ftp_ensemble_ani_v1 = {}

# ftp_ensemble_ani_v1["NuMu_lowlowE"] = {
#     "dataset" : "23520",
#     "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
#     "flavor" : "NuMu",
#     "year" : "2023",
#     "levels"  : {
#         "level6_cascade" : 4798, "level6_hybrid" : 4798, "level6_muon" : 4797, # no events in hdf file!
#     },
# }

ftp_ensemble_ani_v1["NuMu_lowE"] = {
    "dataset" : "23521",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 9000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 8083, "level6_hybrid" : 8084, "level6_muon" : 8081, 
    },
}

ftp_ensemble_ani_v1["NuMu_midE"] = {
    "dataset" : "23522",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 6000, 1000)], 
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 5394, "level6_hybrid" : 5391, "level6_muon" : 5393, "level7_cascade_evtgen" : 5367, "HESE_evtgen" : 5373,
    },
}

ftp_ensemble_ani_v1["NuMu_highE"] = {
    "dataset" : "23523",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 18000, 1000)], # should be 18000
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 17989, "level6_hybrid" : 17993, "level6_muon" : 17992, "level7_cascade_evtgen" : 17965, "HESE_evtgen" : 17939,
    },
}


ftp_ensemble_ani_v1["NuE_lowE"] = {
    "dataset" : "23524",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 972, "level6_hybrid" : 999, "level6_muon" : 986, 
    },
}

ftp_ensemble_ani_v1["NuE_midE"] = {
    "dataset" : "23525",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)], 
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 4145, "level6_hybrid" : 4199, "level6_muon" : 4197, "level7_cascade_evtgen" : 4185, "HESE_evtgen" : 4196,
    },
}

ftp_ensemble_ani_v1["NuE_highE"] = {
    "dataset" : "23526",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 24000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 23973, "level6_hybrid" : 23983, "level6_muon" : 23984, "level7_cascade_evtgen" : 23891, "HESE_evtgen" : 23891,
    },
}


ftp_ensemble_ani_v1["NuTau_lowE"] = {
    "dataset" : "23527",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)], # should be 2000!
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 985, "level6_hybrid" : 1000, "level6_muon" : 998, 
    },
}

ftp_ensemble_ani_v1["NuTau_midE"] = {
    "dataset" : "23528",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)], 
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 3995, "level6_hybrid" : 3998, "level6_muon" : 3997, "level7_cascade_evtgen" : 3876, "HESE_evtgen" : 3993,
    },
}

ftp_ensemble_ani_v1["NuTau_highE"] = {
    "dataset" : "23529",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 22000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level6_cascade" : 21980, "level6_hybrid" : 21982, "level6_muon" : 21983, "level7_cascade_evtgen" : 21929, "HESE_evtgen" : 21909,
    },
}


###
### v2
###

# de muons van level3 muon gingen maar niet. Die run ik nu zonder enige functies van mijn hdf script. Hopelijk lekker snel

ftp_ensemble_ani_v2 = {}

ftp_ensemble_ani_v2["NuMu_lowlowE"] = {
    "dataset" : "23520",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level3_muon" : 4797,
    },
}

ftp_ensemble_ani_v2["NuMu_lowE"] = {
    "dataset" : "23521",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 9000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level3_muon" : 8086,
    },
}

ftp_ensemble_ani_v2["NuMu_midE"] = {
    "dataset" : "23522",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 6000, 1000)], 
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level3_muon" : 5389,
    },
}

ftp_ensemble_ani_v2["NuMu_highE"] = {
    "dataset" : "23523",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 18000, 1000)], # should be 18000
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "level3_muon" : 17984,
    },
}


ftp_ensemble_ani_v2["NuE_lowE"] = {
    "dataset" : "23524",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "level3_muon" : 1000,
    },
}

ftp_ensemble_ani_v2["NuE_midE"] = {
    "dataset" : "23525",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)], 
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "level3_muon" : 4199,
    },
}

ftp_ensemble_ani_v2["NuE_highE"] = {
    "dataset" : "23526",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 24000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "level3_muon" : 23990,
    },
}


ftp_ensemble_ani_v2["NuTau_lowE"] = {
    "dataset" : "23527",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 1000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level3_muon" : 1000,
    },
}

ftp_ensemble_ani_v2["NuTau_midE"] = {
    "dataset" : "23528",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)], 
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level3_muon" : 3997,
    },
}

ftp_ensemble_ani_v2["NuTau_highE"] = {
    "dataset" : "23529",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 22000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "level3_muon" : 21989,
    },
}
