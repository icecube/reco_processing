
import pandas as pd
import simweights
import sys

hdf_file_path_template = "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/{dataset_name}/merged/{level}_{flavor}_{dataset_id}.h5"

###
### merging definitions of the hdf files
###
keys_to_merge = {}

keys_to_merge["level6_cascade"] = {
    "NuE" : ["NuE_lowE", "NuE_midE", "NuE_highE"],
    "NuMu" : ["NuMu_lowE","NuMu_midE", "NuMu_highE"], # "NuMu_lowlowE" was empty
    "NuTau" : ["NuTau_lowE","NuTau_midE", "NuTau_highE"],
    "NuAll" : ['NuE', "NuMu", "NuTau"],
}
keys_to_merge["level6_hybrid"] = keys_to_merge["level6_cascade"]
keys_to_merge["level6_muon"] = keys_to_merge["level6_cascade"]

keys_to_merge["HESE_evtgen"] = {
    "NuE" : ["NuE_midE", "NuE_highE"],
    "NuMu" : ["NuMu_midE", "NuMu_highE"],
    "NuTau" : ["NuTau_midE", "NuTau_highE"],
    "NuAll" : ['NuE', "NuMu", "NuTau"],
}
keys_to_merge["HESE_taupede"] = keys_to_merge["HESE_evtgen"]
keys_to_merge["level7_cascade_evtgen"] = keys_to_merge["HESE_evtgen"]
keys_to_merge["HESE"] = keys_to_merge["HESE_evtgen"]

keys_to_merge["level3_muon"] = {
    "NuE" : ["NuE_lowE", "NuE_midE", "NuE_highE"],
    "NuMu" : ["NuMu_lowlowE","NuMu_lowE","NuMu_midE", "NuMu_highE"],
    "NuTau" : ["NuTau_lowE","NuTau_midE", "NuTau_highE"],
    "NuAll" : ['NuE', "NuMu", "NuTau"],
}

def open_datasets_by_level(simulation_dataset, dataset_name):

    for key, ds in simulation_dataset.items():
        print(f"----- Opening dataset {key}")
        ds["hdf_files"] = {}
        ds["weighters"] = {}
        flavor = ds["flavor"]
        dataset_id = ds["dataset"]

        for level, nfiles in ds["levels"].items():
            print(f"    -> Level {level}")

            hdf_path = hdf_file_path_template.format(dataset_name=dataset_name,level=level, flavor=flavor, dataset_id=dataset_id)
            print(f"    -> file {hdf_path}")

            hdf = pd.HDFStore(hdf_path, "r")
            weighter = simweights.NuGenWeighter(hdf, nfiles=nfiles)

            ds["hdf_files"][level] = hdf
            ds["weighters"][level] = weighter

    return simulation_dataset

def merge_datasets_by_level(simulation_dataset, keys_to_merge=keys_to_merge):

    for level, flavor_map in keys_to_merge.items():
        print(f"----- Merging level {level}")

        # skip if no dataset has this level
        if not any(level in ds.get("weighters", {}) for ds in simulation_dataset.values() if isinstance(ds, dict)):
            print(f"Skipping level {level}, not present in any dataset")
            continue

        for flavor, source_keys in flavor_map.items():
            if flavor not in simulation_dataset:
                simulation_dataset[flavor] = {"weighters": {}, "hdf_files": {}}

            merged = None
            for key in source_keys:
                if key not in simulation_dataset: 
                    continue
                w = simulation_dataset[key].get("weighters", {}).get(level)
                if w is None: 
                    continue
                merged = w if merged is None else merged + w

            if merged is not None:
                simulation_dataset[flavor]["weighters"][level] = merged
    test_merged_hdf_vs_weighter(simulation_dataset, keys_to_merge=keys_to_merge)

    return simulation_dataset


def test_merged_hdf_vs_weighter(simulation_dataset, keys_to_merge=keys_to_merge):
    for level, flavor_map in keys_to_merge.items():
        for flavor, source_keys in flavor_map.items():
            if flavor not in simulation_dataset or level not in simulation_dataset[flavor]["weighters"]:
                print(f"Skipping {flavor}/{level}, not merged")
                continue

            total_rows = 0
            for key in source_keys:
                # raw dataset
                if key in simulation_dataset and "hdf_files" in simulation_dataset[key] and level in simulation_dataset[key]["hdf_files"]:
                    total_rows += len(simulation_dataset[key]["hdf_files"][level]["I3EventHeader"])
                # merged flavor (like NuAll)
                elif key in simulation_dataset and "weighters" in simulation_dataset[key] and level in simulation_dataset[key]["weighters"]:
                    total_rows += len(simulation_dataset[key]["weighters"][level].get_column("I3MCWeightDict", "PrimaryNeutrinoEnergy"))

            merged_rows = len(simulation_dataset[flavor]["weighters"][level].get_column("I3MCWeightDict", "PrimaryNeutrinoEnergy"))

            if total_rows != merged_rows:
                sys.exit(f"[ERROR] {flavor}/{level}: merged {merged_rows} != sum {total_rows}")
    print("Merging is consistent")
