#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ICETRAY_SHELL=/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell
PYTHON=/cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python

INDIR="$SCRIPT_DIR/output/v2"
OUTDIR="$SCRIPT_DIR/output/v2_noGCD"

for season_dir in "$INDIR"/*/; do
    season="$(basename "$season_dir")"
    mkdir -p "$OUTDIR/$season"
    for infile in "$season_dir"*.i3.zst; do
        [ -e "$infile" ] || continue
        fname="$(basename "$infile")"
        outfile="$OUTDIR/$season/$fname"
        echo "Processing $season/$fname ..."
        "$ICETRAY_SHELL" "$PYTHON" "$SCRIPT_DIR/strip_gcd.py" "$infile" "$outfile"
    done
done

echo "Done."
