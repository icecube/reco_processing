# Debugging the BDT

Workflow
- Extract the best fits for the old pid, and some new BDT iterations. Create configs with the input parameters, and separate for each component: run_post_fit_scripts.ipynb
- Create gradients for the combined hese dataset, for all different BDT variables: make_gradients.sh
- Create config files for the new systematic gradients: make_debug_bdt_configs.py
- Create graphs for plotting: reco_space_graphs.ipynb
