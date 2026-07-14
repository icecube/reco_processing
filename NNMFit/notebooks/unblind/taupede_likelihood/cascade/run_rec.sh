#!/bin/bash
# Run cascade taupede reconstruction for Run00126320.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

GCD_FILE=/data/exp/IceCube/2015/filtered/level2pass2/0502/Run00126320/Level2pass2_IC86.2014_data_Run00126320_0502_1_163_GCD.i3.zst
INFILE=/data/user/zchen/pass2_cascade_nutau/taupede/file/data/IC86_2014/burn/final_cascade/Finallevel_IC86_2014_data_Run00126320.i3.zst
OUTFILE=${SCRIPT_DIR}/Run00126320_cascade_rerun_thijs.i3.zst

echo "GCD:     ${GCD_FILE}"
echo "INFILE:  ${INFILE}"
echo "OUTFILE: ${OUTFILE}"

export PYTHONPATH="/home/zchen/.local/lib/python3.11/site-packages:${PYTHONPATH}"

/home/zchen/taupede/ftp_reco/code/addftp_reco.py \
    -o "${OUTFILE}" \
    --isdata --imigrad --qepsilon 1 --icemodel ftp-v1 --tilt --effd --effp --hypo tau \
    "${GCD_FILE}" "${INFILE}"
