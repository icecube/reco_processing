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

def compare_spice_ftp( nufiles, labels, outpath ):
    print("compare")

    os.system(f"mkdir -p {outpath}")

    # get the data
    data = []
    for nufile in nufiles: data += [ extract_data_combined(nufile) ]

    print("Datasets with", [len(dataset) for dataset in data])

    nbins = 20

    # length
    plot_lenres_len( data, fit_keys = ["len_Taupede","len_Taupede"], true_key = "len_tru_tianlu",labels = labels, outpath=outpath, bins = np.linspace(0, 100,30) )
    plot_lenres_len( data, fit_keys = ["len_Taupede","len_Taupede"], true_key = "len_tru_neha",labels = labels, outpath=outpath, bins = np.linspace(0, 100,30) )

    plot_len_fit( data, fit_keys = ["len_Taupede","len_Taupede"], labels=labels, outpath=outpath, bins = np.linspace(0, 100,nbins ) )

    # energy asymmetry
    plot_medasmres_len( data, fit_keys = ["asm_Taupede","asm_Taupede"], asm_true_key = "asm_tru_tianlu", len_tru_key="len_tru_tianlu",labels=labels, outpath=outpath, bins = np.linspace(0, 100,nbins) )
    plot_medasmres_len( data, fit_keys = ["asm_Taupede","asm_Taupede"], asm_true_key = "asm_tru_tianlu", len_tru_key="len_tru_neha",labels=labels, outpath=outpath, bins = np.linspace(0, 100,nbins) )

    plot_medasmres_len( data, fit_keys = ["asm_Taupede","asm_Taupede"], asm_true_key = "asm_tru_neha", len_tru_key="len_tru_tianlu",labels=labels, outpath=outpath, bins = np.linspace(0, 100,nbins) )

    # energy
    plot_mederes( data, fit_keys = ["loge_Taupede","loge_Taupede"], true_key = "loge_tru_tianlu",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_mederes( data, fit_keys = ["loge_Taupede","loge_Taupede"], true_key = "loge_tru_neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_Millipede","loge_Millipede"], true_key = "loge_tru_tianlu",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_mederes( data, fit_keys = ["loge_Millipede","loge_Millipede"], true_key = "loge_tru_neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_MillipedeTrun","loge_MillipedeTrun"], true_key = "loge_tru_tianlu",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_mederes( data, fit_keys = ["loge_MillipedeTrun","loge_MillipedeTrun"], true_key = "loge_tru_neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_RecoETot","loge_RecoETot"], true_key = "loge_tru_tianlu",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_mederes( data, fit_keys = ["loge_RecoETot","loge_RecoETot"], true_key = "loge_tru_neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_Monopod","loge_Monopod"], true_key = "loge_tru_tianlu",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_mederes( data, fit_keys = ["loge_Monopod","loge_Monopod"], true_key = "loge_tru_neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )

    # direction
    plot_medangres( data, fit_keys = ["Taupede","Taupede"], true_key="tianlu",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_medangres( data, fit_keys = ["Taupede","Taupede"], true_key="neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_medangres( data, fit_keys = ["Monopod","Monopod"], true_key="tianlu",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_medangres( data, fit_keys = ["Monopod","Monopod"], true_key="neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_medangres( data, fit_keys = ["SPEFit16","SPEFit16"], true_key="tianlu",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_medangres( data, fit_keys = ["SPEFit16","SPEFit16"], true_key="neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_medangres( data, fit_keys = ["Millipede","Millipede"], true_key="tianlu",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_medangres( data, fit_keys = ["Millipede","Millipede"], true_key="neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_medangres_len( data, fit_keys = ["Taupede","Taupede"], true_key="tianlu",labels=labels, outpath=outpath, bins = np.linspace(0, 100,15) )
    plot_medangres_len( data, fit_keys = ["Taupede","Taupede"], true_key="neha",labels=labels, outpath=outpath, bins = np.linspace(0, 100,15) )


###
### NuTau
###

# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuTau.h5", 
#            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9/NuTau.h5"]
# labels = ["spice", "ftp"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/spice_tau_reco_vs_v9/NuTau"
# compare_spice_ftp(nufiles=nufiles, labels = labels,outpath=outpath)

###
### NuE
###

# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuE.h5", 
#            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9/NuE.h5"]
# labels = ["spice", "ftp"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/spice_tau_reco_vs_v9/NuE"
# compare_spice_ftp(nufiles=nufiles, labels = labels,outpath=outpath)

###
### NuMu
###

nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuMu.h5", 
           "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9/NuMu.h5"]
labels = ["spice", "ftp"]
outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/spice_tau_reco_vs_v9/NuMu"
compare_spice_ftp(nufiles=nufiles, labels = labels,outpath=outpath)
