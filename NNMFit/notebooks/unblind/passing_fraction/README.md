# Passing Fraction Comparison

Comparison of atmospheric neutrino passing fractions between the spline-based
evaluator used in GlobalFit and a direct nuVeto call, for both conventional
(`conv`) and prompt (`pr`) neutrinos and all four flavors
(νμ, ν̄μ, νe, ν̄e).

---

## Purpose

The GlobalFit analysis uses pre-computed photospline splines to evaluate
atmospheric passing fractions at analysis time. This directory checks whether
those splines reproduce what nuVeto would compute directly, and documents the
known differences in the underlying nuVeto configuration.

---

## Files

| File | Role |
|---|---|
| `compare_pf_spline_vs_nuveto.py` | Main comparison script |
| `compare_pf_spline_vs_nuveto.sh` | Local convenience runner (test mode) |
| `submit_compare_pf.sh` | Cluster executable wrapper (sourced by HTCondor) |
| `create_dag.py` | Generates the HTCondor DAG for all 8 combinations |
| `compare_pf_dag.sub` | DAG-compatible HTCondor submit file |
| `setenv.sh` | Activates the Python venv |
| `test_spline_evaluate_vs_evaluate_all.py` | Unit test: `evaluate` vs `evaluate_all` |

---

## How to run

### Locally (single combination, test mode)

```bash
bash compare_pf_spline_vs_nuveto.sh
```

This runs `--flux-type conv --flavor nu_mu --test` (2 energy steps, 2 zenith
steps) via `setenv.sh`.

### Full run, single combination

```bash
source setenv.sh
python compare_pf_spline_vs_nuveto.py --flux-type conv --flavor nu_mu
```

Arguments:

| Flag | Values | Description |
|---|---|---|
| `--flux-type` | `conv`, `pr` | Conventional or prompt flux |
| `--flavor` | `nu_mu`, `nu_mubar`, `nu_e`, `nu_ebar` | Neutrino flavor |
| `--test` | — | Reduced grid (2×2) for quick checks |

### All 8 combinations on the cluster (DAG)

```bash
python create_dag.py          # generates DAG in /scratch/tvaneede/passing_fraction/compare_pf_dag/
cd /scratch/tvaneede/passing_fraction/compare_pf_dag
condor_submit_dag submit.dag
```

Set `submit_jobs = True` in `create_dag.py` to submit automatically.
HTCondor logs go to `/scratch/tvaneede/passing_fraction/compare_pf_dag/logs/`.
Plots are always written to `plots/{flux_type}_{flavor}/` relative to the
script's own directory (anchored via `os.path.abspath(__file__)`), regardless
of the working directory on the execute node.

---

## What the script does

Three scans are performed for each flux-type/flavor combination:

| Scan | Fixed values | Grid |
|---|---|---|
| Energy × cos θ | depth = 1950 m | 50 log-spaced energies [100, 10⁷] GeV; cos θ 0.05–1.0 in steps of 0.05 |
| cos θ (at fixed E) | depth = 1950 m, E = 10⁵ GeV | cos θ 0.05–1.0 in steps of 0.05 |
| Depth | cos θ = 0.5 (zenith ≈ 60°), E = 10⁵ GeV | 17 depths 1400–3000 m |

For every grid point both methods are evaluated:

- **Spline**: `Spline_Evaluator.evaluate(kind, pid, depth, zenith, energy)` →
  returns `log10(PF)`, converted to linear PF.
- **nuVeto**: `nuVeto.passing(E, cos_theta, kind=..., pmodel=..., hadr=..., depth=..., density=...)` →
  returns PF directly.

Six plots are produced:

1. PF vs energy at several fixed cos θ values (spline + nuVeto)
2. PF vs cos θ at several fixed energies
3. Ratio (spline / nuVeto) vs energy
4. Ratio vs cos θ
5. PF vs depth (at fixed E and cos θ)
6. Ratio vs depth

