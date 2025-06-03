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

from lowlevel import *

# general
slc = np.s_[:]

# binning
len_bins = np.arange(0, 101)

def extract_data( nufile, key ):

    tf = tables.open_file(nufile)

    data = {}
    data["len_fit"] = tf.get_node( f'/{key}').cols.length[:][slc]
    data["len_tru"] = tf.root.cc.cols.length[:][slc]
    data["asm_fit"] = get_easymm(tf.get_node(f'/{key}Particles'))[slc]
    data["asm_tru"] = tf.root.cc_easymm[slc]['value']
    data["cth_reco"] = np.cos(tf.get_node(f'/{key}').cols.zenith[:][slc])
    data["azi_reco"] = tf.get_node(f'/{key}').cols.azimuth[:][slc]
    data["cth_tru"] = np.cos(tf.root.cc.cols.zenith[:][slc])
    data["azi_tru"] = tf.root.cc.cols.azimuth[:][slc]
    tf.close()

    return data


def compare( nufiles, keys, labels, outpath ):
    print("compare")

    # get the data
    data = [ extract_data(nufile, key) for (nufile, key) in zip(nufiles, keys) ]

    print("len data", len(data))
    print(data[0].keys())
    print(data[1].keys())

    ###
    ### lenres
    ###

    plt.figure()
    for i, label in enumerate(labels):
        print("plotting", i, labels[i])

        plot_quartiles_vs_x( (data[i]["len_fit"] - data[i]["len_tru"]) / data[i]["len_tru"],
                              data[i]["len_tru"],
                              len_bins[::3],
                              labels[i])
    plt.xlabel(r'Length [m]')
    plt.ylabel('$(L_{rec}-L_{tru})/L_{tru}$')
    plt.axhline(0, linewidth=0.5, color='gray', linestyle='--')
    plt.xlim(0, 50)
    plt.ylim(-0.5, 0.5)
    plt.legend()
    plt.savefig(f'{outpath}/test_medlenres_test.png', bbox_inches='tight')
    plt.clf()


    ###
    ### easym
    ###
    plt.figure()
    for i, label in enumerate(labels):
        plot_quartiles_vs_x(data[i]["asm_fit"] - data[i]["asm_tru"],
                            data[i]["len_tru"],
                            len_bins[::3],
                            labels[i])
    plt.xlabel(r'Length [m]')
    plt.ylabel('$A_{rec}-A_{tru}$')
    plt.axhline(0, linewidth=0.5, color='gray', linestyle='--')
    plt.xlim(0, 50)
    plt.ylim(-0.5, 0.5)
    plt.legend()
    plt.savefig(f'{outpath}/test_medasmres_len.png', bbox_inches='tight')

if __name__ == "__main__":
    
    # nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v7.0/NuTau_22634.h5", "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v8.0/NuTau_22634.h5"]
    # keys = ["TaupedeFit_iMIGRAD_PPB0", "TaupedeFit_iMIGRAD_PPB0"]
    # labels = ["v7.0", "v8.0"]

    # outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/output/compare/"

    # compare(nufiles=nufiles, keys=keys, labels = labels,outpath=outpath)


    nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/neha_spice/NuTau.h5", "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v8.0_old/NuTau_22634.h5"]
    keys = ["HESETaupedeFit", "TaupedeFit_iMIGRAD_PPB0"] 
    labels = ["Current work", "Improved reconstruction"]

    outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/output/compare/"

    compare(nufiles=nufiles, keys=keys, labels = labels,outpath=outpath)