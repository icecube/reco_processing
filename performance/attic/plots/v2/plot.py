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

def plot_mederes_qtot(data, fit_keys, true_key, labels, outpath, bins = np.linspace(1, np.linspace(1, 7, 39)[26]+3, 46)):
    
    print("plot_mederes")

    plt.figure(figsize=(6, 4))

    for i, label in enumerate(labels):

        mask = data[i]["HESE_CausalQTot"] > 6000

        loge_fit = data[i][fit_keys[i]][mask]
        loge_tru = data[i][true_key][mask]
        
        plot_quartiles_vs_x((10**(loge_fit)-10**(loge_tru))/10**(loge_tru),
                            loge_tru,
                            bins,
                            label)
        plt.axhline(0, linewidth=0.5, color='gray', linestyle='--')
        plt.xlabel(r'$\log_{10}(E_{dep}$ [GeV]$)$')
        plt.ylabel('$(E_{rec}-E_{dep})/E_{dep}$')
        plt.ylim(-0.2, 0.2)
        plt.legend()

    plt.savefig(f'{outpath}/mederes_qtot_{"-".join(fit_keys)}_vs_{true_key}.png', bbox_inches='tight')
    plt.clf()


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
    plot_mederes( data, fit_keys = ["loge_Taupede","loge_RecoETot", "loge_Monopod"], true_key = "loge_tru_tianlu",
                  labels=["Taupede","RecoETot", "Monopod"], outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_mederes_qtot( data, fit_keys = ["loge_Taupede","loge_RecoETot", "loge_Monopod"], true_key = "loge_tru_tianlu",
                  labels=["Taupede","RecoETot", "Monopod"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_Taupede","loge_RecoETot", "loge_Monopod"], true_key = "loge_tru_neha",
                  labels=["Taupede","RecoETot", "Monopod"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    # direction
    plot_medangres( data, fit_keys = ["Taupede","Monopod"], true_key="tianlu",
                   labels=["Taupede", "Monopod"], outpath=outpath, bins = np.linspace(4,8,nbins) )




###
### NuTau
###

nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v2/NuTau.h5"]
outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/v2/NuTau"
compare(nufiles=nufiles,outpath=outpath)


###
### NuE
###

# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v2_rec_v5/NuE.h5"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/v5/NuE"
# compare(nufiles=nufiles,outpath=outpath)

###
### NuMu
###

# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v2_rec_v5/NuMu.h5"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/v5/NuMu"
# compare(nufiles=nufiles,outpath=outpath)
