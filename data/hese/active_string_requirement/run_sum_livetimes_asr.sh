#!/bin/bash
# Run sum_livetimes_asr.py with the icetray environment.
# All arguments are forwarded to the Python script.
#   ./run_sum_livetimes_asr.sh
#   ./run_sum_livetimes_asr.sh --datasets IC86_2016 IC86_2017

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ICETRAY_SHELL=/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell
PYTHON=/cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python

"$ICETRAY_SHELL" "$PYTHON" "$SCRIPT_DIR/sum_livetimes_asr.py" "$@" \
    2>&1 | tee "$SCRIPT_DIR/sum_livetimes_asr.log"
