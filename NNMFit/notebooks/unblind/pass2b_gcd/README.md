# Pass2b GCD reprocessing

Recompute `CausalQTot` and `VHESelfVeto` for all HESE v3 events using the official
**pass2b** GCDs from `/data/ana/IceCube/`, replacing the GCDs that were embedded in
the v3 files during the original processing.

## Motivation

The v3 output files carry the GCD that was active at processing time, which does not
correspond to the pass2b reprocessing standard. Applying the pass2b GCD can affect
both the charge calculation (via updated calibration) and the self-veto decision
(via updated geometry/bad-DOM lists).

## Scripts

| File | Purpose |
|---|---|
| `recompute_pass2b.py` | Core icetray script. Reads a v3 file, swaps in the matching per-run pass2b GCD, and writes `CausalQTot_pass2b`, `VHESelfVeto_pass2b`, and `VHESelfVetoVertexTime_pass2b` to the output file. |
| `recompute_pass2b.sh` | Shell wrapper (icetray-shell + venv). |
| `run_all.sh` | Run everything sequentially in the terminal. Skips already-existing output files. |
| `create_hdf.sh` | Convert per-season output i3 files to HDF5. |
| `merge_hdf.sh` | Merge per-season HDF5 files into `merged/EvtGen_merged.h5`. |
| `inspect_pass2b.ipynb` | Notebook comparing original and pass2b quantities. |

## Input / output

- **Input:** `/data/user/tvaneede/GlobalFit/reco_processing/data/hese/output/v3/<season>/<reco>/`
- **Output:** `<season>/<reco>/` (same structure, mirrored here)
- **Merged HDF5:** `merged/EvtGen_merged.h5` (188 events, EvtGen only)

## Conclusions

- **The pass2b GCD has no effect on `CausalQTot` or `VHESelfVeto`.** Confirmed by `compare_v2_v3.py`: running the filter with the original GCD (v2) versus the pass2b GCD (v3) gives identical values for every event across IC79_2010 – IC86_2015.

- The differences seen in `inspect_pass2b.ipynb` between `HESE_CausalQTot` / `HESE_VHESelfVeto` and their `_pass2b` counterparts were a misleading comparison: the `HESE_*` quantities are computed by the official IceCube processing using a different pulse series, not with the same algorithm applied to a different GCD. The differences reflect the pulse series choice, not the GCD.

- **The pass2b GCD reprocessing does not change the HESE event selection.**
