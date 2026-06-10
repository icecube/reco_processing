#!/bin/bash
# Run check_active_strings.py with the icetray environment.
# All arguments are forwarded to the Python script.
#   ./run.sh                              # all datasets, version v2, Taupede
#   ./run.sh --version v1
#   ./run.sh --datasets IC86_2016 IC86_2017
#   ./run.sh --reco-type EvtGen

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ICETRAY_SHELL=/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell
PYTHON=/cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python

"$ICETRAY_SHELL" "$PYTHON" "$SCRIPT_DIR/check_active_strings.py" "$@" \
    2>&1 | tee "$SCRIPT_DIR/check_active_strings.log"
