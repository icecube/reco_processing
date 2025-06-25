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
- v2: Make a copy of the rec script, keep it here. Include proper HESE filtering with HESE_CausalQTot > 6000. Also add the HESE Millipede energyfit in the script. 