Raw values are also written to `plots/{flux_type}_{flavor}/table.txt`.

---

## Spline provenance

The splines used in GlobalFit are located at:

```
/data/user/nlad/PassingFractions/splines/HESE_depth_dependent_grid_11_dep_21/
```

They were produced in two steps by N. Lad (Aug 2023):

### Step 1 — Grid calculation

`/data/user/nlad/PassingFractions/notebooks/DAGMan_grid_calculation_HESE.ipynb`
submitted a DAGMan job array:

```
nuveto/submit_nuveto.sub
  → nuveto/nuveto_cluster_script.sh
    → nuveto/nuveto_cluster_script.py
```

The raw per-(depth, cos θ) pickle files were written to:

```
/data/user/nlad/PassingFractions/HESE_grid_11_dep_21_the_51_ene/
```

### Step 2 — Spline fitting

`v0_2021_passing_fraction_grid_fitter.py` read the raw grid pickles and fitted
tensor B-splines (via `photospline`), writing the result to the splines
directory above.

### nuVeto parameters used to generate the splines

The parameters are stored in every raw grid pickle and were confirmed by
inspection:

| Parameter | Value used for splines |
|---|---|
| `pmodel` | `(HillasGaisser2012, 'H3a')` |
| `hadr` | **`SIBYLL2.3c`** |
| `density` | `('CORSIKA', ('SouthPole', 'December'))` |
| `prpl` | HESE depth-dependent (see below) |

### Spline grid coverage

| Dimension | Min | Max | Points |
|---|---|---|---|
| depth | 1400 m | 3000 m | 11 |
| cos θ | 0.05 | 1.0 | 21 |
| log₁₀(E / GeV) | 1 (10 GeV) | ~6.88 (~7.6×10⁶ GeV) | 51 |

The `Spline_Evaluator` fixes the muon detection threshold at `E_thresh = 1000 GeV`
(`hese_depth_dependent` prpl key) and returns `log10(passing_fraction)`.
Events outside the grid receive default values:

- Below minimum energy or cos θ: `log10(PF) = 0` (PF → 1)
- Above maximum energy: `log10(PF) = −8` (PF → 10⁻⁸)

---

## Known differences between splines and comparison script

These differences mean the comparison is **not** a like-for-like reproduction
of the spline generation. The plots show the combined effect of all of them.

### 1. Detector response (`prpl`) — largest effect

The splines were generated using HESE depth-dependent muon detection
probabilities: `ice_allm97_hese_depth_NNN.pkl` files that encode a realistic
IceCube muon veto response as a function of depth.

The comparison nuVeto calls use the default `prpl = "ice_allm97_step_1"`, a
step-function detector response (muon detected with probability 1 if it
exceeds threshold, 0 otherwise). This is physically different and will produce
systematically different passing fractions, especially at intermediate energies.

The HESE depth-dependent prpl files are custom to N. Lad's setup and were
found in `/home/rnaab/software/virtualenvs/nuveto/`. They are not part of the
standard nuVeto package and are not available in the current analysis venv.

### 2. Hadronic interaction model

| | Value |
|---|---|
| Splines | `SIBYLL2.3c` |
| Comparison script | `SIBYLL2.3E` |

`SIBYLL2.3c` is not available in the current venv
(`py3-v4.4.2_reco-v1.2.3_icetray-v1.16.0`). The closest available model is
`SIBYLL2.3E`.

### 3. Depth handling

The spline generation used integer depths (nearest-neighbour lookup in a
39-entry dict keyed to `z = 1948.0 - depth`). The comparison script passes
float depths directly to nuVeto, which interpolates internally.

### 4. Energy range

The script scans up to log₁₀(E) = 7 (10⁷ GeV), slightly beyond the spline
maximum (~6.88). Above the spline max the evaluator clips to `log10(PF) = −8`.
This causes the ratio to collapse toward zero at the high-energy end of the
scan.
