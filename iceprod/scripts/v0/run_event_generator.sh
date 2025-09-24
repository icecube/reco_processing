#!/bin/bash
/cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/RHEL_7_x86_64/metaprojects/icetray/v1.12.0/env-shell.sh \
        /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/tensorflow_gpu_py3-v4.3.0/bin/python \
        /cvmfs/icecube.opensciencegrid.org/users/tvaneede/reco_processing/v0/run_event_generator.py $@
