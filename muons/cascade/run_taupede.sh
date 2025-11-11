#!/bin/bash
GCD=/cvmfs/icecube.opensciencegrid.org/users/tvaneede/gcd/gcd_pass2_rde.i3.gz

INPATH=${1}
INFILE=${2}
OUTPATH=${3}

OUTPATH_TAUPEDE=${OUTPATH}
OUTPATH_EVTGEN=${OUTPATH}

mkdir -p ${OUTPATH_TAUPEDE}
mkdir -p ${OUTPATH_EVTGEN}

echo "-----------------------------"
echo "Running"
echo "INPATH" ${INPATH}
echo "INFILE" ${INFILE}
echo "OUTPATH" ${OUTPATH}
echo "OUTPATH_TAUPEDE" ${OUTPATH_TAUPEDE}
echo "OUTPATH_EVTGEN" ${OUTPATH_EVTGEN}
echo "-----------------------------"

###
### Regular
###

OUTFILE=${OUTPATH_TAUPEDE}/${INFILE/Finallevel_IC86/Taupede}

# Collect all input files (e.g. *.i3.zst) into a variable
INFILENAMES=(${INPATH}/*.i3.zst)

echo "-----------------------------"
echo "Regular"
echo "OUTFILE" ${OUTFILE}
echo "INFILENAMES" "${INFILENAMES[@]}"

# /cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell \
/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/icetray-env icetray/v1.14.0 \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/reco_processing/v1/rec_tau.py \
    -o ${OUTFILE} \
    --imigrad --icemodel ftp-v1 --tilt --effd --effp --qs $GCD \
    "${INFILENAMES[@]}"


###
### Bright
###

OUTFILE_IBR=${OUTPATH_TAUPEDE}/${INFILE/Finallevel_IC86/Taupede_ibr}

echo "-----------------------------"
echo "IBR"
echo "OUTFILE" ${OUTFILE_IBR}
echo "INFILE" ${OUTFILE}

# /cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell \
/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/icetray-env icetray/v1.14.0 \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/reco_processing/v1/rec_tau.py \
    -o ${OUTFILE_IBR} \
    --imigrad --icemodel ftp-v1 --tilt --effd --effp --ibr --qs $GCD \
    ${OUTFILE}


###
### Bright + DC
###

OUTFILE_IBR_IDC=${OUTPATH_TAUPEDE}/${INFILE/Finallevel_IC86/Taupede_ibr_idc}

echo "-----------------------------"
echo "IBR IDC"
echo "OUTFILE" ${OUTFILE_IBR_IDC}
echo "INFILE" ${OUTFILE_IBR}

# /cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell \
/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/icetray-env icetray/v1.14.0 \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/reco_processing/v1/rec_tau.py \
    -o ${OUTFILE_IBR_IDC} \
    --imigrad --icemodel ftp-v1 --tilt --effd --effp --ibr --idc --qs $GCD \
    ${OUTFILE_IBR}

###
### EvtGen
###

OUTFILE_EVTGEN=${OUTPATH_EVTGEN}/${INFILE/Finallevel_IC86/EvtGen}

echo "-----------------------------"
echo "EvtGen"
echo "OUTFILE" ${OUTFILE_EVTGEN}
echo "INFILE" ${OUTFILE_IBR_IDC}

# /cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/RHEL_7_x86_64/metaprojects/icetray/v1.12.0/env-shell.sh \
/cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/icetray-env icetray/v1.12.0 \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/tensorflow_gpu_py3-v4.3.0/bin/python \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/reco_processing/v0/run_event_generator.py \
    --Inputfile ${OUTFILE_IBR_IDC} \
    --Outputfile ${OUTFILE_EVTGEN}
