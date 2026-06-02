
###
### v0 almost complete, just raise the memory of last evtgen runs
###
hese_extra_iceprod_v0 = {}

# hese_extra_iceprod_v0["MuonGun"] = { #all
#     "dataset" : "21315-21317",
#     "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_iceprod_v6/merged/HESE_MuonGun_MuonGun.h5",
#     "nfiles" : 1,
# }

hese_extra_iceprod_v0["NuE_highE"] = {
    "dataset" : "22663",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "HESE_evtgen" : 1, "HESE_taupede" : 0,
    },
}

hese_extra_iceprod_v0["NuE_midE"] = {
    "dataset" : "22664",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : { 
        "HESE_evtgen" : 1, "HESE_taupede" : 0,
    },
}

hese_extra_iceprod_v0["NuTau_midE"] = {
    "dataset" : "22667",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE_evtgen" : 1, "HESE_taupede" : 0,
    },
}

hese_extra_iceprod_v0["NuTau_highE"] = {
    "dataset" : "22668",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE_evtgen" : 1, "HESE_taupede" : 0,
    },
}


hese_extra_iceprod_v0["NuMu_highE"] = {
    "dataset" : "22670",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE_evtgen" : 1, "HESE_taupede" : 0,
    },
}

hese_extra_iceprod_v0["NuMu_midE"] = {
    "dataset" : "22671",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE_evtgen" : 0, "HESE_taupede" : 0,
    },
}

###
### v1 turns out I had some ghost files, they were removed by David
###
hese_extra_iceprod_v1 = {}

# hese_extra_iceprod_v0["MuonGun"] = { #all
#     "dataset" : "21315-21317",
#     "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_extra_iceprod_v1/merged/HESE_MuonGun_MuonGun.h5",
#     "nfiles" : 1,
# }

hese_extra_iceprod_v1["NuE_highE"] = {
    "dataset" : "22663",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : {
        "HESE_evtgen" : 19624, "HESE_taupede" : 19693,
    },
    "nfiles" : 19624, # used, but total files in folder 19633 for evtgen,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_extra_iceprod_v1/merged/HESE_NuE_22612.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_extra_iceprod_v1/"
}

hese_extra_iceprod_v1["NuE_midE"] = {
    "dataset" : "22664",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuE",
    "year" : "2023",
    "levels"  : { 
        "HESE_evtgen" : 3741, "HESE_taupede" : 3749,
    },
    "nfiles" : 3741,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_extra_iceprod_v1/merged/HESE_NuE_22613.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_extra_iceprod_v1/"
}

hese_extra_iceprod_v1["NuTau_midE"] = {
    "dataset" : "22667",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 4000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE_evtgen" : 3764, "HESE_taupede" : 3769,
    },
    "nfiles" : 3764, 
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_extra_iceprod_v1/merged/HESE_NuTau_22634.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_extra_iceprod_v1/"
}

hese_extra_iceprod_v1["NuTau_highE"] = {
    "dataset" : "22668",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "NuTau",
    "year" : "2023",
    "levels"  : {
        "HESE_evtgen" : 16490, "HESE_taupede" : 16581,
    },
    "nfiles" : 16490,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_extra_iceprod_v1/merged/HESE_NuTau_22635.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_extra_iceprod_v1/"
}


hese_extra_iceprod_v1["NuMu_highE"] = {
    "dataset" : "22670",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE_evtgen" : 9645, "HESE_taupede" : 9687,
    },
    "nfiles" : 9645,
    "hdf_file_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_extra_iceprod_v1/merged/HESE_NuMu_22644.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_extra_iceprod_v1/"
}

hese_extra_iceprod_v1["NuMu_midE"] = {
    "dataset" : "22671",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 5000, 1000)],
    "flavor" : "NuMu",
    "year" : "2023",
    "levels"  : {
        "HESE_evtgen" : 4676, "HESE_taupede" : 4695,
    },
    "nfiles" : 4676,
    "hdf_file_path" : "/mnt/ceph1/-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_extra_iceprod_v1/merged/HESE_NuMu_22645.h5",
    "hdf_path" : "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/hese_extra_iceprod_v1/"
}