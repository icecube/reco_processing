#!/bin/bash

set -e  # Exit on error

source /data/user/tvaneede/GlobalFit/reco_processing/setenv.sh

/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell /data/user/tvaneede/software/py_venvs/py3-v4.4.1_reco-v1.1.0/bin/python /data/user/tvaneede/GlobalFit/reco_processing/hdf/to_hdf5.py $@





# # python /data/user/tvaneede/GlobalFit/reco_processing/hdf/to_hdf5.py -o /data/user/tvaneede/GlobalFit/reco_processing/hdf/output/test/test.h5 i3s /data/user/tvaneede/GlobalFit/reco_processing/output/v7.0/22635/0000000-0000999/Reco_NuTau_NuGenCCNC.022635.000001.i3.zst_out.i3.bz2 /data/user/tvaneede/GlobalFit/reco_processing/output/v7.0/22635/0000000-0000999/Reco_NuTau_NuGenCCNC.022635.000002.i3.zst_out.i3.bz2 \ 


# python /data/user/tvaneede/GlobalFit/reco_processing/hdf/to_hdf5.py \
#     -o /data/user/tvaneede/GlobalFit/reco_processing/hdf/output/test/test.h5 \
#     /data/user/tvaneede/GlobalFit/reco_processing/output/v7.0/22635/0000000-0000999/Reco_NuTau_NuGenCCNC.022635.000001.i3.zst_out.i3.bz2 \
#     /data/user/tvaneede/GlobalFit/reco_processing/output/v7.0/22635/0000000-0000999/Reco_NuTau_NuGenCCNC.022635.000002.i3.zst_out.i3.bz2
