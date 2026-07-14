#!/bin/bash
# Run cascade taupede reconstruction for Run00126320.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

GCD_FILE=/data/exp/IceCube/2015/filtered/level2pass2/0502/Run00126320/Level2pass2_IC86.2014_data_Run00126320_0502_1_163_GCD.i3.zst
INFILE=/data/user/zchen/pass2_cascade_nutau/taupede/file/data/IC86_2014/burn/final_cascade/Finallevel_IC86_2014_data_Run00126320.i3.zst
OUTFILE=${SCRIPT_DIR}/Run00126320_cascade_rerun.i3.zst

HESE_FILE=/data/user/tvaneede/GlobalFit/reco_processing/data/hese/output/v3/IC86_2014/Taupede/Run00126320.i3.zst

echo "GCD:     ${GCD_FILE}"
echo "INFILE:  ${INFILE}"
echo "OUTFILE: ${OUTFILE}"
echo "HESE:    ${HESE_FILE}"

export PYTHONPATH=/home/zchen/taupede/ftp_reco/code/:${PYTHONPATH}

###
### Running just like Zheyang
###

# /cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/icetray-env icetray/v1.14.0 \
#     /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
#     "${SCRIPT_DIR}/addftp_reco.py" \
#     -o "${OUTFILE}" \
#     --isdata --imigrad --icemodel ftp-v1 --tilt --effd --effp \
#     --eval-file "${HESE_FILE}" \
#     --eval-particles-key TaupedeFit_iMIGRAD_PPB0Particles \
#     "${GCD_FILE}" "${INFILE}"

# --- Run 126320  Event 6425207 ---
#   Taupede_ftpParticles (2 particles):
#     [0]  pos=(-225.85, 262.08, 256.19) m  zen=120.602 deg  az=172.935 deg  E=620.05 GeV  t=9733.71 ns  L=14.95 m
#     [1]  pos=(-213.08, 260.50, 263.81) m  zen=120.602 deg  az=172.935 deg  E=34955.09 GeV  t=9783.59 ns  L=0.00 m
#   Stored  logl=5696.868424  rlogl=5.965307  ndof=955
#   PyMillipede (reval ftp):  logl=5696.868424  ndof=6377
#   Delta logl: +0.000000
#   TaupedeFit_iMIGRAD_PPB0Particles (2 particles):
#     [0]  pos=(-214.74, 266.38, 262.96) m  zen=120.322 deg  az=153.149 deg  E=30655.04 GeV  t=9775.00 ns  L=29.48 m
#     [1]  pos=(-192.04, 254.89, 277.85) m  zen=120.322 deg  az=153.149 deg  E=3530.91 GeV  t=9873.34 ns  L=0.00 m
#   PyMillipede (TaupedeFit_iMIGRAD_PPB0Particles):  logl=5721.533235  ndof=6377
#   Delta logl: +24.664811

###
### mintimewidth 8 default cascade
### gives default as above
###

# /cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/icetray-env icetray/v1.14.0 \
#     /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
#     "${SCRIPT_DIR}/addftp_reco.py" \
#     -o "${OUTFILE}" \
#     --isdata --imigrad --icemodel ftp-v1 --tilt --effd --effp \
#     --eval-file "${HESE_FILE}" \
#     --eval-particles-key TaupedeFit_iMIGRAD_PPB0Particles \
#     --mintimewidth 8 \
#     "${GCD_FILE}" "${INFILE}"

# --- Run 126320  Event 6425207 ---
#   Taupede_ftpParticles (2 particles):
#     [0]  pos=(-225.85, 262.08, 256.19) m  zen=120.602 deg  az=172.935 deg  E=620.05 GeV  t=9733.71 ns  L=14.95 m
#     [1]  pos=(-213.08, 260.50, 263.81) m  zen=120.602 deg  az=172.935 deg  E=34955.09 GeV  t=9783.59 ns  L=0.00 m
#   Stored  logl=5696.868424  rlogl=5.965307  ndof=955
#   PyMillipede (reval ftp):  logl=5696.868424  ndof=6377
#   Delta logl: +0.000000
#   TaupedeFit_iMIGRAD_PPB0Particles (2 particles):
#     [0]  pos=(-214.74, 266.38, 262.96) m  zen=120.322 deg  az=153.149 deg  E=30655.04 GeV  t=9775.00 ns  L=29.48 m
#     [1]  pos=(-192.04, 254.89, 277.85) m  zen=120.322 deg  az=153.149 deg  E=3530.91 GeV  t=9873.34 ns  L=0.00 m
#   PyMillipede (TaupedeFit_iMIGRAD_PPB0Particles):  logl=5721.533235  ndof=6377
#   Delta logl: +24.664811


