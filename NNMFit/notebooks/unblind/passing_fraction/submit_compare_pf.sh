#!/bin/bash
SCRIPT_DIR="/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/unblind/passing_fraction"

source "$SCRIPT_DIR/setenv.sh"

python "$SCRIPT_DIR/compare_pf_spline_vs_nuveto.py" "$@"
