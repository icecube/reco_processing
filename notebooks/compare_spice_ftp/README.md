# Compare spice ftp

Here I am comparing my batch of reco files with the spice simulations.

## Compare_spice_ftp.ipynb

the actual notebook to compare the simulations. I ran into a lot of problems, that are fixed now with v5 reco and evtgen_v2_rec_v5.

## Lower muon rate

First problem I ran into in compare_spice_ftp.ipynb is that the muon rate is significantly lower:
                     astro_NuE    astro_NuMu   astro_NuTau         conv       prompt
evtgen_v1_rec_v2  56.20 ± 0.54  14.74 ± 0.22  33.91 ± 0.39  0.00 ± 0.00  0.78 ± 0.01
spice_tau_reco    56.77 ± 0.56  20.42 ± 0.22  34.89 ± 0.43  0.00 ± 0.00  0.80 ± 0.01
I am trying to tackle that in lower_muon_rate.ipynb.

It seems that we really have lets muon events at HESE level. Now creating hdf files at l3 cascade level to see if the difference still persists.

The problem was: I should start from level2 files. 

## No conventional neutrinos

Where are they? no_conv_nu.ipynb

Problem found: I had a bug in my script that creates a table. Only the conventional neutrinos from nutau were printed. This leads to a low number

## relative error or weighted error

How should I represent errors? error.ipynb

I should use the sqrt of the weighted sum, Neha's method.

## Compare true varialbes neha tianlu

compare_true_var_tianlu_neha.ipynb

Many variables are very similar:
- RecoETot, RecoAzimuth, RecoZenith

But the length and energy asymmetry are different.
- Energy asymmetry: I like Neha's implementation better. She actually counts the deposited energy from the different cascades.
- Length: I like Tianlu's definition better. It is the length of the tau lepton, instead of the difference between the shower maxima (Neha)
