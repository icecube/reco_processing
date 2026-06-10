#!/usr/bin/env bash

version=v3
main_path=/data/user/tvaneede/GlobalFit/reco_processing/data/hese

data_path=${main_path}/output/${version}
out_path=${data_path}/merged

mkdir -p ${out_path}

python_exec=/data/user/tvaneede/software/py_venvs/py3-v4.4.1_reco-v1.1.0/bin/python
merge_script=/data/user/tvaneede/GlobalFit/reco_processing/hdf/merge.py

outfile=${out_path}/EvtGen_merged.h5

# Collect all input files
infiles=""

for dir in ${data_path}/IC*; do

    h5file=${dir}/EvtGen/EvtGen.h5

    # Skip missing files
    [[ -f "$h5file" ]] || continue

    echo "Adding $h5file"

    infiles="${infiles} ${h5file}"

done

echo "---------------------------"
echo "Merging files"
echo "Output: ${outfile}"

${python_exec} ${merge_script} -o ${outfile} ${infiles}