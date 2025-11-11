#!/bin/bash
GCD=/cvmfs/icecube.opensciencegrid.org/users/tvaneede/gcd/gcd_pass2_rde.i3.gz

INPATH=${1}
INFILE=${2}
OUTPATH=${3}

OUTPATH_TAUPEDE=${OUTPATH}/Taupede
OUTPATH_TAUPEDE_IBR=${OUTPATH}/Taupede_ibr
OUTPATH_TAUPEDE_IBR_IDC=${OUTPATH}/Taupede_ibr_idc
OUTPATH_EVTGEN=${OUTPATH}/EvtGen

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

OUTFILE=${OUTPATH_TAUPEDE}/${INFILE/HESE/Taupede}
INFILEPATH=${INPATH}/${INFILE}

echo "-----------------------------"
echo "Regular"
echo "OUTFILE" ${OUTFILE}
echo "INFILEPATH" ${INFILEPATH}

/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/icetray-env icetray/v1.14.0 \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/reco_processing/v1/rec_tau.py \
    -o ${OUTFILE} \
    --imigrad --icemodel ftp-v1 --tilt --effd --effp --qs $GCD \
    ${INFILEPATH}


###
### Bright
###

OUTFILE_IBR=${OUTPATH_TAUPEDE_IBR}/${INFILE/HESE/Taupede_ibr}

echo "-----------------------------"
echo "IBR"
echo "OUTFILE" ${OUTFILE_IBR}
echo "INFILE" ${OUTFILE}

/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/icetray-env icetray/v1.14.0 \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/reco_processing/v1/rec_tau.py \
    -o ${OUTFILE_IBR} \
    --imigrad --icemodel ftp-v1 --tilt --effd --effp --ibr --qs $GCD \
    ${OUTFILE}


###
### Bright + DC
###

OUTFILE_IBR_IDC=${OUTPATH_TAUPEDE_IBR_IDC}/${INFILE/HESE/Taupede_ibr_idc}

echo "-----------------------------"
echo "IBR IDC"
echo "OUTFILE" ${OUTFILE_IBR_IDC}
echo "INFILE" ${OUTFILE_IBR}

/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/icetray-env icetray/v1.14.0 \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/reco_processing/v1/rec_tau.py \
    -o ${OUTFILE_IBR_IDC} \
    --imigrad --icemodel ftp-v1 --tilt --effd --effp --ibr --idc --qs $GCD \
    ${OUTFILE_IBR}

###
### EvtGen
###

OUTFILE_EVTGEN=${OUTPATH_EVTGEN}/${INFILE/HESE/EvtGen}

echo "-----------------------------"
echo "EvtGen"
echo "OUTFILE" ${OUTFILE_EVTGEN}
echo "INFILE" ${OUTFILE_IBR_IDC}

/cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/icetray-env icetray/v1.12.0 \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/tensorflow_gpu_py3-v4.3.0/bin/python \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/reco_processing/v0/run_event_generator.py \
    --Inputfile ${OUTFILE_IBR_IDC} \
    --Outputfile ${OUTFILE_EVTGEN}
