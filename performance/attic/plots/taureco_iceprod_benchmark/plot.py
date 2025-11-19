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
    plot_lenres_len( data, fit_keys = ["len_Taupede","len_EventGeneratorDC_Thijs","len_EventGeneratorDC_Max"], true_key = "len_tru_tianlu", labels = ["Taupede", "EvtGen Thijs", "EvtGen Max"], outpath=outpath, bins = np.linspace(0, 100,30) )
    plot_lenres_len( data, fit_keys = ["len_Taupede","len_EventGeneratorDC_Thijs","len_EventGeneratorDC_Max"], true_key = "len_tru_neha", labels = ["Taupede", "EvtGen Thijs", "EvtGen Max"], outpath=outpath, bins = np.linspace(0, 100,30) )

    plot_len_fit( data, fit_keys = ["len_Taupede","len_EventGeneratorDC_Thijs","len_EventGeneratorDC_Max"], labels=["Taupede", "EvtGen Thijs", "EvtGen Max"], outpath=outpath, bins = np.linspace(0, 100,nbins ) )

    # energy asymmetry
    plot_medasmres_len( data, fit_keys = ["asm_Taupede","asm_EventGeneratorDC_Thijs","asm_EventGeneratorDC_Max"], asm_true_key = "asm_tru_tianlu", len_tru_key="len_tru_tianlu",
                        labels=["Taupede", "EvtGen Thijs", "EvtGen Max"], outpath=outpath, bins = np.linspace(0, 100,nbins) )
    plot_medasmres_len( data, fit_keys = ["asm_Taupede","asm_EventGeneratorDC_Thijs","asm_EventGeneratorDC_Max"], asm_true_key = "asm_tru_tianlu", len_tru_key="len_tru_neha",
                        labels=["Taupede", "EvtGen Thijs", "EvtGen Max"], outpath=outpath, bins = np.linspace(0, 100,nbins) )

    plot_medasmres_len( data, fit_keys = ["asm_Taupede","asm_EventGeneratorDC_Thijs","asm_EventGeneratorDC_Max"], asm_true_key = "asm_tru_neha", len_tru_key="len_tru_tianlu",
                        labels=["Taupede", "EvtGen Thijs", "EvtGen Max"], outpath=outpath, bins = np.linspace(0, 100,nbins) )

    # energy
    plot_mederes( data, fit_keys = ["loge_Taupede","loge_EventGeneratorDC_Thijs","loge_EventGeneratorDC_Max","loge_Millipede","loge_MillipedeTrun","loge_RecoETot", "loge_Monopod"], true_key = "loge_tru_tianlu",
                  labels=["Taupede", "EvtGen Thijs", "EvtGen Max", "Millipede","MillipedeTrun","RecoETot", "Monopod"], outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_mederes( data, fit_keys = ["loge_Taupede","loge_EventGeneratorDC_Thijs","loge_EventGeneratorDC_Max","loge_Millipede","loge_MillipedeTrun","loge_RecoETot", "loge_Monopod"], true_key = "loge_tru_neha",
                  labels=["Taupede", "EvtGen Thijs", "EvtGen Max", "Millipede","MillipedeTrun","RecoETot", "Monopod"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_Millipede","loge_MillipedeTrun","loge_RecoETot"], true_key = "loge_tru_tianlu",
                  labels=["Millipede","MillipedeTrun","RecoETot"], outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_mederes( data, fit_keys = ["loge_Millipede","loge_MillipedeTrun","loge_RecoETot"], true_key = "loge_tru_neha",
                  labels=["Millipede","MillipedeTrun","RecoETot"], outpath=outpath, bins = np.linspace(4,8,nbins) )


    # direction
    plot_medangres( data, fit_keys = ["Taupede","EventGeneratorDC_Thijs","EventGeneratorDC_Max","Millipede", "Monopod"], true_key="tianlu",
                   labels=["Taupede", "EvtGen Thijs", "EvtGen Max", "Millipede", "Monopod"], outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_medangres( data, fit_keys = ["Taupede","EventGeneratorDC_Thijs","EventGeneratorDC_Max","Millipede", "Monopod"], true_key="neha",
                   labels=["Taupede", "EvtGen Thijs", "EvtGen Max", "Millipede", "Monopod"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_medangres_len( data, fit_keys = ["Taupede","EventGeneratorDC_Thijs","EventGeneratorDC_Max"], true_key="tianlu",
                        labels=["Taupede", "EvtGen Thijs", "EvtGen Max"], outpath=outpath, bins = np.linspace(0, 100,15) )

    # clean plots with less lines
    # nutau
    plot_medangres( data, fit_keys = ["Taupede","EventGeneratorDC_Thijs","Millipede"], true_key="neha",
                   labels=["Taupede", "EvtGen Thijs", "Millipede"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_medangres( data, fit_keys = ["Taupede","Millipede"], true_key="neha",
                   labels=["Taupede", "Millipede"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_medangres( data, fit_keys = ["Monopod","Millipede"], true_key="neha",
                   labels=["Monopod", "Millipede"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_Taupede","loge_Millipede","loge_MillipedeTrun"], true_key = "loge_tru_neha",
                  labels=["Taupede", "Millipede","MillipedeTrun"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_Taupede","loge_Millipede","loge_RecoETot", "loge_Monopod"], true_key = "loge_tru_neha",
                  labels=["Taupede", "Millipede","RecoETot", "Monopod"], outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_mederes( data, fit_keys = ["loge_Taupede","loge_Millipede","loge_RecoETot", "loge_Monopod"], true_key = "loge_tru_tianlu",
                  labels=["Taupede", "Millipede","RecoETot", "Monopod"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    # nue
    plot_medangres( data, fit_keys = ["Taupede","Monopod","Millipede"], true_key="neha",
                   labels=["Taupede", "Monopod", "Millipede"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_Monopod","loge_Millipede","loge_MillipedeTrun"], true_key = "loge_tru_neha",
                  labels=["Monopod","Millipede","MillipedeTrun"], outpath=outpath, bins = np.linspace(4,8,nbins) )


def compare_evtgen( nufiles, labels, outpath ):
    print("compare")

    os.system(f"mkdir -p {outpath}")

    # get the data
    data = []
    for nufile in nufiles: data += [ extract_data_combined(nufile) ]

    print("Datasets with", [len(dataset) for dataset in data])

    nbins = 20

    # length
    plot_lenres_len( data, fit_keys = ["len_Taupede","len_EventGeneratorDC_Thijs","len_EventGeneratorDC_Max","len_EventGeneratorDC_Combined"], 
                     true_key = "len_tru_tianlu",labels = labels, outpath=outpath, bins = np.linspace(0, 100,30) )
    plot_lenres_len( data, fit_keys = ["len_Taupede","len_EventGeneratorDC_Thijs","len_EventGeneratorDC_Max","len_EventGeneratorDC_Combined"], 
                     true_key = "len_tru_neha",labels = labels, outpath=outpath, bins = np.linspace(0, 100,30) )

    plot_len_fit( data, fit_keys = ["len_Taupede","len_EventGeneratorDC_Thijs","len_EventGeneratorDC_Max","len_EventGeneratorDC_Combined"], 
                  labels=labels, outpath=outpath, bins = np.linspace(0, 100,nbins ) )

    # energy asymmetry
    plot_medasmres_len( data, fit_keys = ["asm_Taupede","asm_EventGeneratorDC_Thijs","asm_EventGeneratorDC_Max","asm_EventGeneratorDC_Combined"], 
                        asm_true_key = "asm_tru_tianlu", len_tru_key="len_tru_tianlu",labels=labels, outpath=outpath, bins = np.linspace(0, 100,nbins) )
    plot_medasmres_len( data, fit_keys = ["asm_Taupede","asm_EventGeneratorDC_Thijs","asm_EventGeneratorDC_Max","asm_EventGeneratorDC_Combined"], 
                        asm_true_key = "asm_tru_tianlu", len_tru_key="len_tru_neha",labels=labels, outpath=outpath, bins = np.linspace(0, 100,nbins) )

    # energy
    plot_mederes( data, fit_keys = ["loge_Taupede","loge_EventGeneratorDC_Thijs","loge_EventGeneratorDC_Max","loge_EventGeneratorDC_Combined"], 
                  true_key = "loge_tru_tianlu",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_mederes( data, fit_keys = ["loge_Taupede","loge_EventGeneratorDC_Thijs","loge_EventGeneratorDC_Max","loge_EventGeneratorDC_Combined"], 
                  true_key = "loge_tru_neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_Monopod","loge_EventGeneratorDC_Thijs","loge_EventGeneratorDC_Max","loge_EventGeneratorDC_Combined"], 
                  true_key = "loge_tru_tianlu",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_mederes( data, fit_keys = ["loge_Monopod","loge_EventGeneratorDC_Thijs","loge_EventGeneratorDC_Max","loge_EventGeneratorDC_Combined"], 
                  true_key = "loge_tru_neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )

    # direction
    plot_medangres( data, fit_keys = ["Taupede","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                   true_key="tianlu",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_medangres( data, fit_keys = ["Taupede","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                   true_key="neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_medangres( data, fit_keys = ["Monopod","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                   true_key="tianlu",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_medangres( data, fit_keys = ["Monopod","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                   true_key="neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_medangres( data, fit_keys = ["SPEFit16","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                   true_key="tianlu",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )
    plot_medangres( data, fit_keys = ["SPEFit16","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                   true_key="neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_medangres_len( data, fit_keys = ["Taupede","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                        true_key="tianlu",labels=labels, outpath=outpath, bins = np.linspace(0, 100,15) )
    plot_medangres_len( data, fit_keys = ["Taupede","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                        true_key="neha",labels=labels, outpath=outpath, bins = np.linspace(0, 100,15) )

def compare_evtgen_clean( nufiles, labels, outpath ):
    print("compare")

    os.system(f"mkdir -p {outpath}")

    # get the data
    data = []
    for nufile in nufiles: data += [ extract_data_combined(nufile) ]

    print("Datasets with", [len(dataset) for dataset in data])

    nbins = 20

    # length
    plot_lenres_len( data, fit_keys = ["len_Taupede","len_EventGeneratorDC_Thijs","len_EventGeneratorDC_Max","len_EventGeneratorDC_Combined"], 
                     true_key = "len_tru_tianlu",labels = labels, outpath=outpath, bins = np.linspace(0, 100,30), plot_quartiles=False )

    plot_len_fit( data, fit_keys = ["len_Taupede","len_EventGeneratorDC_Thijs","len_EventGeneratorDC_Max","len_EventGeneratorDC_Combined"], 
                  labels=labels, outpath=outpath, bins = np.linspace(0, 100,nbins ) )

    # # energy asymmetry
    plot_medasmres_len( data, fit_keys = ["asm_Taupede","asm_EventGeneratorDC_Thijs","asm_EventGeneratorDC_Max","asm_EventGeneratorDC_Combined"], 
                        asm_true_key = "asm_tru_tianlu", len_tru_key="len_tru_tianlu",labels=labels, outpath=outpath, bins = np.linspace(0, 100,nbins), plot_quartiles=False )

    # energy
    plot_mederes( data, fit_keys = ["loge_Taupede","loge_EventGeneratorDC_Thijs","loge_EventGeneratorDC_Max","loge_EventGeneratorDC_Combined"], 
                  true_key = "loge_tru_neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins), plot_quartiles=True )

    plot_mederes( data, fit_keys = ["loge_Monopod","loge_EventGeneratorDC_Thijs","loge_EventGeneratorDC_Max","loge_EventGeneratorDC_Combined"], 
                  true_key = "loge_tru_neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins), plot_quartiles=True )

    # direction
    plot_medangres( data, fit_keys = ["Taupede","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                   true_key="neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins), plot_quartiles=False )

    plot_medangres( data, fit_keys = ["Monopod","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                   true_key="neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins), plot_quartiles=False )

    plot_medangres( data, fit_keys = ["SPEFit16","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                   true_key="neha",labels=labels, outpath=outpath, bins = np.linspace(4,8,nbins), plot_quartiles=False )

    plot_medangres_len( data, fit_keys = ["Taupede","EventGeneratorDC_Thijs","EventGeneratorDC_Max","EventGeneratorDC_Combined"], 
                        true_key="tianlu",labels=labels, outpath=outpath, bins = np.linspace(0, 100,15), plot_quartiles=False )


###
### NuTau
###

nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/taureco_iceprod_benchmark/HESE_evtgen_NuTau.h5"]
outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/taureco_iceprod_benchmark/HESE_evtgen_NuTau"
compare(nufiles=nufiles,outpath=outpath)

# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuTau.h5",
#            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuTau.h5",
#            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuTau.h5",
#            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuTau.h5"]
# labels = ["Taupede", "EvtGen Thijs", "EvtGen Max", "EvtGen Combined"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/evtgen_v4_rec_v9/NuTau_EvtGen"
# compare_evtgen(nufiles=nufiles, labels = labels,outpath=outpath)

# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuTau.h5",
#            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuTau.h5",
#            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuTau.h5",
#            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuTau.h5"]
# labels = ["Taupede", "EvtGen Thijs", "EvtGen Max", "EvtGen Combined"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/evtgen_v4_rec_v9/NuTau_EvtGen_clean"
# compare_evtgen_clean(nufiles=nufiles, labels = labels,outpath=outpath)

###
### NuE
###

# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuE.h5"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/evtgen_v4_rec_v9/NuE"
# compare(nufiles=nufiles,outpath=outpath)


# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuE.h5",
#            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuE.h5",
#            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuE.h5",
#            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuE.h5"]
# labels = ["Taupede", "EvtGen Thijs", "EvtGen Max", "EvtGen Combined"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/evtgen_v4_rec_v9/NuE_EvtGen"
# compare_evtgen(nufiles=nufiles, labels = labels,outpath=outpath)

# ###
# ### NuMu
# ###

# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuMu.h5"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/evtgen_v4_rec_v9/NuMu"
# compare(nufiles=nufiles,outpath=outpath)

# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuMu.h5",
#            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuMu.h5",
#            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuMu.h5",
#            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuMu.h5"]
# labels = ["Taupede", "EvtGen Thijs", "EvtGen Max", "EvtGen Combined"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/evtgen_v4_rec_v9/NuMu_EvtGen"
# compare_evtgen(nufiles=nufiles, labels = labels,outpath=outpath)

