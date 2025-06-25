source /data/user/tvaneede/GlobalFit/reco_processing/setenv.sh

python filter_hese.py --Inputfile /data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator/22635/0000000-0000999/Level3_NuTau_NuGenCCNC.022635.000001.i3.zst --Outputfile /data/user/tvaneede/GlobalFit/reco_processing/filtering/output/test/Level3_NuTau_NuGenCCNC.022635.000001.i3.zst

# dataset=22635 # 22634 22635
# subdataset=0000000-0000999

# outpath=/data/user/tvaneede/GlobalFit/reco_processing/filtering/output/${dataset}/${subdataset}

# mkdir -p ${outpath}

# for i in {1..100}; do
#     run_number=$(printf "%06d" "$i")
#     inputfile=/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator/${dataset}/${subdataset}/Level3_NuTau_NuGenCCNC.0${dataset}.${run_number}.i3.zst
#     outputfile=${outpath}/Level3_NuTau_NuGenCCNC.0${dataset}.${run_number}.i3.zst

#     echo "----------------------------"
#     echo "Current number is: $run_number"

#     python filter_hese.py --Inputfile ${inputfile} --Outputfile ${outputfile}
# done
