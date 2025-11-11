import copy

name = "test_crystal_density_low_2"

snowstorm_iceprod_test_crystal_density_low = {}

snowstorm_iceprod_test_crystal_density_low["NuTau_midE"] = {
    "dataset" : "23501",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 20,
}

snowstorm_iceprod_test_crystal_density_low["NuTau_highE"] = {
    "dataset" : "23500",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 20,
}


###
### level2 reco
###
snowstorm_iceprod_test_crystal_density_low_level2 = copy.deepcopy(snowstorm_iceprod_test_crystal_density_low)
for dataset_type in snowstorm_iceprod_test_crystal_density_low_level2:
    flavor = snowstorm_iceprod_test_crystal_density_low_level2[dataset_type]["flavor"]
    dataset = snowstorm_iceprod_test_crystal_density_low_level2[dataset_type]["dataset"]

    snowstorm_iceprod_test_crystal_density_low_level2[dataset_type]["hdf_file_path"] = (
        f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"{name}/level2_{flavor}_{dataset}.h5"
    )

    snowstorm_iceprod_test_crystal_density_low_level2[dataset_type]["hdf_path"] = (
        "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"{name}"
    )

###
### level3casc reco
###
snowstorm_iceprod_test_crystal_density_low_level3casc = copy.deepcopy(snowstorm_iceprod_test_crystal_density_low)
for dataset_type in snowstorm_iceprod_test_crystal_density_low_level3casc:
    flavor = snowstorm_iceprod_test_crystal_density_low_level3casc[dataset_type]["flavor"]
    dataset = snowstorm_iceprod_test_crystal_density_low_level3casc[dataset_type]["dataset"]

    snowstorm_iceprod_test_crystal_density_low_level3casc[dataset_type]["hdf_file_path"] = (
        f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"{name}/level3_cascade_{flavor}_{dataset}.h5"
    )

    snowstorm_iceprod_test_crystal_density_low_level3casc[dataset_type]["hdf_path"] = (
        "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"{name}"
    )


###
### level3 reco
###
snowstorm_iceprod_test_crystal_density_low_level3muon = copy.deepcopy(snowstorm_iceprod_test_crystal_density_low)
for dataset_type in snowstorm_iceprod_test_crystal_density_low_level3muon:
    flavor = snowstorm_iceprod_test_crystal_density_low_level3muon[dataset_type]["flavor"]
    dataset = snowstorm_iceprod_test_crystal_density_low_level3muon[dataset_type]["dataset"]

    snowstorm_iceprod_test_crystal_density_low_level3muon[dataset_type]["hdf_file_path"] = (
        f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"{name}/level3_muon_{flavor}_{dataset}.h5"
    )

    snowstorm_iceprod_test_crystal_density_low_level3muon[dataset_type]["hdf_path"] = (
        "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"{name}"
    )


###
### HESE reco without the low energy files
###
snowstorm_iceprod_test_crystal_density_low_HESE = copy.deepcopy(snowstorm_iceprod_test_crystal_density_low)
for dataset_type in snowstorm_iceprod_test_crystal_density_low:
    if "low" in dataset_type: del snowstorm_iceprod_test_crystal_density_low_HESE[dataset_type]


for dataset_type in snowstorm_iceprod_test_crystal_density_low_HESE:
    flavor = snowstorm_iceprod_test_crystal_density_low_HESE[dataset_type]["flavor"]
    dataset = snowstorm_iceprod_test_crystal_density_low_HESE[dataset_type]["dataset"]
    
    snowstorm_iceprod_test_crystal_density_low_HESE[dataset_type]["hdf_file_path"] = (
        f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"{name}/HESE_{flavor}_{dataset}.h5"
    )

    snowstorm_iceprod_test_crystal_density_low_HESE[dataset_type]["hdf_path"] = (
        "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/"
        f"{name}"
    )

