#!/usr/bin/env python3
import tables
import os
import sys
from collections import defaultdict
import numpy as np
from scipy.stats import chi2, kstest
from common import calculator
from matplotlib import pyplot as plt
from matplotlib.colors import SymLogNorm, LogNorm, Normalize
import logging
import argparse

sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing/performance")
from lowlevel import *
from extract_data import *
from plot_utils import *

slc = np.s_[:]

def compare( nufiles, outpath ):
    print("compare")

    os.system(f"mkdir -p {outpath}")

    # get the data
    data = []
    for nufile in nufiles*7: data += [ extract_data_combined(nufile) ]

    print("Datasets with", [len(dataset) for dataset in data])

    nbins = 20

    # length
    plot_lenres_len( data, fit_keys = ["len_Taupede"], true_key = "len_tru_tianlu", 
                     labels = ["Taupede"], outpath=outpath, bins = np.linspace(0, 100,30) )
    plot_lenres_len( data, fit_keys = ["len_Taupede"], true_key = "len_tru_neha", 
                     labels = ["Taupede"], outpath=outpath, bins = np.linspace(0, 100,30) )

    plot_len_fit( data, fit_keys = ["len_Taupede"], 
                  labels=["Taupede"], outpath=outpath, bins = np.linspace(0, 100,nbins ) )

    # energy asymmetry
    plot_medasmres_len( data, fit_keys = ["asm_Taupede"], asm_true_key = "asm_tru_tianlu", len_tru_key="len_tru_tianlu",
                        labels=["Taupede"], outpath=outpath, bins = np.linspace(0, 100,nbins) )
    plot_medasmres_len( data, fit_keys = ["asm_Taupede"], asm_true_key = "asm_tru_tianlu", len_tru_key="len_tru_neha",
                        labels=["Taupede"], outpath=outpath, bins = np.linspace(0, 100,nbins) )

    plot_medasmres_len( data, fit_keys = ["asm_Taupede"], asm_true_key = "asm_tru_neha", len_tru_key="len_tru_tianlu",
                        labels=["Taupede"], outpath=outpath, bins = np.linspace(0, 100,nbins) )

    # energy
    plot_mederes( data, fit_keys = ["loge_Taupede","loge_Millipede","loge_MillipedeTrun","loge_RecoETot", "loge_Monopod"], true_key = "loge_tru_tianlu",
                  labels=["Taupede", "Millipede","MillipedeTrun","RecoETot", "Monopod"], outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_mederes( data, fit_keys = ["loge_Taupede","loge_Millipede","loge_MillipedeTrun","loge_RecoETot", "loge_Monopod"], true_key = "loge_tru_neha",
                  labels=["Taupede", "Millipede","MillipedeTrun","RecoETot", "Monopod"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    # direction
    plot_medangres( data, fit_keys = ["Taupede","Millipede", "Monopod"], true_key="tianlu",
                   labels=["Taupede", "Millipede", "Monopod"], outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_medangres( data, fit_keys = ["Taupede","Millipede", "Monopod"], true_key="neha",
                   labels=["Taupede", "Millipede", "Monopod"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_medangres_len( data, fit_keys = ["Taupede"], true_key="tianlu",
                        labels=["Taupede"], outpath=outpath, bins = np.linspace(0, 100,15) )

    # clean plots with less lines
    # nutau
    plot_medangres( data, fit_keys = ["Taupede","Millipede"], true_key="neha",
                   labels=["Taupede","Millipede"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_Taupede","loge_MillipedeTrun", "loge_Monopod"], true_key = "loge_tru_neha",
                  labels=["Taupede", "MillipedeTrun", "Monopod"], outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_mederes( data, fit_keys = ["loge_Taupede","loge_MillipedeTrun", "loge_Monopod"], true_key = "loge_tru_tianlu",
                  labels=["Taupede", "MillipedeTrun", "Monopod"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_Taupede","loge_Millipede","loge_MillipedeTrun"], true_key = "loge_tru_neha",
                  labels=["Taupede", "Millipede", "MillipedeTrun"], outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_mederes( data, fit_keys = ["loge_Taupede","loge_Millipede","loge_MillipedeTrun"], true_key = "loge_tru_tianlu",
                  labels=["Taupede", "Millipede", "MillipedeTrun"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    # nue
    plot_medangres( data, fit_keys = ["Monopod","Millipede"], true_key="neha",
                   labels=["Monopod", "Millipede"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_Monopod","loge_Millipede","loge_MillipedeTrun"], true_key = "loge_tru_neha",
                  labels=["Monopod", "Millipede", "MillipedeTrun"], outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_mederes( data, fit_keys = ["loge_Monopod","loge_Millipede","loge_MillipedeTrun"], true_key = "loge_tru_tianlu",
                  labels=["Monopod", "Millipede", "MillipedeTrun"], outpath=outpath, bins = np.linspace(4,8,nbins) )



###
### NuTau
###

# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9/NuTau.h5"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/v9/NuTau"
# compare(nufiles=nufiles,outpath=outpath)

###
### NuE
###

# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9/NuE.h5"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/v9/NuE"
# compare(nufiles=nufiles,outpath=outpath)

###
### NuMu
###

# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9/NuMu.h5"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/v9/NuMu"
# compare(nufiles=nufiles,outpath=outpath)
