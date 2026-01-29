import pandas as pd
import numpy as np
from argparse import ArgumentParser
import os,sys
import joblib
import pyForwardFolding as pyFF
import matplotlib.pyplot as plt
import shutil
from pathlib import Path
import copy
### arguments
import argparse

sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing/bdt/training/optimize_training")
from features_list_dict import features_list_dict

sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing/bdt/notebooks/")
from bdt import *

sys.path.append( "/data/user/tvaneede/utils" )
from flavor_fracs import *
from FlavourScansPlotting import *

# asimov scan points
points = pd.read_pickle(
'/data/user/tvaneede/GlobalFit/custom_scan_flavor/default_custom_scan_points_flavor.pickle'
)
astro_nue_ratio = np.asarray(points['astro_nue_ratio'])
astro_nutau_ratio = np.asarray(points['astro_nutau_ratio'])

def safe_remove(path):
    path = Path(path)

    if not path.exists():
        print(f"[skip] file does not exist: {path}")
        return

    if path.is_dir():
        raise IsADirectoryError(f"Refusing to delete directory: {path}")

    path.unlink()
    print(f"[removed] {path}")

def update_file( file_path, input_parameters ):

    # Read the file, modify its contents, and overwrite it
    with open(file_path, "r+", encoding="utf-8") as file:
        content = file.read()

        # Replace text
        for old_text, new_text in input_parameters.items():
            content = content.replace(old_text, new_text)

        # Move cursor to the beginning and overwrite the file
        file.seek(0)
        file.write(content)
        file.truncate()  # Remove any leftover content if new content is shorter

def check_missing_events(df_input, dfs_output):
    counts = {ch: len(df) for ch, df in dfs_output.items()}
    empty_channels = [ch for ch, c in counts.items() if c == 0]

    total_in = len(df_input)
    total_out = sum(counts.values())

    print("Event counts per channel:")
    for ch, c in counts.items():
        print(f"  {ch}: {c}")

    print(f"total events: {total_in}, sum of channels: {total_out}")

    if total_in != total_out: raise RuntimeError(f"Event mismatch: input={total_in}, output={total_out}")

    return empty_channels

def split_dataset( df_input, cut_bdt1, cut_bdt2, cut_length = 10 ):

    dfs_output = {}

    ### cascade
    mask_cascade = (df_input["bdt_scores1"] < cut_bdt1) | ((df_input["bdt_scores2"] > cut_bdt2) & (df_input["reco_length"] < cut_length))
    dfs_output["cascade"] = df_input[ mask_cascade ]

    ### double
    mask_double = (df_input["bdt_scores1"] > cut_bdt1) & (df_input["bdt_scores2"] > cut_bdt2) & (df_input["reco_length"] > cut_length)
    dfs_output["double"] = df_input[ mask_double ]

    ### track
    mask_track = (df_input["bdt_scores1"] > cut_bdt1) & (df_input["bdt_scores2"] < cut_bdt2)
    dfs_output["track"] = df_input[ mask_track ]

    return dfs_output

def asimov_scan( ana, datasets, params ):
    obs, ssq = ana.evaluate(datasets,params)

    lik = pyFF.likelihood.PoissonLikelihood(ana,priors)
    mini = pyFF.minimizer.ScipyMinimizer(lik)
    best_fit = mini.minimize(obs,datasets)

    llhs = []

    for i in range(len(astro_nue_ratio)):
        res = mini.minimize(obs,datasets,fixed_pars={"nue_ratio": astro_nue_ratio[i], "nutau_ratio" :  astro_nutau_ratio[i] })
        llhs.append(res[2])

        if i % 20 == 0: 
            print(f"{i} / {len(astro_nue_ratio)}")
            # print(20*"=")
            # print(f"{i} / {len(astro_nue_ratio)}, nue_ratio {astro_nue_ratio[i]}, nutau_ratio {astro_nutau_ratio[i]}, {res[2]}")
            # print(res[0]["success"],res[0]["nit"],res[0]["nfev"],res[0]["njev"])
            # print(res[0]["x"])

    llhs = np.array(llhs)

    dllhs = 2 * (llhs - best_fit[2])

    astro_numu_ratio = np.ones_like(astro_nue_ratio)
    norm = astro_nue_ratio + astro_numu_ratio + astro_nutau_ratio
    fe = astro_nue_ratio/norm
    fmu = astro_numu_ratio/norm
    ftau = astro_nutau_ratio/norm

    return ftau,fe,dllhs



