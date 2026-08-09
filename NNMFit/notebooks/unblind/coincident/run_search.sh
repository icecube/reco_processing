#!/bin/bash
# Search for events in level2 data by MJD.
#
# Calls:
#   1. MJD 56221.342402 — test case (nearest event to 56211 found in EvtGen_merged.h5)
#   2. MJD 56211        — target day, full-day tolerance
#   3. MJD 56666        — target day, full-day tolerance

ICETRAY_SHELL=/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell
PYTHON=/cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python
SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/search_event_by_mjd.py"

# --- 1. Test: precise MJD, 1-second tolerance ---
echo "============================================================"
echo " Test: MJD 56221.342402 (Run 120844 / Event 6079235)"
echo "============================================================"
"$ICETRAY_SHELL" "$PYTHON" "$SCRIPT" \
    --mjd 56221.342402 \
    --tolerance 1 \
    --output "$(dirname "$SCRIPT")/event_MJD56221.342402.i3.zst" \
    2>&1 | tee "$(dirname "$SCRIPT")/search_MJD56221.log"

# # --- 2. MJD 56211: search the full day (tolerance = 86400 s) ---
# echo ""
# echo "============================================================"
# echo " Search: MJD 56211 (full-day tolerance)"
# echo "============================================================"
# "$ICETRAY_SHELL" "$PYTHON" "$SCRIPT" \
#     --mjd 56211 \
#     --tolerance 86400 \
#     --output "$(dirname "$SCRIPT")/event_MJD56211.i3.zst" \
#     2>&1 | tee "$(dirname "$SCRIPT")/search_MJD56211.log"

# # --- 3. MJD 56666: search the full day (tolerance = 86400 s) ---
# echo ""
# echo "============================================================"
# echo " Search: MJD 56666 (full-day tolerance)"
# echo "============================================================"
# "$ICETRAY_SHELL" "$PYTHON" "$SCRIPT" \
#     --mjd 56666 \
#     --tolerance 86400 \
#     --output "$(dirname "$SCRIPT")/event_MJD56666.i3.zst" \
#     2>&1 | tee "$(dirname "$SCRIPT")/search_MJD56666.log"
