

/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell

source /data/user/tvaneede/software/py_venvs/py3-v4.4.1_reco-v1.1.0/bin/activate # my installation of reco

/data/user/tvaneede/GlobalFit/reco_processing/rec_HESE.py -o /data/user/tvaneede/GlobalFit/reco_processing/output/test/test.i3.zst --imigrad --hypo tau --icemodel ftp-v1 --tilt --effd --effp --HESE --qs $I3_DATA/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz /data/user/tvaneede/GlobalFit/reco_processing/notebooks/gulliver_nan/Level2_NuTau_NuGenCCNC.022634.000001.event_id_3327.i3.zst
# rec -o /data/user/tvaneede/GlobalFit/reco_processing/output/test/test.i3.zst --log debug --imigrad --hypo tau --icemodel ftp-v1 --tilt --effd --effp --qs $I3_DATA/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz /data/user/tvaneede/GlobalFit/reco_processing/notebooks/gulliver_nan/Level2_NuTau_NuGenCCNC.022634.000001.event_id_3327.i3.zst
