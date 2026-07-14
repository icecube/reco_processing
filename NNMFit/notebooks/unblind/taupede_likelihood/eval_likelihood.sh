#!/bin/bash
# Wrapper to run eval_likelihood.py in the correct icetray environment.
#
# Usage:
#   ./eval_likelihood.sh <i3file> [--reco taupede|monopod] [options]
#
# All arguments are forwarded to eval_likelihood.py.  Run with --help for
# the full option list.
#
# Examples:
#   ./eval_likelihood.sh Run00126320.i3.zst
#   ./eval_likelihood.sh Run00126320.i3.zst --reco monopod
#   ./eval_likelihood.sh Run00126320.i3.zst --event-id 12345 --zenith 45.0 --azimuth 180.0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ICETRAY_SHELL=/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell
PYTHON=/cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python

exec "$ICETRAY_SHELL" "$PYTHON" "$SCRIPT_DIR/eval_likelihood.py" "$@"
