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


def plot_mederes(data, fit_keys, true_key, labels, outpath, bins = np.linspace(1, np.linspace(1, 7, 39)[26]+3, 46)):
    
    print("plot_mederes")

    plt.figure(figsize=(6, 4))

    for i, label in enumerate(labels):
        loge_fit = data[i][fit_keys[i]]
        loge_tru = data[i][true_key]
        
        plot_quartiles_vs_x((10**(loge_fit)-10**(loge_tru))/10**(loge_tru),
                            loge_tru,
                            bins,
                            label)
        plt.axhline(0, linewidth=0.5, color='gray', linestyle='--')
        plt.xlabel(r'$\log_{10}(E_{dep}$ [GeV]$)$')
        plt.ylabel('$(E_{rec}-E_{dep})/E_{dep}$')
        plt.ylim(-0.2, 0.2)
        plt.legend()

    plt.savefig(f'{outpath}/mederes_{"-".join(fit_keys)}_vs_{true_key}.png', bbox_inches='tight')
    plt.clf()


def plot_medangres(data, fit_keys,true_key,labels, outpath, bins = np.linspace(1, np.linspace(1, 7, 39)[26]+3, 46)):
    
    print("plot_medangres")

    plt.figure(figsize=(6, 4))

    meanmed = []
    for i, label in enumerate(labels):
        reco_zen = np.arccos(data[i][f"cth_{fit_keys[i]}"])
        reco_azi = data[i][f"azi_{fit_keys[i]}"]
        cth_tru = data[i][f"cth_tru_{true_key}"]
        azi_tru = data[i][f"azi_tru_{true_key}"]
        loge_tru = data[i][f"loge_tru_{true_key}"]
        cas = np.degrees(calculator.center_angle(
            np.arccos(cth_tru), azi_tru,
            reco_zen, reco_azi))
        _, per50, _ = plot_quartiles_vs_x(cas, loge_tru, bins, label)
        meanmed.append(np.nanmean(per50))

    yup = 20
    ylo = 0
    ysc = 'linear'

    plt.xlabel(rf'$\log_{{10}}(E_{{dep}}$ [GeV]$)$')
    plt.ylabel('Median angular resolution [deg.]')
    plt.ylim(ylo, yup)
    plt.yscale(ysc)
    plt.legend()
    plt.savefig(f'{outpath}/medangres_{"-".join(fit_keys)}_vs_{true_key}.png', bbox_inches='tight')
    plt.clf()

def plot_medangres_len(data, fit_keys, true_key, labels, outpath, bins = np.linspace(0,100, 40) ):

    print("plot_medangres_len")
    
    plt.figure(figsize=(6, 4))
    
    meanmed = []
    for i, label in enumerate(labels):
        reco_zen = np.arccos(data[i][f"cth_{fit_keys[i]}"])
        reco_azi = data[i][f"azi_{fit_keys[i]}"]
        cth_tru = data[i][f"cth_tru_{true_key}"]
        azi_tru = data[i][f"azi_tru_{true_key}"]
        len_tru = data[i][f"len_tru_{true_key}"]
        cas = np.degrees(calculator.center_angle(
            np.arccos(cth_tru), azi_tru,
            reco_zen, reco_azi))

        _, per50, _ = plot_quartiles_vs_x(cas, len_tru, bins, label)
        meanmed.append(np.nanmean(per50))

    yup = 10
    ylo = 0
    ysc = 'linear'

    xlo = 3
    plt.xlabel(r'True length [m]')
    plt.ylabel('Median angular resolution [deg.]')
    plt.ylim(ylo, yup)
    plt.yscale(ysc)
    plt.xlim(xmin=xlo)
    plt.legend()
    plt.savefig(f'{outpath}/medangres_len_{"-".join(fit_keys)}_vs_{true_key}.png', bbox_inches='tight')

    plt.clf()

def plot_len_fit(data, fit_keys,labels, outpath, bins = np.linspace(0,100, 40) ):
    plt.figure(figsize=(6, 4))

    for i, label in enumerate(labels):
        plt.hist(data[i][fit_keys[i]], bins=bins, density=True,
                 histtype='step', label=label, linewidth=1.5)

    plt.xlabel(r'Length [m]')
    plt.ylabel('Normalized count')
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(f'{outpath}/{"-".join(fit_keys)}.png', bbox_inches='tight')
    plt.clf()

def plot_lenres_len( data, fit_keys, true_key, labels, outpath, bins = np.linspace(0, 100,35) ):

    plt.figure()
    for i, label in enumerate(labels):
        plot_quartiles_vs_x( (data[i][fit_keys[i]] - data[i][true_key]) / data[i][true_key],
                              data[i][true_key],
                              bins,
                              labels[i])
    plt.xlabel(r'Length [m]')
    plt.ylabel('$(L_{rec}-L_{true})/L_{true}$')
    plt.axhline(0, linewidth=0.5, color='gray', linestyle='--')
    plt.xlim(0, 50)
    plt.ylim(-0.5, 0.5)
    plt.legend()
    plt.savefig(f'{outpath}/medlenres_{"-".join(fit_keys)}_vs_{true_key}.png', bbox_inches='tight')
    plt.clf()

