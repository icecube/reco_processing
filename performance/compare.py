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
    print(f"dataset {key} has {len(data["len_fit"])} evts")

    return data

def extract_data_evtgen( nufile, key ):

    tf = tables.open_file(nufile)

    data = {}
    data["len_fit"] = tf.get_node( f'/{key}').cols.cascade_cascade_00001_distance[:][slc]
    data["len_tru"] = tf.root.cc.cols.length[:][slc]
    data["asm_fit"] = get_easymm_evtgen(tf.get_node(f'/{key}'))[slc]
    data["asm_tru"] = tf.root.cc_easymm[slc]['value']
    data["cth_reco"] = np.cos(tf.get_node(f'/{key}').cols.cascade_zenith[:][slc])
    data["azi_reco"] = tf.get_node(f'/{key}').cols.cascade_azimuth[:][slc]
    data["cth_tru"] = np.cos(tf.root.cc.cols.zenith[:][slc])
    data["azi_tru"] = tf.root.cc.cols.azimuth[:][slc]
    tf.close()
    print(f"dataset {key} has {len(data["len_fit"])} evts")

    return data


def plot_lenres_len( data, labels, outpath ):

    plt.figure()
    for i, label in enumerate(labels):
        plot_quartiles_vs_x( (data[i]["len_fit"] - data[i]["len_tru"]) / data[i]["len_tru"],
                              data[i]["len_tru"],
                              len_bins[::3],
                              labels[i])
    plt.xlabel(r'Length [m]')
    plt.ylabel('$(L_{rec}-L_{true})/L_{true}$')
    plt.axhline(0, linewidth=0.5, color='gray', linestyle='--')
    plt.xlim(0, 50)
    plt.ylim(-0.5, 0.5)
    plt.legend()
    plt.savefig(f'{outpath}/test_medlenres_test.png', bbox_inches='tight')
    plt.clf()

def plot_medasmres_len( data, labels, outpath ):

    plt.figure()
    for i, label in enumerate(labels):
        plot_quartiles_vs_x(data[i]["asm_fit"] - data[i]["asm_tru"],
                            data[i]["len_tru"],
                            len_bins[::3],
                            labels[i])
    plt.xlabel(r'Length [m]')
    plt.ylabel('$A_{rec}-A_{true}$')
    plt.axhline(0, linewidth=0.5, color='gray', linestyle='--')
    plt.xlim(0, 50)
    plt.ylim(-0.5, 0.5)
    plt.legend()
    plt.savefig(f'{outpath}/test_medasmres_len.png', bbox_inches='tight')

def compare_files( nufiles, keys, labels, outpath ):
    print("compare")

    # get the data
    data = []
    for (nufile, key) in zip(nufiles, keys):
        if "EventGenerator" in key:
            data += [extract_data_evtgen(nufile, key)]
        else: data += [ extract_data(nufile, key) ]

    print("Datasets with", [len(dataset) for dataset in data])

    plot_lenres_len( data, labels, outpath )

    plot_medasmres_len( data, labels, outpath )


if __name__ == "__main__":
    
    # nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v7.0/NuTau_22634.h5", "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v8.0/NuTau_22634.h5"]
    # keys = ["TaupedeFit_iMIGRAD_PPB0", "TaupedeFit_iMIGRAD_PPB0"]
    # labels = ["v7.0", "v8.0"]
    # outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/output/compare/"
    # compare(nufiles=nufiles, keys=keys, labels = labels,outpath=outpath)


    # # nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/neha_spice/NuTau.h5", "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1/NuTau_22634_0000000-0000999.h5"]
    # nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/neha_spice/NuTau.h5", "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1/NuTau.h5"]
    # keys = ["HESETaupedeFit", "TaupedeFit_iMIGRAD_PPB0"] 
    # labels = ["This work", "Future improved reconstruction"]
    # outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/compare/"
    # compare(nufiles=nufiles, keys=keys, labels = labels,outpath=outpath)

    # nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1/NuTau.h5", "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/rec_v1_bright/NuTau.h5"]
    # keys = ["TaupedeFit_iMIGRAD_PPB0", "TaupedeFit_iMIGRAD_PPB0_bright"] 
    # labels = ["v1 reco", "with bright"]
    # outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/bright/"
    # compare_files(nufiles=nufiles, keys=keys, labels = labels,outpath=outpath)


    nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1/NuTau.h5", 
               "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v0_rec_v1/NuTau.h5",
               "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v0_rec_v1/NuTau.h5"]
    keys = ["TaupedeFit_iMIGRAD_PPB0", 
            "EventGeneratorDC_Max",
            "EventGeneratorDC_Thijs"] 
    labels = ["v1 reco", "EvtGen Max", "EvtGen Thijs"]
    outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/evtgen/"
    compare_files(nufiles=nufiles, keys=keys, labels = labels,outpath=outpath)



