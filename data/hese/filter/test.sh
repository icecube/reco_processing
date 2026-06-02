#!/bin/bash

# ### One of the missing files from the Neha production
# RUN_DIR="/data/exp/IceCube/2013/filtered/level2pass2a/0727/Run00122752"
# GCD_FILE="${RUN_DIR}/Level2pass2_IC86.2013_data_Run00122752_0727_1_25_GCD.i3.zst"
# OUTPUT_DIR="/data/user/tvaneede/GlobalFit/reco_processing/data/hese/filter/output/test/IC86_2013"
# OUTPUT_FILE="${OUTPUT_DIR}/Run00122752.i3.zst"

# mkdir -p "${OUTPUT_DIR}"

# /cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell \
#     /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
#     /data/user/tvaneede/GlobalFit/reco_processing/data/hese/filter/filter_HESE.py \
#     --RunDir "${RUN_DIR}" \
#     --GCDfile "${GCD_FILE}" \
#     --Outputfile "${OUTPUT_FILE}"

### One of present files to check the reco, 122649
RUN_DIR="/data/exp/IceCube/2013/filtered/level2pass2a/0707/Run00122649/"
GCD_FILE="${RUN_DIR}/Level2pass2_IC86.2013_data_Run00122649_0707_1_21_GCD.i3.zst"
OUTPUT_DIR="/data/user/tvaneede/GlobalFit/reco_processing/data/hese/filter/output/test/IC86_2013"
OUTPUT_FILE="${OUTPUT_DIR}/Run00122649.i3.zst"

mkdir -p "${OUTPUT_DIR}"

/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
    /data/user/tvaneede/GlobalFit/reco_processing/data/hese/filter/filter_HESE.py \
    --RunDir "${RUN_DIR}" \
    --GCDfile "${GCD_FILE}" \
    --Outputfile "${OUTPUT_FILE}"