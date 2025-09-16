
# using local scripts
# /cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell \
#     /data/user/tvaneede/software/py_venvs/py3-v4.4.1_reco-v1.1.0/bin/python \
#     /data/user/tvaneede/GlobalFit/reco_processing/filter/filter_HESE.py \
#     --Inputfile /data/sim/IceCube/2023/filtered/level2/neutrino-generator/22634/0000000-0000999/Level2_NuTau_NuGenCCNC.022634.000000.i3.zst \
#     --Outputfile /data/user/tvaneede/GlobalFit/reco_processing/filter/output/test/HESE_NuTau_NuGenCCNC.022634.000000.i3.zst \

###
### trying to get cvmfs to work
###

# # using same installation as cvmfs
# /cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell \
#     /mnt/ceph1-npx/user/tvaneede/software/py_venvs/test_iceprod_reco/py3-v4.4.1_reco-v1.1.0/bin/python \
#     /data/user/tvaneede/GlobalFit/reco_processing/filter/filter_HESE.py \
#     --Inputfile /data/sim/IceCube/2023/filtered/level2/neutrino-generator/22634/0000000-0000999/Level2_NuTau_NuGenCCNC.022634.000000.i3.zst \
#     --Outputfile /data/user/tvaneede/GlobalFit/reco_processing/filter/output/test/HESE_NuTau_NuGenCCNC.022634.000000.i3.zst \

# using cvmfs
/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/reco_processing/v0/filter_HESE.py \
    --Inputfile /data/sim/IceCube/2023/filtered/level2/neutrino-generator/22634/0000000-0000999/Level2_NuTau_NuGenCCNC.022634.000000.i3.zst \
    --Outputfile /data/user/tvaneede/GlobalFit/reco_processing/filter/output/test/HESE_NuTau_NuGenCCNC.022634.000000.i3.zst \
