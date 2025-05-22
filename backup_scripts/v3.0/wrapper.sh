#!/bin/bash

set -e  # Exit on error

source /data/user/tvaneede/GlobalFit/reco_processing/setenv.sh

/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell /data/user/tvaneede/software/py_venvs/py3-v4.4.1_reco-v1.1.0/bin/python rec $@
