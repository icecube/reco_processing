# Compare spice ftp

Here I am comparing my batch of reco files with the spice simulations.

## Lower muon rate

First problem I ran into in compare_spice_ftp.ipynb is that the muon rate is significantly lower:
                     astro_NuE    astro_NuMu   astro_NuTau         conv       prompt
evtgen_v1_rec_v2  56.20 ± 0.54  14.74 ± 0.22  33.91 ± 0.39  0.00 ± 0.00  0.78 ± 0.01
spice_tau_reco    56.77 ± 0.56  20.42 ± 0.22  34.89 ± 0.43  0.00 ± 0.00  0.80 ± 0.01
I am trying to tackle that in lower_muon_rate.ipynb.

It seems that we really have lets muon events at HESE level. Now creating hdf files at l3 cascade level to see if the difference still persists.

## No conventional neutrinos

Where are they? no_conv_nu.ipynb

Problem found: I had a bug in my script that creates a table. Only the conventional neutrinos from nutau were printed. This leads to a low number

## relative error or weighted error?