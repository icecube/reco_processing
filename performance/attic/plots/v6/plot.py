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
    for nufile in nufiles*10: data += [ extract_data_combined(nufile) ]

    print("Datasets with", [len(dataset) for dataset in data])

    nbins = 20

    plot_mederes( data, fit_keys = ["loge_Taupede","loge_Millipede","loge_MillipedeTrun"], true_key = "loge_tru_neha",
                  labels=["Taupede", "Millipede","MillipedeTrun"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_Taupede","loge_MonoMillipede","loge_MonoMillipedeTrun"], true_key = "loge_tru_neha",
                  labels=["Taupede", "MonoMillipede","MonoMillipedeTrun"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_Taupede","loge_TauMillipede","loge_TauMillipedeTrun"], true_key = "loge_tru_neha",
                  labels=["Taupede", "TauMillipede","TauMillipedeTrun"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_Taupede","loge_SPEMillipede","loge_SPEMillipedeTrun"], true_key = "loge_tru_neha",
                  labels=["Taupede", "SPEMillipede","SPEMillipedeTrun"], outpath=outpath, bins = np.linspace(4,8,nbins) )

    plot_mederes( data, fit_keys = ["loge_Millipede","loge_MillipedeTrun", "loge_MonoMillipede","loge_MonoMillipedeTrun", "loge_SPEMillipede","loge_SPEMillipedeTrun", "loge_TauMillipede","loge_TauMillipedeTrun"], true_key = "loge_tru_neha",
                  labels=["Millipede","MillipedeTrun","MonoMillipede","MonoMillipedeTrun","SPEMillipede","SPEMillipedeTrun","TauMillipede","TauMillipedeTrun"], outpath=outpath, bins = np.linspace(4,8,nbins) )



###
### NuTau
###

nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v6/NuTau.h5"]
outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/v6/NuTau"
compare(nufiles=nufiles,outpath=outpath)

###
### NuE
###

# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuE.h5"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/spice_tau_reco/NuE"
# compare(nufiles=nufiles,outpath=outpath)

###
### NuMu
###

# nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuMu.h5"]
# outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/spice_tau_reco/NuMu"
# compare(nufiles=nufiles,outpath=outpath)
