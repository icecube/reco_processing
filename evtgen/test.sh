#!/bin/bash

# using mirco's environment
/cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/RHEL_7_x86_64/metaprojects/icetray/v1.12.0/env-shell.sh /mnt/ceph1-npx/user/mhuennefeld/DNN_reco/virtualenvs/tensorflow_gpu_py3-v4.3.0/bin/python /data/user/tvaneede/GlobalFit/reco_processing/evtgen/run_event_generator.py \
        --Inputfile /data/user/tvaneede/GlobalFit/reco_processing/output/v1/22635/0000000-0000999/Reco_NuTau_NuGenCCNC.022635.000001.i3.zst_out.i3.bz2 \
        --Outputfile /data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/test/test.i3.bz2

# my own environment
