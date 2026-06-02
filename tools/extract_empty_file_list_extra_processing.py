import glob 
import os, sys
from collections import defaultdict


baseline_sets_dict = {
    "22663":
        {
            "id": 22663,
            "year": 2023,
            "name": "NuGen NuE high E",
            "flavor": "NuE",
            "nfiles_gen": 20000, # was 19693
        },
    "22664":
        {
            "id": 22664,
            "year": 2023,
            "name": "NuGen NuE mid E",
            "flavor": "NuE",
            "nfiles_gen": 4000, # was 3747
        },
    "22667":
        {
            "id": 22667,
            "year": 2023,
            "name": "NuGen NuTau mid E",
            "flavor": "NuTau",
            "nfiles_gen": 4000, # 3763
        },
    "22668":
        {
            "id": 22668,
            "year": 2023,
            "name": "NuGen NuTau high E",
            "flavor": "NuTau",
            "nfiles_gen": 20000, # 16563
        },

    "22670":
        {
            "id": 22670,
            "year": 2023,
            "name": "NuGen NuMu high E",
            "flavor": "NuMu",
            "nfiles_gen": 15000, # 9688
        },
    "22671":
        {
            "id": 22671,
            "year": 2023,
            "name": "NuGen NuMu mid E",
            "flavor": "NuMu",
            "nfiles_gen": 5000, # 4687
        },
}

def get_reco_file_path(level, year, dataset, subfolder):
    if level == "level2": return f"/data/sim/IceCube/{year}/filtered/level2/neutrino-generator/{dataset}/{subfolder}/"
    if level == "HESE_taupede": return f"/data/sim/IceCube/{year}/filtered/HESE/neutrino-generator/taupede/{dataset}/{subfolder}/"
    if level == "HESE_evtgen": return f"/data/sim/IceCube/{year}/filtered/HESE/neutrino-generator/evtgen/{dataset}/{subfolder}"

def file_index_to_subfolder(idx, block=1000):
    """
    Convert file index -> subfolder string like 0000000-0000999
    """
    start = (idx // block) * block
    end = start + block - 1
    return f"{start:07d}-{end:07d}"

def list_existing_indices(path, pattern="*.i3*"):
    """
    Extract file indices from filenames in a directory.
    Assumes filenames contain the index as a zero-padded integer.
    """
    indices = set()
    for f in glob.glob(os.path.join(path, pattern)):
        basename = os.path.basename(f)
        digits = "".join(c for c in basename if c.isdigit())
        if digits:
            indices.add(int(digits))
    return indices

def find_missing_level2_files(dataset_info):
    """
    Returns a dict:
      {subfolder: [missing_indices]}
    """
    year = dataset_info["year"]
    dataset = dataset_info["id"]
    nfiles = dataset_info["nfiles_gen"]
    flavor = dataset_info["flavor"]

    subfolders = [f"{i:07d}-{i+999:07d}" for i in range(0, nfiles, 1000)]

    missing = {}
    file_list = []

    for subfolder in subfolders:
        path = get_reco_file_path("level2", year, dataset, subfolder)

        lower_bound = int(subfolder.split("-")[-2])

        missing[subfolder] = []

        for run_id in range(0,1000):

            run_number = f"{run_id+lower_bound:06d}"
            
            file_path = f"{path}/Level2_{flavor}_NuGenCCNC.0{dataset}.{run_number}.i3.zst"

            if not os.path.isfile(file_path):
                missing[subfolder].append(run_number)
                file_list.append(file_path)
                continue

    return missing, file_list

def check_hese_levels(missing_dict, dataset_info, level="HESE_taupede"):
    """
    For each missing level2 file, check if it exists at HESE levels.
    Returns:
      {level: {subfolder: [indices_found]}}
    """
    year = dataset_info["year"]
    dataset = dataset_info["id"]
    flavor = dataset_info["flavor"]

    found = {}
    file_list = []

    for subfolder, run_numbers in missing_dict.items():
        found[subfolder] = []
        for run_number in run_numbers:
            path = get_reco_file_path(level, year, dataset, subfolder)

            file_path = f"{path}/HESE_{flavor}_NuGenCCNC.0{dataset}.{run_number}.i3.zst"
            if os.path.isfile(file_path):
                found[subfolder].append(run_number)
                file_list.append(file_path)
                continue

    return found, file_list

all_results = {}

missing_level2_all = []
taupede_found_all = []
evtgen_found_all = []

for ds_key, ds_info in baseline_sets_dict.items():
    print(f"=== Dataset {ds_key}: {ds_info['name']} ===")

    missing_level2,missing_level2_list = find_missing_level2_files(ds_info)
    print(f"Missing level2 files: {sum(len(v) for v in missing_level2.values())} of {ds_info['nfiles_gen']}")

    taupede_found,taupede_found_list = check_hese_levels(missing_level2, ds_info, level="HESE_taupede")
    print(f"Found hese taupede files: {sum(len(v) for v in taupede_found.values())}")

    evtgen_found,evtgen_found_list = check_hese_levels(missing_level2, ds_info, level="HESE_evtgen")
    print(f"Found hese taupede files: {sum(len(v) for v in evtgen_found.values())}")

    # accumulate
    missing_level2_all.extend(missing_level2_list)
    taupede_found_all.extend(taupede_found_list)
    evtgen_found_all.extend(evtgen_found_list)

    # break

for outname, files in zip(["missing_level2.txt","taupede_found.txt","evtgen_found.txt"],
                            [missing_level2_all,taupede_found_all,evtgen_found_all]):
    with open(f"extract_empty_file_list_extra_processing/{outname}", "w+") as f:
        for path in files:
            f.write(path + "\n")