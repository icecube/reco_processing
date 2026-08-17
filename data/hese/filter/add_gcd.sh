#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ICETRAY_SHELL=/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell
PYTHON=/cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python

INDIR="$SCRIPT_DIR/output/v2_noGCD"
OUTDIR="$SCRIPT_DIR/output/v2_pass2GCD"
GCD_BASE="/data/ana/IceCube"

for season_dir in "$INDIR"/*/; do
    season="$(basename "$season_dir")"
    year="${season: -4}"
    mkdir -p "$OUTDIR/$season"

    for infile in "$season_dir"*.i3.zst; do
        [ -e "$infile" ] || continue
        fname="$(basename "$infile")"
        run_num="${fname#Run}"
        run_num="${run_num%.i3.zst}"

        gcdfile=""
        for try_year in "$year" "$((year+1))" "$((year-1))"; do
            gcdfile=$(ls "$GCD_BASE/$try_year/filtered/level2pass2b/GCD/"*"Run${run_num}"*GCD*.i3* 2>/dev/null | sort | head -1)
            [ -n "$gcdfile" ] && break
        done
        if [ -z "$gcdfile" ]; then
            echo "ERROR: no GCD found for $season/$fname" >&2
            exit 1
        fi

        outfile="$OUTDIR/$season/$fname"
        echo "Processing $season/$fname ..."
        "$ICETRAY_SHELL" "$PYTHON" "$SCRIPT_DIR/add_gcd.py" "$infile" "$gcdfile" "$outfile"
    done
done

echo "Done."
