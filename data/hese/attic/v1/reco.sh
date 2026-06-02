#!/bin/bash
set -e

INPATH=${1}
OUTPATH=${2}

OUTPATH_TAUPEDE=${OUTPATH}/Taupede
OUTPATH_EVTGEN=${OUTPATH}/EvtGen

mkdir -p ${OUTPATH}
mkdir -p ${OUTPATH_TAUPEDE}
mkdir -p ${OUTPATH_EVTGEN}

echo "-----------------------------"
echo "Running"
echo "INPATH" ${INPATH}
echo "OUTPATH" ${OUTPATH}
echo "-----------------------------"

###
### Regular
###

OUTFILE=${OUTPATH_TAUPEDE}/Taupede.i3.zst

echo "-----------------------------"
echo "Regular"
echo "INPATH" ${INPATH}
echo "OUTFILE" ${OUTFILE}

/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/icetray-env icetray/v1.14.0 \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
    /data/user/tvaneede/GlobalFit/reco_processing/iceprod/scripts/v1/rec_tau_data_hese.py \
    -o ${OUTFILE} \
    --imigrad --icemodel ftp-v1 --tilt --effd --effp --qs --isdata \
    ${INPATH}/*.i3.zst

##
## EvtGen
##

OUTFILE_EVTGEN=${OUTPATH_EVTGEN}/EvtGen.i3.zst

echo "-----------------------------"
echo "EvtGen"
echo "OUTFILE" ${OUTFILE_EVTGEN}
echo "INFILE" ${OUTFILE}

/cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/icetray-env icetray/v1.12.0 \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/tensorflow_gpu_py3-v4.3.0/bin/python \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/reco_processing/v0/run_event_generator.py \
    --Inputfile ${OUTFILE} \
    --Outputfile ${OUTFILE_EVTGEN}
