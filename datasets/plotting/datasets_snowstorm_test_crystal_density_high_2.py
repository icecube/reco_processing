import copy

name = "test_crystal_density_high_2"

snowstorm_iceprod_test_crystal_density_high = {}

snowstorm_iceprod_test_crystal_density_high["NuTau_midE"] = {
    "dataset" : "23499",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 20,
}

snowstorm_iceprod_test_crystal_density_high["NuTau_highE"] = {
    "dataset" : "23498",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 20,
}


###
### level2 reco
###
snowstorm_iceprod_test_crystal_density_high_level2 = copy.deepcopy(snowstorm_iceprod_test_crystal_density_high)
for dataset_type in snowstorm_iceprod_test_crystal_density_high_level2:
    flavor = snowstorm_iceprod_test_crystal_density_high_level2[dataset_type]["flavor"]
    dataset = snowstorm_iceprod_test_crystal_density_high_level2[dataset_type]["dataset"]

    snowstorm_iceprod_test_crystal_density_high_level2[dataset_type]["hdf_file_path"] = (
        f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"{name}/level2_{flavor}_{dataset}.h5"
    )

    snowstorm_iceprod_test_crystal_density_high_level2[dataset_type]["hdf_path"] = (
        "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"{name}"
    )

###
### level3casc reco
###
snowstorm_iceprod_test_crystal_density_high_level3casc = copy.deepcopy(snowstorm_iceprod_test_crystal_density_high)
for dataset_type in snowstorm_iceprod_test_crystal_density_high_level3casc:
    flavor = snowstorm_iceprod_test_crystal_density_high_level3casc[dataset_type]["flavor"]
    dataset = snowstorm_iceprod_test_crystal_density_high_level3casc[dataset_type]["dataset"]

    snowstorm_iceprod_test_crystal_density_high_level3casc[dataset_type]["hdf_file_path"] = (
        f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"{name}/level3_cascade_{flavor}_{dataset}.h5"
    )

    snowstorm_iceprod_test_crystal_density_high_level3casc[dataset_type]["hdf_path"] = (
        "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"{name}"
    )


###
### level3 reco
###
snowstorm_iceprod_test_crystal_density_high_level3muon = copy.deepcopy(snowstorm_iceprod_test_crystal_density_high)
for dataset_type in snowstorm_iceprod_test_crystal_density_high_level3muon:
    flavor = snowstorm_iceprod_test_crystal_density_high_level3muon[dataset_type]["flavor"]
    dataset = snowstorm_iceprod_test_crystal_density_high_level3muon[dataset_type]["dataset"]

    snowstorm_iceprod_test_crystal_density_high_level3muon[dataset_type]["hdf_file_path"] = (
        f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"{name}/level3_muon_{flavor}_{dataset}.h5"
    )

    snowstorm_iceprod_test_crystal_density_high_level3muon[dataset_type]["hdf_path"] = (
        "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"{name}"
    )


###
### HESE reco without the low energy files
###
snowstorm_iceprod_test_crystal_density_high_HESE = copy.deepcopy(snowstorm_iceprod_test_crystal_density_high)
for dataset_type in snowstorm_iceprod_test_crystal_density_high:
    if "low" in dataset_type: del snowstorm_iceprod_test_crystal_density_high_HESE[dataset_type]


for dataset_type in snowstorm_iceprod_test_crystal_density_high_HESE:
    flavor = snowstorm_iceprod_test_crystal_density_high_HESE[dataset_type]["flavor"]
    dataset = snowstorm_iceprod_test_crystal_density_high_HESE[dataset_type]["dataset"]
    
    snowstorm_iceprod_test_crystal_density_high_HESE[dataset_type]["hdf_file_path"] = (
        f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"{name}/HESE_{flavor}_{dataset}.h5"
    )

    snowstorm_iceprod_test_crystal_density_high_HESE[dataset_type]["hdf_path"] = (
        "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"{name}"
    )



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