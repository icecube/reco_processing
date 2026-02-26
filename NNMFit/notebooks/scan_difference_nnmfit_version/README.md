I made a contour of the same likelihood scan with 2 different nnmfit versions. The result was very different. Turns out, one is not throwing away the failed fits.

Why do the fit fail? and why does the likelihood contour look fine including the failed fits?

Lets check

/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/dag_scans/flavor_globalfit/hese/mcd-simpletopology_flux-hese_feat-11features_plus_rloglmilli_econf_evtgen/bdt1_0.333333_bdt2_0.366667_length_10_10bdtprod_threshold_0.122_combinedBaseline/FitRes_astro_nue_ratio_p0_8725_astro_nutau_ratio_p0_1633.pickle
{'astro_nue_ratio': 0.8724553385957623, 'astro_nutau_ratio': 0.16327378479434979} False
{'success': False, 'message': 'ABNORMAL_TERMINATION_IN_LNSRCH', 'nfev': 82, 'nit': 40, 'warnflag': 2}
{'astro_norm': 3.091526607478308, 'gamma_astro': 2.898080824703695, 'inel_scale': 0.966659220849468, 'CR_grad': 0.1028816064800035, 'barr_h': -0.0010432922173516364, 'barr_w': -0.011471769163064766, 'barr_y': -0.033251628594809506, 'barr_z': -0.01748876574640077, 'conv_norm': 0.9817880397182167, 'delta_gamma': 0.00036887875690272734, 'prompt_norm': 0.9571601685969781}
136.48054554098883

Seems like the optimization stopped early. Perhaps we can try different tolerance, or another optimization algo.


Now lets check the log file from: /scratch/tvaneede/NNMFit/condor/12_02_2026_12_35_05/logs/astro_nue_ratio_p0_8725_astro_nutau_ratio_p0_1633.err

doesnt look too weird. I continue like this, but try a different minimizer later.