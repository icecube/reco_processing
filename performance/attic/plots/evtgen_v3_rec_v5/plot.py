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

def compare_evtgen( nufiles, outpath ):
    print("compare")

    os.system(f"mkdir -p {outpath}")

    # get the data
    data = []
    for nufile in nufiles: data += [ extract_data_combined(nufile) ]

    print("Datasets with", [len(dataset) for dataset in data])

    labels = ["Taupede", "EvtGen Thijs", "EvtGen Max", "EvtGen Combined"]
    labels_mono = ["Monopod", "EvtGen Thijs", "EvtGen Max", "EvtGen Combined"]
    labels_spe = ["SPEFit16", "EvtGen Thijs", "EvtGen Max", "EvtGen Combined"]


    nbins = 15

    # length
    plot_lenres_len( data, fit_keys = ["len_Taupede","len_EventGeneratorDC_Thijs","len_EventGeneratorDC_Max","len_EventGeneratorDC_Combined"], 
                     true_key = "len_tru_tianlu",labels = labels, outpath=outpath, bins = np.linspace(0, 100,30) )
    plot_lenres_len( data, fit_keys = ["len_Taupede","len_EventGeneratorDC_Thijs","len_EventGeneratorDC_Max","len_EventGeneratorDC_Combined"], 
                     true_key = "len_tru_neha",labels = labels, outpath=outpath, bins = np.linspace(0, 100,30) )

    plot_len_fit( data, fit_keys = ["len_Taupede","len_EventGeneratorDC_Thijs","len_EventGeneratorDC_Max","len_EventGeneratorDC_Combined"], 
                  labels=labels, outpath=outpath, bins = np.linspace(0, 100,nbins ) )

    plot_lenres_len( data, fit_keys = ["len_EventGeneratorDC_Thijs","len_EventGeneratorDC_Max","len_EventGeneratorDC_Combined"], 
                     true_key = "len_tru_tianlu",labels = labels[1:], outpath=outpath, bins = np.linspace(0, 100,30) )

    # energy asymmetry
    plot_medasmres_len( data, fit_keys = ["asm_Taupede","asm_EventGeneratorDC_Thijs","asm_EventGeneratorDC_Max","asm_EventGeneratorDC_Combined"], 
                        asm_true_key = "asm_tru_tianlu", len_tru_key="len_tru_tianlu",labels=labels, outpath=outpath, bins = np.linspace(0, 100,nbins) )
    plot_medasmres_len( data, fit_keys = ["asm_Taupede","asm_EventGeneratorDC_Thijs","asm_EventGeneratorDC_Max","asm_EventGeneratorDC_Combined"], 
                        asm_true_key = "asm_tru_tianlu", len_tru_key="len_tru_neha",labels=labels, outpath=outpath, bins = np.linspace(0, 100,nbins) )

    plot_medasmres_len( data, fit_keys = ["asm_EventGeneratorDC_Thijs","asm_EventGeneratorDC_Max","asm_EventGeneratorDC_Combined"], 
                        asm_true_key = "asm_tru_tianlu", len_tru_key="len_tru_tianlu",labels=labels[1:], outpath=outpath, bins = np.linspace(0, 100,nbins) )

    # energy
    plot_mederes( data, fit_keys = ["loge_Taupede","loge_EventGeneratorDC_Thijs","loge_EventGeneratorDC_Max","loge_EventGeneratorDC_Combined"], 
                  true_key = "loge_tru_tianlu",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_mederes( data, fit_keys = ["loge_Taupede","loge_EventGeneratorDC_Thijs","loge_EventGeneratorDC_Max","loge_EventGeneratorDC_Combined"], 
                  true_key = "loge_tru_neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_Monopod","loge_EventGeneratorDC_Thijs","loge_EventGeneratorDC_Max","loge_EventGeneratorDC_Combined"], 
                  true_key = "loge_tru_tianlu",labels=labels_mono, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_mederes( data, fit_keys = ["loge_Monopod","loge_EventGeneratorDC_Thijs","loge_EventGeneratorDC_Max","loge_EventGeneratorDC_Combined"], 
                  true_key = "loge_tru_neha",labels=labels_mono, outpath=outpath, bins = np.linspace(4,8,nbins) )

    # direction
    plot_medangres( data, fit_keys = ["Taupede","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                   true_key="tianlu",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_medangres( data, fit_keys = ["Taupede","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                   true_key="neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_medangres( data, fit_keys = ["Monopod","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                   true_key="tianlu",labels=labels_mono, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_medangres( data, fit_keys = ["Monopod","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                   true_key="neha",labels=labels_mono, outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_medangres( data, fit_keys = ["SPEFit16","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                   true_key="tianlu",labels=labels_spe, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_medangres( data, fit_keys = ["SPEFit16","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                   true_key="neha",labels=labels_spe, outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_medangres_len( data, fit_keys = ["Taupede","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                        true_key="tianlu",labels=labels, outpath=outpath, bins = np.linspace(0, 100,15) )
    plot_medangres_len( data, fit_keys = ["Taupede","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                        true_key="neha",labels=labels, outpath=outpath, bins = np.linspace(0, 100,15) )


###
### NuTau
###

# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5/NuTau.h5",
#            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5/NuTau.h5",
#            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5/NuTau.h5",
#            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5/NuTau.h5"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/evtgen_v3_rec_v5/NuTau_EvtGen"
# compare_evtgen(nufiles=nufiles, outpath=outpath)

###
### NuE
###

nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5/NuE.h5",
           "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5/NuE.h5",
           "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5/NuE.h5",
           "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5/NuE.h5"]
outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/evtgen_v3_rec_v5/NuE_EvtGen"
compare_evtgen(nufiles=nufiles, outpath=outpath)

###
### NuMu
###



