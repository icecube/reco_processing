import tables

path = "/data/user/tvaneede/GlobalFit/reco_processing/data/hese/output/v1/IC79_2010/EvtGen/EvtGen.h5"
path = "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_ensemble_ani_v1/merged/HESE_evtgen_NuTau.h5"

with tables.open_file(path, mode="r") as f:
    for node in f.walk_nodes("/", classname="Table"):
        print(f"\n{node._v_pathname}")
        print("  " + ", ".join(node.colnames))
