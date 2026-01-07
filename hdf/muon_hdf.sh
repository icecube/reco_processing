
reco_version=hese_iceprod_v6
out_path=/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/hdf/output/${reco_version}/merged

outfiles=""

for run in 21315 21316 21317; do
# for run in 21317; do
    file_path=/data/user/tvaneede/GlobalFit/reco_processing/muons/hese/output/${run}/EvtGen/
    outfiles="${outfiles} ${out_path}/HESE_MuonGun_MuonGun_${run}.h5"
    ./to_hdf5.sh -i ${file_path} -o ${out_path}/HESE_MuonGun_MuonGun_${run}.h5 -f MuonGun
done

/data/user/tvaneede/software/py_venvs/py3-v4.4.1_reco-v1.1.0/bin/python merge.py -o ${out_path}/HESE_MuonGun_MuonGun.h5 ${outfiles}
