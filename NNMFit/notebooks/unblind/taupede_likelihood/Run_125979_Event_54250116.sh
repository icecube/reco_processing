#!/bin/bash
# Compare taupede hypotheses across two processing chains.
#
# Run 1 (baseline):  HESE particles + HESE pulses              → delta should be 0
# Run 2 (cross):     Finallevel particles + HESE pulses
#
# Output is written to Run_125979_Event_54250116.txt in the same directory.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ICETRAY_ENV=/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/icetray-env
PYTHON=/cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python
EVAL="${SCRIPT_DIR}/eval_likelihood.py"

HESE_FILE=/data/user/tvaneede/GlobalFit/reco_processing/data/hese/output/v3/IC86_2014/EvtGen/Run00125979.i3.zst
FINAL_FILE=/data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/i3files/NoDeepCore/HESE12/Bfr/IC86_2014/Run00125979_MJD57053_Taupede_out.i3.bz2
GCD_FILE=/data/exp/IceCube/2015/filtered/level2pass2a/0130/Run00125979/Level2pass2_IC86.2014_data_Run00125979_0130_1_143_GCD.i3.zst

OUTFILE="${SCRIPT_DIR}/Run_125979_Event_54250116.txt"

{
    echo "=========================================================="
    echo "Run 1: HESE particles + HESE pulses (baseline, delta = 0)"
    echo "=========================================================="
    $ICETRAY_ENV icetray/v1.14.0 "$PYTHON" "$EVAL" \
        "$HESE_FILE" \
        --particles-key TaupedeFit_iMIGRAD_PPB0Particles \
        --compare-key   TaupedeFit_iMIGRAD_PPB0FitParams \
        2>&1

    echo ""
    echo "=========================================================="
    echo "Run 2: Finallevel particles + HESE pulses"
    echo "=========================================================="
    $ICETRAY_ENV icetray/v1.14.0 "$PYTHON" "$EVAL" \
        "$HESE_FILE" \
        --hypo-file     "$FINAL_FILE" \
        --particles-key HESETaupedeFitParticles \
        --compare-key   TaupedeFit_iMIGRAD_PPB0FitParams \
        2>&1

} | tee "$OUTFILE"

echo ""
echo "Output written to ${OUTFILE}"
