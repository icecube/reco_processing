#!/bin/bash
set -e  # Exit on error

# doesnt work in condor
/data/user/tvaneede/software/py_venvs/py3-v4.4.2_pyFF/bin/python \
    /data/user/tvaneede/GlobalFit/reco_processing/bdt/training/optimize_training/optimize_cuts/optimize_cuts.py \
    $@
