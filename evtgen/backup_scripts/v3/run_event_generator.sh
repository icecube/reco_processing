#!/bin/bash

set -e  # Exit on error

/cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/RHEL_7_x86_64/metaprojects/icetray/v1.12.0/env-shell.sh /mnt/ceph1-npx/user/mhuennefeld/DNN_reco/virtualenvs/tensorflow_gpu_py3-v4.3.0/bin/python /data/user/tvaneede/GlobalFit/reco_processing/evtgen/run_event_generator.py $@


