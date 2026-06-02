#!/bin/bash
set -e

OUTPATH=/data/user/tvaneede/GlobalFit/reco_processing/data/hese/output/v1/IC86_2022
OUTPATH_TAUPEDE=/data/user/tvaneede/GlobalFit/reco_processing/data/hese/output/v1/IC86_2022/Taupede
OUTPATH_EVTGEN=/data/user/tvaneede/GlobalFit/reco_processing/data/hese/output/v1/IC86_2022/EvtGen

mkdir -p ${OUTPATH}
mkdir -p ${OUTPATH_TAUPEDE}
mkdir -p ${OUTPATH_EVTGEN}

echo "-----------------------------"
echo "Running"
echo "INPATH" ${INPATH}
echo "OUTPATH" ${OUTPATH}
echo "-----------------------------"

###
### Regular
###

OUTFILE=${OUTPATH_TAUPEDE}/Taupede.i3.zst

echo "-----------------------------"
echo "Regular"
echo "INPATH" ${INPATH}
echo "OUTFILE" ${OUTFILE}

/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/icetray-env icetray/v1.14.0 \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
    /data/user/tvaneede/GlobalFit/reco_processing/iceprod/scripts/v1/rec_tau_data_hese.py \
    -o ${OUTFILE} \
    --imigrad --icemodel ftp-v1 --tilt --effd --effp --qs --isdata \
    \
    /data/exp/IceCube/2022/filtered/level2/0808/Run00136918/Level2_IC86.2022_data_Run00136918_0808_83_689_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00136918_MJD59799_0.i3.zst \
    \
    /data/exp/IceCube/2022/filtered/level2/1229/Run00137489/Level2_IC86.2022_data_Run00137489_1229_84_717_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00137489_MJD59942_0.i3.zst \
    \
    /data/exp/IceCube/2023/filtered/level2/0417/Run00137845/Level2_IC86.2022_data_Run00137845_0417_84_735_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00137845_MJD60051_0.i3.zst \
    \
    /data/exp/IceCube/2023/filtered/level2/0622/Run00138069/Level2_IC86.2022_data_Run00138069_0622_84_746_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00138069_MJD60117_0.i3.zst \
    \
    /data/exp/IceCube/2022/filtered/level2/0826/Run00136985/Level2_IC86.2022_data_Run00136985_0826_83_692_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00136985_MJD59817_0.i3.zst \
    \
    /data/exp/IceCube/2023/filtered/level2/0106/Run00137512/Level2_IC86.2022_data_Run00137512_0106_84_717_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00137512_MJD59950_0.i3.zst \
    \
    /data/exp/IceCube/2023/filtered/level2/0430/Run00137891/Level2_IC86.2022_data_Run00137891_0430_84_736_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00137891_MJD60064_0.i3.zst \
    \
    /data/exp/IceCube/2023/filtered/level2/0707/Run00138125/Level2_IC86.2022_data_Run00138125_0707_84_748_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00138125_MJD60132_0.i3.zst \
    \
    /data/exp/IceCube/2022/filtered/level2/0902/Run00137007/Level2_IC86.2022_data_Run00137007_0902_83_694_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00137007_MJD59825_0.i3.zst \
    \
    /data/exp/IceCube/2023/filtered/level2/0109/Run00137527/Level2_IC86.2022_data_Run00137527_0109_84_717_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00137527_MJD59953_0.i3.zst \
    \
    /data/exp/IceCube/2023/filtered/level2/0511/Run00137930/Level2_IC86.2022_data_Run00137930_0511_84_738_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00137930_MJD60075_0.i3.zst \
    \
    /data/exp/IceCube/2023/filtered/level2/0709/Run00138134/Level2_IC86.2022_data_Run00138134_0709_84_748_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00138134_MJD60134_0.i3.zst \
    \
    /data/exp/IceCube/2022/filtered/level2/1016/Run00137160/Level2_IC86.2022_data_Run00137160_1016_83_702_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00137160_MJD59868_0.i3.zst \
    \
    /data/exp/IceCube/2023/filtered/level2/0217/Run00137661/Level2_IC86.2022_data_Run00137661_0217_84_723_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00137661_MJD59992_0.i3.zst \
    \
    /data/exp/IceCube/2023/filtered/level2/0610/Run00138035/Level2_IC86.2022_data_Run00138035_0610_84_744_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00138035_MJD60105_0.i3.zst \
    \
    /data/exp/IceCube/2023/filtered/level2/1127/Run00138611/Level2_IC86.2022_data_Run00138611_1127_84_775_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00138611_MJD60275_0.i3.zst \
    \
    /data/exp/IceCube/2022/filtered/level2/1018/Run00137167/Level2_IC86.2022_data_Run00137167_1018_83_703_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00137167_MJD59870_0.i3.zst \
    \
    /data/exp/IceCube/2023/filtered/level2/0329/Run00137786/Level2_IC86.2022_data_Run00137786_0329_84_730_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00137786_MJD60032_0.i3.zst \
    \
    /data/exp/IceCube/2023/filtered/level2/0620/Run00138065/Level2_IC86.2022_data_Run00138065_0620_84_746_GCD.i3.zst \
    /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022/Run00138065_MJD60116_0.i3.zst

##
## EvtGen
##

OUTFILE_EVTGEN=${OUTPATH_EVTGEN}/${OUTPATH}/EvtGen.i3.zst

echo "-----------------------------"
echo "EvtGen"
echo "OUTFILE" ${OUTFILE_EVTGEN}
echo "INFILE" ${OUTFILE}

/cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/icetray-env icetray/v1.12.0 \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/tensorflow_gpu_py3-v4.3.0/bin/python \
    /cvmfs/icecube.opensciencegrid.org/users/tvaneede/reco_processing/v0/run_event_generator.py \
    --Inputfile ${OUTFILE} \
    --Outputfile ${OUTFILE_EVTGEN}
