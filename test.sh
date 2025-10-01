
# /cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell \
#     /data/user/tvaneede/software/py_venvs/py3-v4.4.1_reco-v1.1.0/bin/python \
#     /data/user/tvaneede/GlobalFit/reco_processing/rec_tau.py \
#     -o /data/user/tvaneede/GlobalFit/reco_processing/output/test/test.i3.zst \
#     --imigrad --hypo tau --icemodel ftp-v1 --tilt --effd --effp --nframes 9 \
#     --qs $I3_DATA/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz \
#     /data/user/tvaneede/GlobalFit/reco_processing/filter/output/test/HESE_NuTau_NuGenCCNC.022634.000000.i3.zst


###
### running script 3 times in a row
###

# /cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell \
#     /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
#     /data/user/tvaneede/GlobalFit/reco_processing/rec_tau.py \
#     -o /data/user/tvaneede/GlobalFit/reco_processing/output/test/test.i3.zst \
#     --imigrad --icemodel ftp-v1 --tilt --effd --effp --nframes 9 \
#     --qs /data/user/tvaneede/GlobalFit/reco_processing/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz \
#     /data/user/tvaneede/GlobalFit/reco_processing/filter/output/test/HESE_NuTau_NuGenCCNC.022634.000000.i3.zst

# /cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell \
#     /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
#     /data/user/tvaneede/GlobalFit/reco_processing/rec_tau.py \
#     -o /data/user/tvaneede/GlobalFit/reco_processing/output/test/test_ibr.i3.zst \
#     --imigrad --icemodel ftp-v1 --tilt --effd --ibr --effp --nframes 9 \
#     --qs /data/user/tvaneede/GlobalFit/reco_processing/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz \
#     /data/user/tvaneede/GlobalFit/reco_processing/output/test/test.i3.zst

# /cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell \
#     /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
#     /data/user/tvaneede/GlobalFit/reco_processing/rec_tau.py \
#     -o /data/user/tvaneede/GlobalFit/reco_processing/output/test/test_ibr_idc.i3.zst \
#     --imigrad --icemodel ftp-v1 --tilt --effd --ibr --idc --effp --nframes 9 \
#     --qs /data/user/tvaneede/GlobalFit/reco_processing/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz \
#     /data/user/tvaneede/GlobalFit/reco_processing/output/test/test_ibr.i3.zst
