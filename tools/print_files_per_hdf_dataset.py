import os
import re
from collections import defaultdict

version = "ftp_ensemble_v0"
LOGDIR = f"/scratch/tvaneede/reco/hdf_iceprod/{version}/logs"

found_pattern = re.compile(r"\bfound\s+(\d+)\b")
using_pattern = re.compile(r"\busing\s+(\d+)\b")

# nested default dict (two levels)
data_found = defaultdict(lambda: defaultdict(dict))
data_using = defaultdict(lambda: defaultdict(dict))

total_files = 0
found_files = 0
used_files = 0

for filename in os.listdir(LOGDIR):
    if not filename.endswith(".out"):
        continue
    
    total_files += 1

    filename_split = filename.split("_")

    file_range = filename_split[-1].replace(".out", "")
    dataset = filename_split[-2]
    prefix = "_".join(filename_split[:-2])

    filepath = os.path.join(LOGDIR, filename)
    with open(filepath, "r", errors="ignore") as f:
        text = f.read()

    found_match = found_pattern.search(text)
    used_match = using_pattern.search(text)
    if found_match:
        found_files += 1
        found_num = int(found_match.group(1))
        data_found[dataset][prefix][file_range] = found_num
    else:
        data_found[dataset][prefix][file_range] = None  # mark missing "found"
    if used_match:
        used_files += 1
        used_num = int(used_match.group(1))
        data_using[dataset][prefix][file_range] = used_num
    else:
        data_using[dataset][prefix][file_range] = None  # mark missing "found"

# --- summary output ---
print(f"Processed {total_files} .out files")
print(f"Found 'found N' in {found_files} files\n")
print(f"Found 'using N' in {used_files} files\n")

for dataset, prefixes in sorted(data_found.items()):
    print(f"Dataset {dataset}")
    for prefix, ranges in sorted(prefixes.items()):
        # calculate sum for this level/prefix
        level_sum = sum(v for v in ranges.values() if v is not None)
        print(f"  {prefix} total found: {level_sum}")
        for r, val in sorted(ranges.items()):
            print(f"    {r}: {val if val is not None else '(no found)'}")
        
        ranges = data_using[dataset][prefix]
        level_sum = sum(v for v in ranges.values() if v is not None)
        print(f"  {prefix} total used: {level_sum}")
        # for r, val in sorted(ranges.items()):
        #     print(f"    {r}: {val if val is not None else '(no found)'}")