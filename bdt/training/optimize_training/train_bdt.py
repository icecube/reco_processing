#!/bin/python
import pandas as pd
import sys
from analysis_tools.workflows.evaluation_flow import evaluation_flow
from analysis_tools.workflows.BDT_pipeline import run_bdt_pipeline
from analysis_tools.namings.BDT_feature_naming import BDT_feature_name_change
from analysis_tools.BDT_tools.Testset_preparation import create_learning_input,annotate_labels
from analysis_tools.BDT_tools.BDT_evaluation import find_best_two_bdt_thresholds,plot_bdt_threshold_scan
from analysis_tools.workflows.prediction_flow import prediction_flow,predict_scores
from analysis_tools.my_selectors.apply_selection import apply_selection

### arguments
import argparse

parser = argparse.ArgumentParser(
    description='Training bdt model',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-o', '--out', 
                    default='/data/user/tvaneede/GlobalFit/reco_processing/bdt/training/optimize_training/output/test', 
                    required=True,
                    help='out path')
parser.add_argument('--mcd', 
                    choices=('flavor', 'truetopology', 'simpletopology'),
                    default='flavor', 
                    required=True,
                    help='model config name')
parser.add_argument('--flux', 
                    choices=('hese', 'cascade', "gamma2"),
                    default='flavor', 
                    required=True,
                    help='flux name')
parser.add_argument('--feat', 
                    default='13features', 
                    required=True,
                    help='feature name')

args = parser.parse_args()

for k, v in vars(args).items():
    print(f"{k:10} : {v}")

### input data
# df_train = pd.read_parquet("/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/datasets/bdt/SnowStorm_v2_HESE_Baseline_v7_noMuon/dataset_IC86_pass2_SnowStorm_v2_FTP_v7_noMuon.parquet")
df_train = pd.read_parquet("/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/datasets/flavor_globalfit/hese/combined/IC86_pass2_SnowStorm_v2_FTP_Baseline_Extra_hdf-v1_noMuon/dataset_IC86_pass2_SnowStorm_v2_FTP_Baseline_Extra_hdf-v1_noMuon.parquet")

df_test = df_train.copy()

### model configs
sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing/bdt/training/optimize_training")
from model_configs_dict import model_configs_dict
model_configs = model_configs_dict[args.mcd]

### precuts
Taupede_name = "TaupedeFit_iMIGRAD_PPB0"
precut_dict = {
'MonopodFit_iMIGRAD_PPB0_energy':('>', 10**4.5),
'Taupede_Distance':[('>', 10),('<', 400)],
  f'{Taupede_name}_1_x':[('>', -500),('<', 500)],
  f'{Taupede_name}_1_y':[('>', -500),('<', 500)],
  f'{Taupede_name}_1_z':{'and':[('>', -500),('<', 500)],
                                  'or':[('>', -50), ('<', -150)]},
  f'{Taupede_name}_2_x':[('>', -500),('<', 500)],
  f'{Taupede_name}_2_y':[('>', -500),('<', 500)],
  f'{Taupede_name}_2_z':{'and':[('>', -500),('<', 500)],
                                  'or':[('>', -50), ('<', -150)]},
}

df_train_precut = apply_selection(df_train,precut_dict).copy()
df_test_precut = apply_selection(df_test,precut_dict).copy()

### reweight
from flux_model_dict import flux_model_dict
flux_model = flux_model_dict[args.flux]

per_flavor_norm = flux_model["per_flavor_norm"]
gamma_astro = flux_model["gamma_astro"]
norm_factor = 0.5 * per_flavor_norm * 1e-18
for df in (df_train_precut, df_test_precut):
    e = df["MCPrimaryEnergy"] / 1e5
    df["fluxless_weight"] = df["powerlaw"] * 1e18 * e**2
    df["weight"] = df["fluxless_weight"] * norm_factor * e**(-gamma_astro)

### features list
from features_list_dict import features_list_dict
features_list = features_list_dict[args.feat]

### train
model_name = 'BDT_workflow_test'

models, summary = run_bdt_pipeline(
    df_train_precut, df_train_precut,
    global_precuts = None,
    model_configs  = model_configs,
    features       = features_list,
    weight_col     = 'weight',
    purity_target  = 0.90,
    score_cols     = [f'bdt1_score_{model_name}',f'bdt2_score_{model_name}'],
    train_outdir   = f'{args.out}/train',
    eval_outdir    = f'{args.out}/eval',
) 

