taken from /data/user/nlad/NNMFitStuff/HESE_spice-bfr_Binning.ipynb

I am trying to compare my plot to Neha's plot, so I started simple, comparing our events from:

<class 'pandas.io.pytables.HDFStore'>
File path: /data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline/hdf_files/PostMask/22082_60TeVCut.hdf5

<class 'pandas.io.pytables.HDFStore'>
File path: /data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuE_22082.h5

Turns out I had events that neha didnt have, and vice versa. Then looking at one of these events, I saw that Neha's hdf had a different RecoETot than in her reconstructed icetray files. For me, this comparison seems hopeless.
