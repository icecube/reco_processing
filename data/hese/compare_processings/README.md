# Comparing v1 vs test reconstruction

## Context

**v1** (`output/v1/`) is based on pre-existing reconstructed files at:

```
/data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/HESE
```

Those files were produced by earlier processing campaigns and are taken as-is — the reconstruction steps were not rerun. They represent a fixed reference for the Taupede reconstruction.

**test** (`output/test/`) is a fresh reconstruction starting from the raw Level-2 data, applying the same filtering and reconstruction chain from scratch.

## What we found

The input pulses (`SplitInIcePulses`, `SplitInIcePulsesIC`, `SplitInIcePulsesICPulseCleaned`, `SRTSplitInIcePulses`, `SRTSplitInIcePulses_IC_Singles_PPB0`) and all GCD frame objects are byte-for-byte identical between v1 and test.

The reconstruction results differ slightly:

- `LineFit` and `CascadeLlhVertexFit_L3` are identical.
- `SPEFit2` shows floating-point level differences (~1e-6 rad in direction), likely due to a newer version of icetray and/or different compiler/threading settings.
- `CascadeLlhVertexFit_L2` converges to a different local minimum (Δzen ~ 0.5 rad, ΔE ~ 54k GeV). This propagates into `CascadeLast_L2`, `MonopodFit_iMIGRAD_PPB0`, and `TaupedeFit_iMIGRAD_PPB0`.

The differences are caused by a newer version of icetray combined with different reconstruction settings, which can cause likelihood minimisers to follow different paths to (local) minima even from the same starting pulses.

## Conclusion

The test reconstruction is trusted as the final result.

## Scripts

- `compare_event.py` — compares a single event (RunID=122649, EventID=63903532) between the two files: GCD frames, pulse series, and selected I3Particle keys.
- `run_compare.sh` — wrapper that launches `compare_event.py` inside the correct icetray environment and saves output to `compare_event.log`.
