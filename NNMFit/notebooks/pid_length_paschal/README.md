# PID & length study — Paschal Coyle

## Motivation

This study was prompted by a question from Paschal Coyle: from which tau decay lengths can IceCube reconstruct double cascades? The goal is to understand the sensitivity of the reconstructed track length as a function of true tau decay length (`TrueLength`), with NuE as a reference for the "no second cascade" baseline.

A future comparison with KM3NeT is planned, but KM3NeT simulation files are not yet available.

## Notebook

**`hese_histograms.ipynb`** — opens the HESE SnowStorm dataset and produces weighted histograms using an astrophysical flux model (per-flavour norm 2.12 × 10⁻¹⁸, γ = 2.87). Events are weighted by `fluxless_weight × AstroFluxModel(MCPrimaryEnergy)`.

Plots:
1. Reconstructed energy split by neutrino flavour (νe / νμ / ντ)
2. Reconstructed length split by neutrino flavour
3. True MC primary energy split by neutrino flavour
4. Normalised reconstructed length: all νe vs ντ in 5 m TrueLength slices (0–5, 5–10, …, 45–50, >50 m)

## Dataset

```
datasets/flavor_globalfit/hese/combined/
  IC86_pass2_SnowStorm_v2_FTP_Baseline_Combined_v7-v1_fluxlessweight/
  dataset_IC86_pass2_SnowStorm_v2_FTP_Baseline_Combined_v7-v1_fluxlessweight.parquet
```
