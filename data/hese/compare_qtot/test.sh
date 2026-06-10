# #!/bin/bash
# INPUT="/data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/i3files/NoDeepCore/HESE12/Bfr/IC86_2014/Run00125914_MJD57036_Taupede_out.i3.bz2"
# OUTPUT="/data/user/tvaneede/GlobalFit/reco_processing/data/hese/compare_qtot/Run00125914_MJD57036_selfveto.i3.bz2"

# /data/user/tvaneede/GlobalFit/reco_processing/data/hese/compare_qtot/compare_qtot.sh \
#     --Inputfile "$INPUT" \
#     --Outputfile "$OUTPUT"


# INPUT="/data/user/eyildizci/hese_tracks_processing/L5/new_IC86_2014/Run00125914_MJD57036.i3.bz2"
# OUTPUT="/data/user/tvaneede/GlobalFit/reco_processing/data/hese/compare_qtot/Run00125914_MJD57036_selfveto_emre.i3.bz2"
# GCD="/data/exp/IceCube/2015/filtered/level2pass2a/0114/Run00125914/Level2pass2_IC86.2014_data_Run00125914_0114_1_198_GCD.i3.zst"

# /data/user/tvaneede/GlobalFit/reco_processing/data/hese/compare_qtot/compare_qtot.sh \
#     --GCD "${GCD}" \
#     --Inputfile "$INPUT" \
#     --Outputfile "$OUTPUT"


# Level2 run directory — single event 75630389
INPUT="/data/exp/IceCube/2015/filtered/level2pass2a/0114/Run00125914/"
OUTPUT="/data/user/tvaneede/GlobalFit/reco_processing/data/hese/compare_qtot/Run00125914_level2_event75630389_selfveto.i3.bz2"
GCD="/data/exp/IceCube/2015/filtered/level2pass2a/0114/Run00125914/Level2pass2_IC86.2014_data_Run00125914_0114_1_198_GCD.i3.zst"

/data/user/tvaneede/GlobalFit/reco_processing/data/hese/compare_qtot/compare_qtot.sh \
    --GCD "${GCD}" \
    --Inputfile "$INPUT" \
    --Outputfile "$OUTPUT" \
    --EventID 75630389
