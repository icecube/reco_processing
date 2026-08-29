#!/bin/sh

source /data/user/tvaneede/software/py_venvs/py3-v4.4.2_reco-v1.2.3_icetray-v1.16.0/bin/activate
echo "venv: $VIRTUAL_ENV"

export HDF5_USE_FILE_LOCKING='FALSE'
echo "HDF5_USE_FILE_LOCKING=$HDF5_USE_FILE_LOCKING"

SCRIPT="/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/unblind/passing_fraction/plights_tianlu/nuveto_cluster_script.py"

echo "----- starting python -----"
echo "cos_theta=$1  output=$2  kind=$3  depth=$4  prpl_dir=$5"

python "$SCRIPT" -c "$1" -d "$4" -o "$2" -k "$3" --prpl-dir "$5"