def polygon_area(x, y):
    # Close path if not already closed
    if x[0] != x[-1] or y[0] != y[-1]:
        x = np.append(x, x[0])
        y = np.append(y, y[0])
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

def plot_flavor_triangle(ftau,fe,dllhs,outpath):
    levels = [2.37]#,4.605]#4.605#, 5.99]
    levlabels = ['68%']#'90% CL']#,'95% CL']

    fig = plt.figure()
    tax = flavor_triangle()

    ftau_grid,fe_grid,ts_grid = grided_TS_nutau_nue(ftau,fe,dllhs,interp_method='linear', N_grid=17)

    # best fit
    tax.ca.scatter([1.0/3], [1.0/3], marker='*', facecolor='black', edgecolor='k', lw=0.5, s=80)

    C = tax.ca.contour(ftau_grid,fe_grid,ts_grid, 
                       levels,linestyles=["-"],linewidths=1.5)
    
    paths = C.get_paths()
    contour_size = 0.0
    for p in paths:
        v = p.vertices
        x, y = v[:, 0], v[:, 1]
        contour_size += polygon_area(x, y)

    plt.savefig(outpath,bbox_inches='tight')

    return contour_size, x, y

def event_rate( ana, config, datasets, params, livetime = 12*365*24*60*60 ):


    result = {}

    models = pyFF.config.models_from_config(config)
    obs, _ = ana.evaluate(datasets,params)

    # astro
    params_astro = copy.deepcopy(params)
    params_astro["conv_norm"]   = 0
    params_astro["conv_norm"] = 0

    params_conv = copy.deepcopy(params)
    params_conv["astro_norm"]  = 0
    params_conv["prompt_norm"] = 0

    params_prompt = copy.deepcopy(params)
    params_prompt["astro_norm"] = 0
    params_prompt["conv_norm"]  = 0
    params_conv["prompt_norm"] = 1

    for k,dkey in zip(obs.keys(),datasets.keys()):
        d = datasets[dkey]
        w = models[k]["neutrino_model"].evaluate(d,params_astro) 
        for nu_type, nu_name in zip([12,14,16],["NuE","NuMu","NuTau"]):
            mask = abs(d["true_type"]) == nu_type
            result[f"rate_{k}_{nu_name}"] = sum(w[mask]) * livetime

        result[f"rate_{k}_conv"]   = sum( models[k]["neutrino_model"].evaluate(d,params_conv) )   * livetime
        result[f"rate_{k}_prompt"] = sum( models[k]["neutrino_model"].evaluate(d,params_prompt) ) * livetime

    return result


