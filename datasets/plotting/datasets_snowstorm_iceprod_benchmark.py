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
### level3casc reco
###
snowstorm_iceprod_benchmark_level3casc = copy.deepcopy(snowstorm_iceprod_benchmark)
for dataset_type in snowstorm_iceprod_benchmark_level3casc:
    flavor = snowstorm_iceprod_benchmark_level3casc[dataset_type]["flavor"]
    dataset = snowstorm_iceprod_benchmark_level3casc[dataset_type]["dataset"]

    snowstorm_iceprod_benchmark_level3casc[dataset_type]["hdf_file_path"] = (
        f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"snowstorm_iceprod_benchmark/level3_cascade_{flavor}_{dataset}.h5"
    )

    snowstorm_iceprod_benchmark_level3casc[dataset_type]["hdf_path"] = (
        "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        "snowstorm_iceprod_benchmark"
    )


###
### level3 reco
###
snowstorm_iceprod_benchmark_level3muon = copy.deepcopy(snowstorm_iceprod_benchmark)
for dataset_type in snowstorm_iceprod_benchmark_level3muon:
    flavor = snowstorm_iceprod_benchmark_level3muon[dataset_type]["flavor"]
    dataset = snowstorm_iceprod_benchmark_level3muon[dataset_type]["dataset"]

    snowstorm_iceprod_benchmark_level3muon[dataset_type]["hdf_file_path"] = (
        f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"snowstorm_iceprod_benchmark/level3_muon_{flavor}_{dataset}.h5"
    )

    snowstorm_iceprod_benchmark_level3muon[dataset_type]["hdf_path"] = (
        "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        "snowstorm_iceprod_benchmark"
    )


###
### level8 reco
###
snowstorm_iceprod_benchmark_level8 = copy.deepcopy(snowstorm_iceprod_benchmark)
del snowstorm_iceprod_benchmark_level8["NuMu_lowlowE"]
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
for dataset_type in snowstorm_iceprod_benchmark:
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

###
### more benchmark
###


ftp_baseline_level2 = {}

ftp_baseline_level2["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2/NuTau_22634.h5",
    'nfiles' : 1000, # 4000,
}

ftp_baseline_level2["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2/NuTau_22635.h5",
    'nfiles' : 1000, # 19997,

}


ftp_baseline_level2["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2/NuE_22613.h5",
    'nfiles' : 1000, # 3987,
}

ftp_baseline_level2["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2/NuE_22612.h5",
    'nfiles' : 1000, # 19960,
}

ftp_baseline_level2["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : ["0000000-0000999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2/NuMu_22645.h5",
    'nfiles' : 1000, # 5000,
}



ftp_baseline_level2["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : ["0000000-0000999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2/NuMu_22644.h5",
    'nfiles' : 1000, # 14998,
}

### l3 casc

ftp_baseline_level3casc = {}

ftp_baseline_level3casc["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc/NuTau_22634.h5",
    'nfiles' : 1000, # 4000,
}

ftp_baseline_level3casc["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc/NuTau_22635.h5",
    'nfiles' : 1000, # 19997,
}


ftp_baseline_level3casc["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc/NuE_22613.h5",
    'nfiles' : 1000, # 3987,
}

ftp_baseline_level3casc["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc/NuE_22612.h5",
    'nfiles' : 1000, # 19960,
}

ftp_baseline_level3casc["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : ["0000000-0000999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc/NuMu_22645.h5",
    'nfiles' : 1000, # 5000,
}



ftp_baseline_level3casc["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : ["0000000-0000999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc/NuMu_22644.h5",
    'nfiles' : 1000, # 14998,
}