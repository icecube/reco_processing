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


def extract_data_combined(nufile):
    tf = tables.open_file(nufile)
    data = {}

    is_ftp = False if "spice" in nufile else True
    is_evtgen = True if "evtgen" in nufile else False

    print(20*"-")
    print("Opening", nufile, "is_ftp", is_ftp)

    # Choose Taupede and Monopod keys based on format
    taupede_key = "TaupedeFit_iMIGRAD_PPB0" if is_ftp else "HESETaupedeFit"
    monopod_key = "MonopodFit_iMIGRAD_PPB0" if is_ftp else "HESEMonopodFit"

    # Taupede reconstruction
    data["cth_Taupede"] = np.cos(tf.get_node(f'/{taupede_key}').cols.zenith[:][slc])
    data["azi_Taupede"] = tf.get_node(f'/{taupede_key}').cols.azimuth[:][slc]
    data["loge_Taupede"] = np.log10(tf.get_node(f'/{taupede_key}').cols.energy[:][slc])
    data["len_Taupede"] = tf.get_node(f'/{taupede_key}').cols.length[:][slc]
    data["asm_Taupede"] = get_easymm(tf.get_node(f'/{taupede_key}Particles'))[slc]

    # Monopod
    data["cth_Monopod"] = np.cos(tf.get_node(f'/{monopod_key}').cols.zenith[:][slc])
    data["azi_Monopod"] = tf.get_node(f'/{monopod_key}').cols.azimuth[:][slc]
    data["loge_Monopod"] = np.log10(tf.get_node(f'/{monopod_key}').cols.energy[:][slc])

    # SPEFit (same in both cases)
    key = "SPEFit16"
    data["cth_SPEFit16"] = np.cos(tf.get_node(f'/{key}').cols.zenith[:][slc])
    data["azi_SPEFit16"] = tf.get_node(f'/{key}').cols.azimuth[:][slc]
    data["loge_SPEFit16"] = np.log10(tf.get_node(f'/{key}').cols.energy[:][slc])

    # EventGenerator only for FTP
    if is_evtgen:
        for key in ["EventGeneratorDC_Thijs", "EventGeneratorDC_Max"]:
            data[f"len_{key}"] = np.abs(tf.get_node(f'/{key}').cols.cascade_cascade_00001_distance[:][slc])
            data[f"asm_{key}"] = get_easymm_evtgen(tf.get_node(f'/{key}'))[slc]
            data[f"cth_{key}"] = np.cos(tf.get_node(f'/{key}').cols.cascade_zenith[:][slc])
            data[f"azi_{key}"] = tf.get_node(f'/{key}').cols.cascade_azimuth[:][slc]
            data[f"loge_{key}"] = np.log10(tf.get_node(f'/{key}').cols.cascade_energy[:][slc] + 
                                           tf.get_node(f'/{key}').cols.cascade_cascade_00001_energy[:][slc])

    # Millipede reconstructions
    key = "HESEMillipedeFit"
    data["cth_Millipede"] = np.cos(tf.get_node(f'/{key}').cols.zenith[:][slc])
    data["azi_Millipede"] = tf.get_node(f'/{key}').cols.azimuth[:][slc]
    data["loge_Millipede"] = np.log10(tf.root.HESEMillipedeFitDepositedEnergy[slc]['value'])
    data["loge_MillipedeTrun"] = np.log10(tf.root.HESEMillipedeFitTruncatedDepositedEnergy[slc]['value'])

    # extra millipede stuff from v6
    if "v6" in nufile or "v7" in nufile:
        data["loge_MonoMillipede"] = np.log10(tf.root.MonopodFit_iMIGRAD_PPB0MillipedeFitDepositedEnergy[slc]['value'])
        data["loge_MonoMillipedeTrun"] = np.log10(tf.root.MonopodFit_iMIGRAD_PPB0MillipedeFitTruncatedDepositedEnergy[slc]['value'])
        data["loge_SPEMillipede"] = np.log10(tf.root.SPEFit16MillipedeFitDepositedEnergy[slc]['value'])
        data["loge_SPEMillipedeTrun"] = np.log10(tf.root.SPEFit16MillipedeFitTruncatedDepositedEnergy[slc]['value'])
        data["loge_TauMillipede"] = np.log10(tf.root.TaupedeFit_iMIGRAD_PPB0MillipedeFitDepositedEnergy[slc]['value'])
        data["loge_TauMillipedeTrun"] = np.log10(tf.root.TaupedeFit_iMIGRAD_PPB0MillipedeFitTruncatedDepositedEnergy[slc]['value'])


    # Reco information neha
    data["loge_RecoETot"] = np.log10(tf.root.RecoETot[slc]['value'])

    # True information (Tianlu)
    data["cth_tru_tianlu"] = np.cos(tf.root.cc.cols.zenith[:][slc])
    data["azi_tru_tianlu"] = tf.root.cc.cols.azimuth[:][slc]
    data["loge_tru_tianlu"] = np.log10(tf.root.cc.cols.energy[:][slc])
    data["asm_tru_tianlu"] = tf.root.cc_easymm[slc]['value']
    data["len_tru_tianlu"] = tf.root.cc.cols.length[:][slc]

    # True information (Neha)
    data["cth_tru_neha"] = np.cos(tf.root.TrueZenith[slc]['value'])
    data["azi_tru_neha"] = tf.root.TrueAzimuth[slc]['value']
    data["loge_tru_neha"] = np.log10(tf.root.TrueETot[slc]['value'])
    data["asm_tru_neha"] = tf.root.TrueERatio[slc]['value']
    data["len_tru_neha"] = tf.root.TrueL[slc]['value']

    tf.close()
    print(f"dataset {nufile} has {len(data['cth_tru_tianlu'])} evts")

    return data
