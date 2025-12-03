#!/bin/bash

set -e  # Exit on error

### this env has not working muongun
# source /data/user/tvaneede/GlobalFit/reco_processing/setenv.sh
# /cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell /data/user/tvaneede/software/py_venvs/py3-v4.4.1_reco-v1.1.0/bin/python /data/user/tvaneede/GlobalFit/reco_processing/hdf/to_hdf5.py $@

## older environment, muongun works
# source /data/user/tvaneede/software/py_venvs/py3-v4.3.0_reco-v1.1.0_icetray-v1.12.0/bin/activate
# /cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/RHEL_7_x86_64/metaprojects/icetray/v1.12.0/env-shell.sh /data/user/tvaneede/software/py_venvs/py3-v4.3.0_reco-v1.1.0_icetray-v1.12.0/bin/python /data/user/tvaneede/GlobalFit/reco_processing/hdf/to_hdf5.py $@

# ## get rid of RHEL_7, ALMA now
# /cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/icetray-env icetray/v1.12.0 \
#     /data/user/tvaneede/software/py_venvs/py3-v4.3.0_reco-v1.1.0_icetray-v1.12.0/bin/python \
#     /data/user/tvaneede/GlobalFit/reco_processing/hdf/to_hdf5.py $@

## lets see if I can get rid off the hdf writer error
/cvmfs/icecube.opensciencegrid.org/py3-v4.4.2/icetray-env icetray/v1.16.0 \
    /data/user/tvaneede/software/py_venvs/py3-v4.4.2_reco-v1.2.3_icetray-v1.16.0/bin/python \
    /data/user/tvaneede/GlobalFit/reco_processing/hdf/to_hdf5.py $@
