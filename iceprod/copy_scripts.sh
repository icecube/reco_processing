#!/bin/sh
version=$1

local_path=/data/user/tvaneede/GlobalFit/reco_processing/iceprod/scripts/${version}
cvmfs_path=/net/cvmfs_users/tvaneede/reco_processing

mkdir -p ${local_path}

cp -r /data/user/tvaneede/GlobalFit/reco_processing/segments ${local_path}
cp /data/user/tvaneede/GlobalFit/reco_processing/rec_tau.py ${local_path}
cp /data/user/tvaneede/GlobalFit/reco_processing/rec_tau.sh ${local_path}
cp /data/user/tvaneede/GlobalFit/reco_processing/filter/filter_HESE.py ${local_path}
cp /data/user/tvaneede/GlobalFit/reco_processing/filter/filter_HESE.sh ${local_path}
cp /data/user/tvaneede/GlobalFit/reco_processing/evtgen/run_event_generator.py ${local_path}
cp /data/user/tvaneede/GlobalFit/reco_processing/evtgen/run_event_generator.sh ${local_path}

cp -r ${local_path} ${cvmfs_path}