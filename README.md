# Reconstruction processing

Wrappers around the reconstruction scripts from Tianlu:
- https://github.com/icecube/reco/tree/main/reco
I am using version with latest commit 7f46745:
- https://github.com/icecube/reco/commit/7f46745748cf3cdba04540f96bec1534d6ba7db1

- test.sh: example script for running Taupede reconstruction
- create_dag.py: creates and submits dag jobs to condor
- simulation_datasets.py: overview of which datasets to process 
- filtering: Contains script to filter HESE events from simulations.

## Versions

- v0: First 100 files of 22635 and 22634 based on filtering v0, which still had a lot of orphaned q frames.
- v1: Based on filtering v1.0, removed orphaned frames. Getting more statistics to check performance, and start playing with the BDT
- v2: Make a copy of the rec script, keep it here. Include proper HESE filtering with HESE_CausalQTot > 6000. Also add the HESE Millipede energyfit in the script. Also include some variable calculations.
- v3: again, i made a mistake in v2 with the hese selection. I should start from level2. I update the reco script, now I also run the SPEFit16 reco. I removed the bdt variables and other bullshit, will be in the hdf scripts from now. I only run a small subsample (100 files per flavor/energy) to check if I get the right event rate, followed by setting the late pulse cleaning off by setting a large residual argument (v4)
- v4: See v3, I set a large --residual 100000 to turn off late pulse cleaning
- v5: actual hese selection, all variables
- v6: trying to fix problems with HESEMillipede fit.
- v7: still found a shitty performance of HESEMillipede fit in v6. I saw 2 other differences with Neha in the HESEMillipede Fit params. ExcludeDeepCore = False and I shouldnt have had a BrightDOMThreshold=args.bdthres=15. Let's try again.
- v8: after discussing with tianlu, trying the exact exact same millipede settings as for the seeds. I am doubtful. But.. It seems to fix my problem. 
- v9: same as v8, but all flavors and energy ranges. I copied the hdf high energy tau files from v8.
- v10: do a check with new gcd from christopher/tianlu

## iceprod
- v0: copy of the scripts. remove filtering from script, ready for l6 cascade or l2 files