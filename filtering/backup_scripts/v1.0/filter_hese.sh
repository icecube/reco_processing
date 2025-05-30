#!/bin/bash

set -e  # Exit on error

source /data/user/tvaneede/GlobalFit/reco_processing/setenv.sh

INPUTPATH=$1
OUTPUTPATH=$2

for file in ${INPUTPATH}/*.i3.zst; do
    echo "------------------------------ Processing $file"
    filename="${file##*/}"
    outputfile=${OUTPUTPATH}/${filename}

    /cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell /data/user/tvaneede/software/py_venvs/py3-v4.4.1_reco-v1.1.0/bin/python /data/user/tvaneede/GlobalFit/reco_processing/filtering/filter_hese.py --Inputfile ${file} --Outputfile ${outputfile}
done