# step2_hese_flavor_reunblind / studies

Side studies for the step2 (flavor) reunblinding fit.

## compare_SAY_Poisson.ipynb
Compares the nominal 1D scan with the SAY likelihood (`nbestfit50_all_param_2sigma_1D_10steps_PassingHESE`) to the same scan with the Poisson likelihood (`..._PassingHESE_Poisson`). It shows the best fits and 1σ errors of all parameters side by side, overlays the profile likelihoods and plots an overview of the shifts (`plots_compare_SAY_Poisson/`).
Poisson gives the same astro_norm (3.59 vs 3.62), a slightly softer spectrum (γ 2.85 vs 2.93, ~0.5σ) and a lower νe ratio (0.72 vs 0.90, ~0.6σ), with the largest nuisance shifts in the muon parameters; everything stays within 1σ.

## asimov_closure.ipynb
Makes flavor triangles from the Asimov flavor scans in `dag_scans/.../asimov_closure` (SAY and Poisson with/without systematics and with different muon templates, plus SAY variants with another minimizer and the old simulation), injected at the HESE best fit with a 1:1:1 flavor composition. It marks the injected and best-fit compositions in the triangles, overlays groups of scans, and prints, for every parameter, the injected value against the best fit (`plots_asimov_closure/`).
Poisson closes exactly everywhere, while the SAY bias depends on the muon template: astro_norm +0.30 / muon norm −0.30 with the combined template, +0.04 / −0.13 with the paper KDE, and closure within +0.001 / −0.02 with the non-paper KDE (`muonconvneha`), independent of the minimizer (LBFGSB vs LBFGSB_force), the simulation version and the NNMFit version; the scan with the old simulation, NNMFit v0.3.0 and default livetime reproduces the earlier benchmark `hese/SAY/hese_HESEBestfit_SPL_noinel_nosyst` (best fit within 0.002, |ΔTS| ≤ 0.16).
