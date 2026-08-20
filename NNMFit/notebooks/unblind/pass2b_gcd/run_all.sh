#!/bin/bash
# Process all HESE v3 files sequentially, adding CausalQTot_pass2b and
# VHESelfVeto_pass2b using per-run pass2b GCDs.

set -e

V3_BASE="/data/user/tvaneede/GlobalFit/reco_processing/data/hese/output/v3"
OUTPUT_BASE="/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/unblind/pass2b_gcd"
SCRIPT="${OUTPUT_BASE}/recompute_pass2b.sh"

SEASONS=(IC79_2010 IC86_2011 IC86_2012 IC86_2013 IC86_2014 IC86_2015
         IC86_2016 IC86_2017 IC86_2018 IC86_2019 IC86_2020 IC86_2021 IC86_2022)

total=0
done_count=0

for season in "${SEASONS[@]}"; do
    for reco_type in Taupede EvtGen; do
        reco_dir="${V3_BASE}/${season}/${reco_type}"
        [ -d "${reco_dir}" ] || continue

        out_dir="${OUTPUT_BASE}/${season}/${reco_type}"
        mkdir -p "${out_dir}"

        for input_file in "${reco_dir}"/Run*.i3*; do
            [ -f "${input_file}" ] || continue
            total=$((total + 1))
        done
    done
done

echo "Processing ${total} files..."
echo ""

for season in "${SEASONS[@]}"; do
    for reco_type in Taupede EvtGen; do
        reco_dir="${V3_BASE}/${season}/${reco_type}"
        [ -d "${reco_dir}" ] || continue

        out_dir="${OUTPUT_BASE}/${season}/${reco_type}"
        mkdir -p "${out_dir}"

        for input_file in "${reco_dir}"/Run*.i3*; do
            [ -f "${input_file}" ] || continue

            basename=$(basename "${input_file}")
            output_file="${out_dir}/${basename}"
            done_count=$((done_count + 1))

            if [ -f "${output_file}" ]; then
                echo "[${done_count}/${total}] SKIP (exists): ${season}/${reco_type}/${basename}"
                continue
            fi

            echo "[${done_count}/${total}] ${season}/${reco_type}/${basename}"
            "${SCRIPT}" \
                --InputFile  "${input_file}" \
                --Season     "${season}" \
                --OutputDir  "${out_dir}"
        done
    done
done

echo ""
echo "All done."
