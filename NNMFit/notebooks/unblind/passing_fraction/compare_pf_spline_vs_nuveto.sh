#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/setenv.sh"

PY="$SCRIPT_DIR/compare_pf_spline_vs_nuveto.py"

python "$PY" --flux-type conv --flavor nu_mu --test

# for flux_type in conv pr; do
#     for flavor in nu_mu nu_mubar nu_e nu_ebar; do
#         echo "=== ${flux_type} ${flavor} ==="
#         python "$PY" --flux-type "$flux_type" --flavor "$flavor"
#     done
# done
