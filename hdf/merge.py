import h5py
import shutil
import sys
import os
import argparse

def merge_datasets(target, source):
    for name, item in source.items():
        if isinstance(item, h5py.Dataset):
            if name not in target:
                source.copy(name, target)
            else:
                dset_src = item[...] # load source data into memory
                dset_dst = target[name]
                if dset_dst.shape[1:] != dset_src.shape[1:]: # enforce dataset to only differ along axis 0, index
                    raise ValueError(f"Shape mismatch in dataset '{name}'")
                new_size = dset_dst.shape[0] + dset_src.shape[0]
                dset_dst.resize((new_size,) + dset_dst.shape[1:])
                dset_dst[-dset_src.shape[0]:] = dset_src
        elif isinstance(item, h5py.Group):
            if name not in target:
                target.create_group(name)
            merge_datasets(target[name], item)

def merge_hdf5_files(output_file, input_files):
    if not input_files:
        raise ValueError("No input files provided.")

    # Start with a copy of the first file
    shutil.copyfile(input_files[0], output_file)

    with h5py.File(output_file, 'a') as fout:
        for f in input_files[1:]:
            print(f"Merging {f}...")
            with h5py.File(f, 'r') as fin:
                merge_datasets(fout, fin)

if __name__ == "__main__":
    # Example usage:
    # python merge_hdf5.py output.h5 input1.h5 input2.h5 input3.h5
    if len(sys.argv) < 4:
        print("Usage: python merge_hdf5.py output.h5 input1.h5 input2.h5 ...")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description='Extract CausalQTot and MJD data from i3 to h5')

    parser.add_argument('inputs', nargs='+', help='input i3s')
    parser.add_argument('-o', '--out', default='merge.h5',
                        type=str, help='output file')
    args = parser.parse_args()

    output = args.out
    inputs = args.inputs

    merge_hdf5_files(output, inputs)


