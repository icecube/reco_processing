
# GCD=/cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz
GCD=/cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_AVG_55697-57531_PASS2_SPE_withScaledNoise.i3.gz

DATASET=21315
SUBFOLDER=0000000-0000999
NFILE=000999

###
### L3
###

INFILE=/data/sim/IceCube/2016/filtered/level2/MuonGun/${DATASET}/${SUBFOLDER}/Level2_IC86.2016_MuonGun.0${DATASET}.${NFILE}.i3.zst

# l3 cascade
OUTPATH=/data/user/tvaneede/GlobalFit/reco_processing/muons/cascade/output/level3/cascade/${DATASET}/${SUBFOLDER}/
OUTFILE_L3CASC=${OUTPATH}/level3_cascade_IC86.2016_MuonGun.0${DATASET}.${NFILE}.i3.zst

mkdir -p ${OUTPATH}

/cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/RHEL_7_x86_64/metaprojects/icetray/v1.9.2/env-shell.sh \
    /cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/RHEL_7_x86_64/bin/python \
    /cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/metaprojects/icetray/v1.9.2/level3-filter-cascade/python/level3_Master.py \
    --input ${INFILE} --output ${OUTFILE_L3CASC} --gcd ${GCD} --MC


# l3 muon
OUTPATH=/data/user/tvaneede/GlobalFit/reco_processing/muons/cascade/output/level3/muon/${DATASET}/${SUBFOLDER}/
I3OUTFILE=${OUTPATH}/level3_muon_IC86.2016_MuonGun.0${DATASET}.${NFILE}.i3.zst
OUTFILE=${OUTPATH}/finallevel_NuMU_IC86.2016_MuonGun.0${DATASET}.${NFILE}.i3.zst

mkdir -p ${OUTPATH}

/cvmfs/icecube.opensciencegrid.org/users/eganster/combo.releases.V01-00-02.py3-v4.0.1.RHEL_7_x86_64/env-shell.sh \
    /cvmfs/icecube.opensciencegrid.org/py3-v4.0.1/RHEL_7_x86_64/bin/python \
    /cvmfs/icecube.opensciencegrid.org/users/eganster/combo.releases.V01-00-02.py3-v4.0.1.RHEL_7_x86_64/lib/icecube/finallevel_filter_diffusenumu/process_L345.py \
    --input ${INFILE} --i3output ${I3OUTFILE} --output ${OUTFILE} --gcd ${GCD} --is_mc True --do_postL5 True

###
### L4
###
OUTPATH=/data/user/tvaneede/GlobalFit/reco_processing/muons/cascade/output/level4/${DATASET}/${SUBFOLDER}/
OUTFILE=${OUTPATH}/level4_cascade_IC86.2016_MuonGun.0${DATASET}.${NFILE}.i3.zst

mkdir -p ${OUTPATH}

/cvmfs/icecube.opensciencegrid.org/users/chill/metaproject_l4_legacy/build/env-shell.sh \
    /cvmfs/icecube.opensciencegrid.org/py3-v4.0.1/RHEL_7_x86_64/bin/python \
    /cvmfs/icecube.opensciencegrid.org/users/chill/metaproject_l4_legacy/src/level4-processing-cascade/python/cascade_level4_master.py \
    -i ${OUTFILE_L3CASC} -o ${OUTFILE} -g ${GCD} -p legacy
