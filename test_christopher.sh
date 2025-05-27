#!/bin/bash

# rec -o /data/user/tvaneede/GlobalFit/reco_processing/output/test/Reco_NuTau_NuGenCCNC.022635.000001.i3.zst \
#     --imigrad \         # iminuit migrad minimizer
#     --hypo tau \        # hypothesis: tau
#     --icemodel ftp-v1 \ # ftp-v1 icemodel + tilt effd effp = ftp-v3
#     --tilt \            # tilt in ice
#     --effd \            # effective distance table
#     --effp \            # effective distance table
#     --qs $I3_DATA/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz \
#     --idc \             # include deepcore DOMs
#     --ibr \             # include bright DOMs
#     --nframes 60 \      # just do x frames for testing
#     /data/user/tvaneede/GlobalFit/reco_processing/output/v7.0/22635/0000000-0000999/Reco_NuTau_NuGenCCNC.022635.000001.i3.zst_out.i3.bz2

rec -o /data/user/tvaneede/GlobalFit/reco_processing/output/test/Reco_NuTau_NuGenCCNC.022635.000001.i3.zst --imigrad --hypo tau --icemodel ftp-v1 --tilt --effd --effp --idc --ibr --qs $I3_DATA/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz /data/user/tvaneede/GlobalFit/reco_processing/output/v7.0/22635/0000000-0000999/Reco_NuTau_NuGenCCNC.022635.000001.i3.zst_out.i3.bz2 --nframes 60
