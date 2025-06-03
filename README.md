# Reconstruction processing

- test.sh: example script for running Taupede reconstruction
- create_dag.py: creates and submits dag jobs to condor
- simulation_datasets.py: overview of which datasets to process 
- filtering: Contains script to filter HESE events from simulations.

## Versions

- v0: First 100 files of 22635 and 22634 based on filtering v0, which still had a lot of orphaned q frames.
- v1: Based on filtering v1.0, removed orphaned frames. Getting more statistics to check performance, and start playing with the BDT