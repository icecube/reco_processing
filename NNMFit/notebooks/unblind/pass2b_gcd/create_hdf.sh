#!/usr/bin/env bash

hdf_script=/data/user/tvaneede/GlobalFit/reco_processing/hdf/to_hdf5.sh

data_path=/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/unblind/pass2b_gcd

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