def plot_medasmres_len( data, fit_keys, asm_true_key, len_tru_key, labels, outpath, bins = np.linspace(0, 100,35) ):

    plt.figure()
    for i, label in enumerate(labels):
        plot_quartiles_vs_x(data[i][fit_keys[i]] - data[i][asm_true_key],
                            data[i][len_tru_key],
                            bins,
                            labels[i])
    plt.xlabel(r'Length [m]')
    plt.ylabel('$A_{rec}-A_{true}$')
    plt.axhline(0, linewidth=0.5, color='gray', linestyle='--')
    plt.xlim(0, 50)
    plt.ylim(-0.5, 0.5)
    plt.legend()
    plt.savefig(f'{outpath}/medasmres_len_{"-".join(fit_keys)}_{asm_true_key}_vs_{len_tru_key}.png', bbox_inches='tight')


def compare_files( nufiles, keys, labels, outpath ):
    print("compare")

    os.system(f"mkdir -p {outpath}")

    # get the data
    data = []
    for (nufile, key) in zip(nufiles, keys):
        if "EventGenerator" in key:
            data += [extract_data_evtgen(nufile, key)]
        else: data += [ extract_data(nufile, key) ]

    print("Datasets with", [len(dataset) for dataset in data])

    plot_lenres_len( data, labels, outpath )
    plot_medasmres_len( data, labels, outpath )
    plot_len_fit( data, labels, outpath )
    plot_medangres( data, labels, outpath )
    plot_medangres_len( data, labels, outpath )
    plot_mederes( data, labels, outpath )


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



    ###
    ### compare v1 with spice
    ###
    # nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuTau.h5", "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1/NuTau.h5"]
    # keys = ["HESETaupedeFit", "TaupedeFit_iMIGRAD_PPB0"] 
    # labels = ["spice_tau_reco", "v1"]
    # outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/compare/spice_tau_reco_vs_v1/NuTau"
    # compare_files(nufiles=nufiles, keys=keys, labels = labels,outpath=outpath)

    ###
    ### compare v1 with bright
    ###
    # nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1/NuTau.h5", "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/rec_v1_bright/NuTau.h5"]
    # keys = ["TaupedeFit_iMIGRAD_PPB0", "TaupedeFit_iMIGRAD_PPB0_bright"] 
    # labels = ["v1 reco", "with bright"]
    # outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/compare/bright/"
    # compare_files(nufiles=nufiles, keys=keys, labels = labels,outpath=outpath)

    ###
    ### compare v1 with bright
    ###    
    # nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1/NuTau.h5", 
    #            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v0_rec_v1/NuTau.h5",
    #            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v0_rec_v1/NuTau.h5"]
    # keys = ["TaupedeFit_iMIGRAD_PPB0", 
    #         "EventGeneratorDC_Max",
    #         "EventGeneratorDC_Thijs"] 
    # labels = ["v1 reco", "EvtGen Max", "EvtGen Thijs"]
    # outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/compare/evtgen_v0_rec_v1/"
    # compare_files(nufiles=nufiles, keys=keys, labels = labels,outpath=outpath)

    # ###
    # ### compare v2 with spice
    # ###
    # nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuTau.h5", "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v2/NuTau.h5"]
    # keys = ["HESETaupedeFit", "TaupedeFit_iMIGRAD_PPB0"] 
    # labels = ["spice_tau_reco", "v2"]
    # outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/compare/spice_tau_reco_vs_v2/NuTau"
    # compare_files(nufiles=nufiles, keys=keys, labels = labels,outpath=outpath)

    # nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuE.h5", "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v2/NuE.h5"]
    # keys = ["HESETaupedeFit", "TaupedeFit_iMIGRAD_PPB0"] 
    # labels = ["spice_tau_reco", "v2"]
    # outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/compare/spice_tau_reco_vs_v2/NuE"
    # compare_files(nufiles=nufiles, keys=keys, labels = labels,outpath=outpath)

    # ###
    # ### Compare v1 with v2
    # ### 
    # nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1/NuTau.h5", "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v2/NuTau.h5"]
    # keys = ["TaupedeFit_iMIGRAD_PPB0", "TaupedeFit_iMIGRAD_PPB0"] 
    # labels = ["v1", "v2"]
    # outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/compare/v1_vs_v2"
    # compare_files(nufiles=nufiles, keys=keys, labels = labels,outpath=outpath)


    # ###
    # ### compare v1 with bright
    # ###    
    # nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v1_rec_v2/NuTau.h5", 
    #            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v1_rec_v2/NuTau.h5",
    #            "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v1_rec_v2/NuTau.h5"]
    # keys = ["TaupedeFit_iMIGRAD_PPB0", 
    #         "EventGeneratorDC_Max",
    #         "EventGeneratorDC_Thijs"] 
    # labels = ["v2 reco", "EvtGen Max", "EvtGen Thijs"]
    # outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/compare/evtgen_v1_rec_v2/"
    # compare_files(nufiles=nufiles, keys=keys, labels = labels,outpath=outpath)


    ###
    ### Compare v1 with v2
    ### 
    nufiles = ["/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1/NuTau.h5", "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v2/NuTau.h5"]
    keys = ["TaupedeFit_iMIGRAD_PPB0", "TaupedeFit_iMIGRAD_PPB0"] 
    labels = ["v1", "v2"]
    outpath = "/data/user/tvaneede/GlobalFit/reco_processing/performance/plots/compare/v1_vs_v2"
    compare_files(nufiles=nufiles, keys=keys, labels = labels,outpath=outpath)