###
### mintimewidth 16 default hese
### gives default as above
###

# /cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/icetray-env icetray/v1.14.0 \
#     /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
#     "${SCRIPT_DIR}/addftp_reco.py" \
#     -o "${OUTFILE}" \
#     --isdata --imigrad --icemodel ftp-v1 --tilt --effd --effp \
#     --eval-file "${HESE_FILE}" \
#     --eval-particles-key TaupedeFit_iMIGRAD_PPB0Particles \
#     --mintimewidth 16 \
#     "${GCD_FILE}" "${INFILE}"


# --- Run 126320  Event 6425207 ---
#   Taupede_ftpParticles (2 particles):
#     [0]  pos=(-219.39, 259.39, 261.98) m  zen=114.716 deg  az=177.350 deg  E=22016.68 GeV  t=9765.79 ns  L=19.10 m
#     [1]  pos=(-202.06, 258.59, 269.96) m  zen=114.716 deg  az=177.350 deg  E=12298.37 GeV  t=9829.48 ns  L=0.00 m
#   Stored  logl=4099.999736  rlogl=4.857820  ndof=844
#   PyMillipede (reval ftp):  logl=4099.999736  ndof=6041
#   Delta logl: +0.000000
#   TaupedeFit_iMIGRAD_PPB0Particles (2 particles):
#     [0]  pos=(-214.74, 266.38, 262.96) m  zen=120.322 deg  az=153.149 deg  E=30655.04 GeV  t=9775.00 ns  L=29.48 m
#     [1]  pos=(-192.04, 254.89, 277.85) m  zen=120.322 deg  az=153.149 deg  E=3530.91 GeV  t=9873.34 ns  L=0.00 m
#   PyMillipede (TaupedeFit_iMIGRAD_PPB0Particles):  logl=4100.741572  ndof=6041
#   Delta logl: +0.741836

###
### update to latest GCD
###

GCD_FILE=/data/exp/IceCube/2015/filtered/level2pass2a/0502/Run00126320/Level2pass2_IC86.2014_data_Run00126320_0502_1_163_GCD.i3.zst

/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/icetray-env icetray/v1.14.0 \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
    "${SCRIPT_DIR}/addftp_reco.py" \
    -o "${OUTFILE}" \
    --isdata --imigrad --icemodel ftp-v1 --tilt --effd --effp \
    --eval-file "${HESE_FILE}" \
    --eval-particles-key TaupedeFit_iMIGRAD_PPB0Particles \
    --mintimewidth 16 \
    "${GCD_FILE}" "${INFILE}"

# --- Run 126320  Event 6425207 ---
#   Taupede_ftpParticles (2 particles):
#     [0]  pos=(-219.39, 259.39, 261.98) m  zen=114.716 deg  az=177.350 deg  E=22016.68 GeV  t=9765.79 ns  L=19.10 m
#     [1]  pos=(-202.06, 258.59, 269.96) m  zen=114.716 deg  az=177.350 deg  E=12298.37 GeV  t=9829.48 ns  L=0.00 m
#   Stored  logl=4099.999736  rlogl=4.857820  ndof=844
#   PyMillipede (reval ftp):  logl=4099.999736  ndof=6041
#   Delta logl: +0.000000
#   TaupedeFit_iMIGRAD_PPB0Particles (2 particles):
#     [0]  pos=(-214.74, 266.38, 262.96) m  zen=120.322 deg  az=153.149 deg  E=30655.04 GeV  t=9775.00 ns  L=29.48 m
#     [1]  pos=(-192.04, 254.89, 277.85) m  zen=120.322 deg  az=153.149 deg  E=3530.91 GeV  t=9873.34 ns  L=0.00 m
#   PyMillipede (TaupedeFit_iMIGRAD_PPB0Particles):  logl=4100.741572  ndof=6041
#   Delta logl: +0.741836