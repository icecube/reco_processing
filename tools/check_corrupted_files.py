import os
from glob import glob
from icecube import dataio

def check_file_integrity(file_path):
    try:
        reader = dataio.I3File(file_path)
        while reader.more():
            reader.pop_frame()
        return True
    except Exception as e:
        print(f"[CORRUPT] {file_path}\n  --> {type(e).__name__}: {e}")
        return False

directory = "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator/22043/0000000-0000999/"
i3_files = sorted(glob(os.path.join(directory, "*.i3.zst")))

print(f"Checking {len(i3_files)} files for corruption...")

for i, file_path in enumerate(i3_files, 1):
    print(f"[{i}/{len(i3_files)}] Checking {os.path.basename(file_path)}...")
    check_file_integrity(file_path)
