import pandas as pd
import sys, glob, pickle

files = glob.glob("/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/dag_scans/flavor_globalfit/hese/mcd-simpletopology_flux-hese_feat-11features_plus_rloglmilli_econf_evtgen/bdt1_0.333333_bdt2_0.366667_length_10_10bdtprod_threshold_0.122_combinedBaseline/*.pickle")

for file in files:
    print(30*"-")
    print(file)
    f = open(file, "rb")
    p = pickle.load(f)
    fit_param = p['fit-result'][1]
    lik = p['fit-result'][0]
    fixed_param = p['fixed-parameters']
    opt_output = p['fit-result'][2]
    succes = opt_output["success"]

    print(fixed_param, succes)
    print(opt_output)
    print(fit_param)
    print(lik)