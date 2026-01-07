
reco_version=burnsample_v0
out_path=/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/${reco_version}

outfiles=""

for (( i=2011; i<=2022; i++ )); do
    echo "$i"
    outfiles="${outfiles} /data/user/tvaneede/GlobalFit/reco_processing/hdf/output/${reco_version}/level3_cascade_Taupede_Data_v0_${i}.h5"
done

/data/user/tvaneede/software/py_venvs/py3-v4.4.1_reco-v1.1.0/bin/python merge.py -o ${out_path}/level3_cascade_Taupede_Data_v0.h5 ${outfiles}