if __name__ == "__main__":
    ### inputs 
    parser = argparse.ArgumentParser(
        description='Training bdt model',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-o', '--outpath', 
                        default='/data/user/tvaneede/GlobalFit/reco_processing/bdt/training/optimize_training/optimize_cuts/test', 
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

    model_name = f"mcd-{args.mcd}_flux-{args.flux}_feat-{args.feat}"
    feature_name = args.feat

    ### user settings
    main_dir = "/data/user/tvaneede/GlobalFit/reco_processing/bdt/training/optimize_training/optimize_cuts"
    model_dir = f"/data/user/tvaneede/GlobalFit/reco_processing/bdt/training/optimize_training/output/{model_name}/train"

    # infile = "/data/user/tvaneede/GlobalFit/BESTIE_thijs/dataset/dataset_IC86_pass2_SnowStorm_v2_FTP_v6_noMuon.parquet"
    infile = "/data/user/tvaneede/GlobalFit/reco_processing/sumstat/datasets/SnowStorm_v2_HESE_Baseline_v7_noMuon/dataset_IC86_pass2_SnowStorm_v2_FTP_v7_noMuon.parquet" # adding the ibr idc variables
    infile_filename = "input.parquet"

    output_dir = args.outpath
    os.system(f"mkdir -p {output_dir}")

    config_template = f"{main_dir}/config_pyff.yaml"
    config_input = f"config_input.yaml"

    ### main
    this_path = Path.cwd()
    config_dst = this_path / config_input
    infile_condor = this_path / infile_filename

    print(20*"=","running in directory", this_path)

    print(20*"=", f"copying {infile} to {infile_condor}")
    shutil.copy(infile, infile_condor)
    assert infile_condor.exists(), f"Input copy: {infile_condor}"

    print(20*"=", f"loading bdt {model_name}")
    model1 = joblib.load(f"{model_dir}/bdt1_model.pkl")
    model2 = joblib.load(f"{model_dir}/bdt2_model.pkl")

    print(20*"=", f"opening {infile_filename}")
    df_input = pd.read_parquet( infile_filename )

    print(20*"=", f"appending bdt with features {feature_name}")
    df_input = Append_BDT_pyFF(df_input, model1, model2, features_list_dict[feature_name])

    print(20*"=", f"copying {config_template} to {config_dst}")
    shutil.copy(config_template, config_dst)
    assert config_dst.exists(), f"Config copy failed: {config_dst}"

    print(20*"=", "update config file path")
    update_file(f"{this_path}/{config_input}", input_parameters={"<THIS_PATH>" : str(this_path)})

    bdt_cuts = np.linspace(0,1,31)

    rows = []

    for i in range(len(bdt_cuts)):
        for j in range(len(bdt_cuts)):
            cut_bdt1 = bdt_cuts[i]
            cut_bdt2 = bdt_cuts[j]

            print(20*"=", "creating 3 channels", cut_bdt1, cut_bdt2)

            dfs_output = split_dataset( df_input=df_input, cut_bdt1=cut_bdt1, cut_bdt2=cut_bdt2, cut_length=10 )
            empty = check_missing_events(df_input, dfs_output)
            if empty:
                print("Empty channels:", empty)
                continue

            print("writing channels to file")
            for channel,df_output in dfs_output.items(): 
                df_output.to_parquet(this_path / f"{channel}.parquet", index=False)

            print("loading pyff config")
            config = f"./{config_input}"
            ana = pyFF.config.analysis_from_config(config)
            datasets = pyFF.config.dataset_from_config(config)
            params, priors = pyFF.config.params_from_config(config)
            
            variance = ana.variance(datasets,params)

            if i % 3 == 0 and j % 3 == 0:
            # if False:
                print("asimov scan")
                ftau,fe,dllhs = asimov_scan( ana = ana, datasets = datasets, params = params )
                contour_size,x,y = plot_flavor_triangle(ftau,fe,dllhs, outpath=f"{output_dir}/bdt1-{cut_bdt1}_bdt2-{cut_bdt2}.pdf")
                df_contour = pd.DataFrame({"x": x,"y": y,})
                df_contour.to_parquet(f"{output_dir}/bdt1-{cut_bdt1}_bdt2-{cut_bdt2}.parquet")
            else:
                print("skipping asimov")
                contour_size = 1

            rows.append({
                "cut_bdt1" : cut_bdt1,
                "cut_bdt2" : cut_bdt2,
                "n_cascade": len(dfs_output["cascade"]),
                "n_double": len(dfs_output["double"]),
                "n_track": len(dfs_output["track"]),
                "contour_size" : float(contour_size),
                **{f"variance_{k}": float(v) for k, v in variance.items()},
                **{k : float(v) for k,v in event_rate(ana = ana, config = config, datasets = datasets, params = params).items()}
            })

            print("cleaning files")
            for channel in dfs_output: 
                safe_remove(this_path / f"{channel}.parquet")

        #     break
        # break

    print(f"store dataframe at {output_dir}")
    df = pd.DataFrame(rows)
    df.to_parquet(f"{output_dir}/optimization.parquet")

    print("final clean")
    safe_remove(infile_filename)
    safe_remove(config_dst)

