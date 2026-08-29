#!/bin/sh

ICETRAY_SHELL="/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell"
PYTHON="/cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python"
SCRIPT="/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/unblind/passing_fraction/plights_tianlu/pf_grid_fitter.py"

RES="/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/unblind/passing_fraction/plights_tianlu/pf_grid/hese_plight_11dep_21cth_51ene/"
OUT="/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/unblind/passing_fraction/plights_tianlu/splines/hese_plight_11dep_21cth_51ene/"

"$ICETRAY_SHELL" "$PYTHON" "$SCRIPT" --res "$RES" --out "$OUT"
