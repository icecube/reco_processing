# source /data/user/tvaneede/GlobalFit/reco_processing/setenv.sh

# rec -o /data/user/tvaneede/GlobalFit/reco_processing/output/test/Reco_NuTau_NuGenCCNC.022635.000001.i3.zst --imigrad --hypo tau --icemodel ftp-v1 --tilt --effd --effp --qs $I3_DATA/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz /data/user/tvaneede/GlobalFit/reco_processing/filtering/output/test/Level3_NuTau_NuGenCCNC.022635.000001.i3.zst --nframes 20

# problematic event
/data/user/tvaneede/GlobalFit/reco_processing/rec_HESE.py -o /data/user/tvaneede/GlobalFit/reco_processing/output/test/test.i3.zst --imigrad --hypo tau --icemodel ftp-v1 --tilt --effd --effp --HESE --nframes 150 --qs $I3_DATA/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz /data/sim/IceCube/2023/filtered/level2/neutrino-generator/22634/0000000-0000999/Level2_NuTau_NuGenCCNC.022634.000000.i3.zst
# rec -o /data/user/tvaneede/GlobalFit/reco_processing/output/test/test_2.i3.zst --imigrad --hypo tau --icemodel ftp-v1 --tilt --effd --effp --qs $I3_DATA/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz /data/sim/IceCube/2023/filtered/level2/neutrino-generator/22634/0000000-0000999/Level2_NuTau_NuGenCCNC.022634.000001.i3.zst
