#!/usr/bin/env bash

version=neha_event
main_path=/data/user/tvaneede/GlobalFit/reco_processing/data/hese
hdf_script=/data/user/tvaneede/GlobalFit/reco_processing/hdf/to_hdf5.sh

data_path=/data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/i3files/NoDeepCore/HESE12/Bfr
outdir=${main_path}/output/${version}

mkdir -p ${outdir}

for dir in ${data_path}/IC*; do

    outfile=${outdir}/$(basename ${dir}).h5

    # Skip if not a directory
    [[ -d "$dir" ]] || continue

    echo "---------------------------"
    echo "Processing $dir"
    echo "outfile $outfile"

    ${hdf_script} -o ${outfile} -i ${dir} -f Data

done