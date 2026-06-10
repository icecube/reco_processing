#!/usr/bin/env bash

main_path=/data/user/tvaneede/GlobalFit/reco_processing/data/hese
hdf_script=/data/user/tvaneede/GlobalFit/reco_processing/hdf/to_hdf5.sh
outpath=/data/user/tvaneede/GlobalFit/reco_processing/data/hese/output/emre_new

data_path=/data/user/eyildizci/hese_tracks_processing/L5/

for dir in ${data_path}/new_IC*; do

    indir=${dir}
    outfile=${outpath}/$(basename ${dir}).h5

    # Skip if not a directory
    [[ -d "$indir" ]] || continue

    echo "---------------------------"
    echo "Processing $indir"
    echo "outfile $outfile"

    ${hdf_script} -o ${outfile} -i ${indir} -f Data


done