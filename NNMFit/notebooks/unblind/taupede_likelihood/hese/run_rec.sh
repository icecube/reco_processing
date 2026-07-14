#!/bin/bash
# Re-run taupede reconstruction for Run00126320 using the local copy of
# rec_tau_data_hese.py (which prints millipede_params to stdout).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

INFILE=/data/user/tvaneede/GlobalFit/reco_processing/data/hese/filter/output/v2/IC86_2014/Run00126320.i3.zst
OUTFILE=${SCRIPT_DIR}/Run00126320_rerun.i3.zst

echo "INFILE:  ${INFILE}"
echo "OUTFILE: ${OUTFILE}"

/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/icetray-env icetray/v1.14.0 \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
    "${SCRIPT_DIR}/rec_tau_data_hese.py" \
    -o "${OUTFILE}" \
    --imigrad --icemodel ftp-v1 --tilt --effd --effp --qs --isdata \
    "${INFILE}"
