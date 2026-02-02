import sys
import numpy as np
import pandas as pd

from weights import *

livetime_yr = 11.687
livetime_s  = livetime_yr * 365.25 * 24 * 3600 # 11.687 year

def print_event_rate(simulation_dataset, level_dict=None, livetime_s=livetime_s):
    """
    Print expected event rates per level for a single simulation_dataset.
    
    simulation_dataset: dict for one dataset (e.g., ftp_ensemble_ani_v1)
    level_dict: optional dict mapping level -> label; if None, uses all levels in NuE
    """

    # Use all levels in NuMu if no level_dict provided
    if level_dict is None:
        level_dict = {level: level for level in simulation_dataset["NuMu"]["weighters"].keys()}

    data = {}

    for level, label in level_dict.items():
        channel_data = {}

        # Astro fluxes
        for flavor in ["NuE", "NuMu", "NuTau"]:
        # for flavor in ['NuE_midE','NuE_highE', "NuMu_midE","NuMu_highE", "NuTau_midE","NuTau_highE"]:

            if flavor not in simulation_dataset or level not in simulation_dataset[flavor]["weighters"]:
                continue
            w_obj = simulation_dataset[flavor]["weighters"][level]
            # Choose flux model based on label (HESE vs cascade)
            if "HESE" in label or "hese" in label.lower():
                weights = w_obj.get_weights(AstroFluxModel_HESE) * livetime_s
            else:
                weights = w_obj.get_weights(AstroFluxModel_cascade) * livetime_s
            rate = np.sum(weights)
            error = np.sqrt(np.sum(weights**2))
            channel_data[f"astro_{flavor}"] = f"{rate:.2f} ± {error:.2f}"

        # Conventional & prompt using NuAll
        if "NuAll" in simulation_dataset and level in simulation_dataset["NuAll"]["weighters"]:
            w_obj = simulation_dataset["NuAll"]["weighters"][level]

            weights_conv = w_obj.get_weights(generator_conv) * livetime_s
            rate_conv = np.sum(weights_conv)
            err_conv = np.sqrt(np.sum(weights_conv**2))
            channel_data["conv"] = f"{rate_conv:.3f} ± {err_conv:.3f}"

            weights_prompt = w_obj.get_weights(generator_pr) * livetime_s
            rate_prompt = np.sum(weights_prompt)
            err_prompt = np.sqrt(np.sum(weights_prompt**2))
            channel_data["prompt"] = f"{rate_prompt:.2f} ± {err_prompt:.2f}"

        data[label] = channel_data

    # Build DataFrame
    df = pd.DataFrame.from_dict(data, orient="index")
    # columns_order = [f"astro_{f}" for f in ["NuE", "NuMu", "NuTau"]] + ["conv", "prompt"]
    # df = df[[c for c in columns_order if c in df.columns]]
    print(df.to_string())

