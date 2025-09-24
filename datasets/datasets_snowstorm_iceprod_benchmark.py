import copy

snowstorm_iceprod_benchmark = {}

snowstorm_iceprod_benchmark["NuTau_lowE"] = {
    "dataset" : "23458",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
}

snowstorm_iceprod_benchmark["NuTau_midE"] = {
    "dataset" : "23459",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
}

snowstorm_iceprod_benchmark["NuTau_highE"] = {
    "dataset" : "23460",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
}

snowstorm_iceprod_benchmark["NuE_lowE"] = {
    "dataset" : "23455",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "year" : "2023",
    "nfiles" : 10,
}

snowstorm_iceprod_benchmark["NuE_midE"] = {
    "dataset" : "23456",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "year" : "2023",
    "nfiles" : 10,
}

snowstorm_iceprod_benchmark["NuE_highE"] = {
    "dataset" : "23457",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "year" : "2023",
    "nfiles" : 10,
}

snowstorm_iceprod_benchmark["NuMu_lowlowE"] = {
    "dataset" : "23451",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "year" : "2023",
    "nfiles" : 10,
}

snowstorm_iceprod_benchmark["NuMu_lowE"] = {
    "dataset" : "23452",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "year" : "2023",
    "nfiles" : 10,
}

snowstorm_iceprod_benchmark["NuMu_midE"] = {
    "dataset" : "23453",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "year" : "2023",
    "nfiles" : 10,
}

snowstorm_iceprod_benchmark["NuMu_highE"] = {
    "dataset" : "23454",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "year" : "2023",
    "nfiles" : 10,
}

###
### level2 reco
###
snowstorm_iceprod_benchmark_level2 = copy.deepcopy(snowstorm_iceprod_benchmark)
for dataset_type in snowstorm_iceprod_benchmark_level2:
    flavor = snowstorm_iceprod_benchmark_level2[dataset_type]["flavor"]
    dataset = snowstorm_iceprod_benchmark_level2[dataset_type]["dataset"]

    snowstorm_iceprod_benchmark_level2[dataset_type]["hdf_file_path"] = (
        f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"snowstorm_iceprod_benchmark/level2_{flavor}_{dataset}.h5"
    )

    snowstorm_iceprod_benchmark_level2[dataset_type]["hdf_path"] = (
        "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        "snowstorm_iceprod_benchmark"
    )

###
### level3 reco
###
snowstorm_iceprod_benchmark_level3 = copy.deepcopy(snowstorm_iceprod_benchmark)
for dataset_type in snowstorm_iceprod_benchmark_level3:
    flavor = snowstorm_iceprod_benchmark_level3[dataset_type]["flavor"]
    dataset = snowstorm_iceprod_benchmark_level3[dataset_type]["dataset"]

    snowstorm_iceprod_benchmark_level3[dataset_type]["hdf_file_path"] = (
        f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"snowstorm_iceprod_benchmark/level3_cascade_{flavor}_{dataset}.h5"
    )

    snowstorm_iceprod_benchmark_level3[dataset_type]["hdf_path"] = (
        "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        "snowstorm_iceprod_benchmark"
    )


###
### level8 reco
###
snowstorm_iceprod_benchmark_level8 = copy.deepcopy(snowstorm_iceprod_benchmark)
for dataset_type in snowstorm_iceprod_benchmark_level8:
    flavor = snowstorm_iceprod_benchmark_level8[dataset_type]["flavor"]
    dataset = snowstorm_iceprod_benchmark_level8[dataset_type]["dataset"]

    snowstorm_iceprod_benchmark_level8[dataset_type]["hdf_file_path"] = (
        f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"snowstorm_iceprod_benchmark/level8_cascade_{flavor}_{dataset}.h5"
    )

    snowstorm_iceprod_benchmark_level8[dataset_type]["hdf_path"] = (
        "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        "snowstorm_iceprod_benchmark"
    )

###
### HESE reco without the low energy files
###
snowstorm_iceprod_benchmark_HESE = copy.deepcopy(snowstorm_iceprod_benchmark)
for dataset_type in snowstorm_iceprod_benchmark_level8:
    if "low" in dataset_type: del snowstorm_iceprod_benchmark_HESE[dataset_type]

for dataset_type in snowstorm_iceprod_benchmark_HESE:
    flavor = snowstorm_iceprod_benchmark_HESE[dataset_type]["flavor"]
    dataset = snowstorm_iceprod_benchmark_HESE[dataset_type]["dataset"]
    
    snowstorm_iceprod_benchmark_HESE[dataset_type]["hdf_file_path"] = (
        f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"snowstorm_iceprod_benchmark/HESE_evtgen_{flavor}_{dataset}.h5"
    )

    snowstorm_iceprod_benchmark_HESE[dataset_type]["hdf_path"] = (
        "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        "snowstorm_iceprod_benchmark"
    )