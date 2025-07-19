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
from compare import *

slc = np.s_[:]

def extract_data( nufile, key, hypo ):

    tf = tables.open_file(nufile)

    data = {}
    data["cth_reco"] = np.cos(tf.get_node(f'/{key}').cols.zenith[:][slc])
    data["azi_reco"] = tf.get_node(f'/{key}').cols.azimuth[:][slc]
    data["loge_fit"] = np.log10(tf.get_node(f'/{fit_node_name(nufile)}').cols.energy[:][slc])

    if hypo == "tau":
        data["cth_tru"] = np.cos(tf.root.cc.cols.zenith[:][slc])
        data["azi_tru"] = tf.root.cc.cols.azimuth[:][slc]
        data["loge_tru"] = np.log10(tf.root.cc.cols.energy[:][slc])
    elif hypo == "cascade":
        data["cth_tru"] = np.cos(tf.root.cascade.cols.zenith[:][slc])
        data["azi_tru"] = tf.root.cascade.cols.azimuth[:][slc]
        data["loge_tru"] = np.log10(tf.root.cascade.cols.energy[:][slc])
    elif hypo == "track":
        data["cth_tru"] = np.cos(tf.root.track.cols.zenith[:][slc])
        data["azi_tru"] = tf.root.track.cols.azimuth[:][slc]
        data["loge_tru"] = np.log10(tf.root.track.cols.energy[:][slc])
    else:
        print("hypo not found")

    if "Taupede" in key:
        data["len_fit"] = tf.get_node( f'/{key}').cols.length[:][slc]
        data["len_tru"] = tf.root.cc.cols.length[:][slc]
        data["asm_fit"] = get_easymm(tf.get_node(f'/{key}Particles'))[slc]
        data["asm_tru"] = tf.root.cc_easymm[slc]['value']

    tf.close()
    print(f"dataset {key} has {len(data["cth_reco"])} evts")

    return data


def compare_files_v3_vs_v4( nufiles, keys, labels, outpath, hypo ):
    print("compare")

    os.system(f"mkdir -p {outpath}")

    # get the data
    data = []
    for (nufile, key) in zip(nufiles, keys):
        if "EventGenerator" in key:
            data += [extract_data_evtgen(nufile, key)]
        else: data += [ extract_data(nufile, key, hypo) ]

    print("Datasets with", [len(dataset) for dataset in data])

    nbins = 20

    if "Taupede" in keys[0]:
        plot_lenres_len( data, labels, outpath, bins = np.linspace(0, 100,30) )
        plot_medasmres_len( data, labels, outpath, bins = np.linspace(0, 100,nbins) )
        plot_len_fit( data, labels, outpath, bins = np.linspace(0, 100,nbins ) )
        plot_medangres_len( data, labels, outpath, np.linspace(0, 100,15) )

    plot_mederes( data, labels, outpath, bins = np.linspace(4,8,nbins) )
    plot_medangres( data, labels, outpath, bins = np.linspace(4,8,nbins) )


# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v3/NuTau.h5", "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v4/NuTau.h5"]
# keys = ["TaupedeFit_iMIGRAD_PPB0", "TaupedeFit_iMIGRAD_PPB0"] 
# labels = ["Taupede residual 1500", "Taupede residual 100000"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/compare/v3_vs_v4/NuTau_Taupede"
# hypo = "tau"
# compare_files_v3_vs_v4(nufiles=nufiles, keys=keys, labels = labels,outpath=outpath, hypo=hypo)

# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v3/NuE.h5", "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v4/NuE.h5"]
# keys = ["MonopodFit_iMIGRAD_PPB0", "MonopodFit_iMIGRAD_PPB0"] 
# labels = ["Monopod residual 1500", "Monopod residual 100000"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/compare/v3_vs_v4/NuE_Monopod"
# hypo = "tau"
# compare_files_v3_vs_v4(nufiles=nufiles, keys=keys, labels = labels,outpath=outpath, hypo=hypo)

nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v3/NuMu.h5", "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v4/NuMu.h5"]
keys = ["SPEFit16", "SPEFit16"] 
labels = ["v3", "v4"]
outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/compare/v3_vs_v4/NuMu_SPEFit"
hypo = "track"
compare_files_v3_vs_v4(nufiles=nufiles, keys=keys, labels = labels,outpath=outpath, hypo=hypo)


