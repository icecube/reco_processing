# step1_hese_flux_reunblind / studies

Side studies for the step1 (flux) reunblinding fit. Shared helpers come from `../../step2_hese_flavor_reunblind/analysis_utils.py`.

## compare_SAY_Poisson.ipynb
Compares the step1 1D scan with the SAY likelihood (PassingHESE + _fine combined) to the same scan with the Poisson likelihood (`..._PassingHESE_Poisson`): best fits and 1σ errors side by side, overlaid profile likelihoods, an overview of the shifts, and a 2-column LaTeX table (`plots_compare_SAY_Poisson/`). Both fits are without detector priors (the `priors` key was not read by NNMFit).
The signal agrees (astro_norm 1.65 vs 1.71, γ 2.81 in both) but Poisson gives clearly smaller upper errors on astro_norm (+0.56 vs +0.85) and γ (+0.17 vs +0.27); the muon norm shifts by ~1σ (0.59 → 0.83).

## compare_fixedprior.ipynb
Compares the step1 results after fixing the detector priors (`..._fixedprior`, `prior` key): a SAY table with HESE-7.5, HESE-12 flavor, this analysis without detector priors and with fixed priors, a SAY vs Poisson table with fixed priors (pandas and LaTeX), and the 2D (γ, Φ0) scan compared with HESE-7.5 (fixed priors alone and a 3-way plot with the scan without detector priors, `plots_compare_fixedprior/`).
With the priors the signal barely moves (astro_norm 1.65 → 1.68, γ 2.81 → 2.82) but its upper errors shrink (astro_norm +0.85 → +0.50, γ +0.27 → +0.17) and the detector parameters move off their range edges (ice_crystal 0.81 → 0.93) with two-sided errors; SAY and Poisson now agree on the signal (astro_norm 1.683 vs 1.682, γ 2.816 vs 2.814).
