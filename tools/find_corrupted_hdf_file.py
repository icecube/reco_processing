import glob
import os, sys
import simweights

infiles = glob.glob( "/data/sim/IceCube/2020/filtered/level6/cascade/neutrino-generator/cascade/22857/0013000-0013999/*.i3.*" )

for infile in infiles:
    cmd = f"/data/user/tvaneede/GlobalFit/reco_processing/hdf/to_hdf5.sh -i {infile} -o /data/user/tvaneede/GlobalFit/reco_processing/hdf/output/test/test.h5 -f NuE"
    