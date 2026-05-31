#!/usr/bin/env bash

version=v1
main_path=/data/user/tvaneede/GlobalFit/reco_processing/data/hese
hdf_script=/data/user/tvaneede/GlobalFit/reco_processing/hdf/to_hdf5.sh

data_path=${main_path}/output/${version}

for dir in ${data_path}/IC*; do

    indir=${dir}/EvtGen
    outfile=${indir}/EvtGen.h5

    # Skip if not a directory
    [[ -d "$indir" ]] || continue

    echo "---------------------------"
    echo "Processing $indir"
    echo "outfile $outfile"

    ${hdf_script} -o ${outfile} -i ${indir} -f Data


done