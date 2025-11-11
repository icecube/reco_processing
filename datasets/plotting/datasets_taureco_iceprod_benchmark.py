import copy

taureco_iceprod_benchmark = {}

taureco_iceprod_benchmark["NuTau_lowE"] = {
    "dataset" : "22633",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
}

taureco_iceprod_benchmark["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
}

taureco_iceprod_benchmark["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
}

taureco_iceprod_benchmark["NuE_lowE"] = {
    "dataset" : "22614",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "year" : "2023",
    "nfiles" : 10,
}

taureco_iceprod_benchmark["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "year" : "2023",
    "nfiles" : 10,
}

taureco_iceprod_benchmark["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "year" : "2023",
    "nfiles" : 10,
}

taureco_iceprod_benchmark["NuMu_lowE"] = {
    "dataset" : "22646",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "year" : "2023",
    "nfiles" : 10,
}

taureco_iceprod_benchmark["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "year" : "2023",
    "nfiles" : 10,
}

taureco_iceprod_benchmark["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "year" : "2023",
    "nfiles" : 10,
}


###
### level8 reco
###
taureco_iceprod_benchmark_level8 = copy.deepcopy(taureco_iceprod_benchmark)
for dataset_type in taureco_iceprod_benchmark_level8:
    flavor = taureco_iceprod_benchmark_level8[dataset_type]["flavor"]
    dataset = taureco_iceprod_benchmark_level8[dataset_type]["dataset"]

    taureco_iceprod_benchmark_level8[dataset_type]["hdf_file_path"] = (
        f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"taureco_iceprod_benchmark/level8_cascade_{flavor}_{dataset}.h5"
    )

    taureco_iceprod_benchmark_level8[dataset_type]["hdf_path"] = (
        "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        "taureco_iceprod_benchmark"
    )


###
### HESE reco without the low energy files
###
taureco_iceprod_benchmark_HESE = copy.deepcopy(taureco_iceprod_benchmark)
for dataset_type in taureco_iceprod_benchmark_level8:
    if "low" in dataset_type: del taureco_iceprod_benchmark_HESE[dataset_type]

for dataset_type in taureco_iceprod_benchmark_HESE:
    flavor = taureco_iceprod_benchmark_HESE[dataset_type]["flavor"]
    dataset = taureco_iceprod_benchmark_HESE[dataset_type]["dataset"]
    
    taureco_iceprod_benchmark_HESE[dataset_type]["hdf_file_path"] = (
        f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"taureco_iceprod_benchmark/HESE_evtgen_{flavor}_{dataset}.h5"
    )

    taureco_iceprod_benchmark_HESE[dataset_type]["hdf_path"] = (
        "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        "taureco_iceprod_benchmark"
    )

###
### benchmark
###
evtgen_v4_rec_v9 = {}

evtgen_v4_rec_v9["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v4",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuTau_22634.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9",
    "nfiles" : 2000,
}

evtgen_v4_rec_v9["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v4",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuTau_22635.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9",
    "nfiles" : 2000,
}

evtgen_v4_rec_v9["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v4",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuE_22613.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9",
    "nfiles" : 1997,
}

evtgen_v4_rec_v9["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v4",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuE_22612.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9",
    "nfiles" : 2000,
}

evtgen_v4_rec_v9["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v4",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuMu_22645.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9",
    "nfiles" : 2000,
}

evtgen_v4_rec_v9["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v4",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuMu_22644.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9",
    "nfiles" : 2000,
}