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


logging.getLogger('matplotlib.font_manager').disabled = True

knots_mie = np.arange(5.261904764, 180, 10)
knots_lea = np.arange(4.761904761904762, 180, 10)
knots_std = np.arange(2.5, 180, 5)


def get_legend(node_name):
    """ Legend for secondary line
    """
    dd = {'EMC': 'EMC',
          'MonopodFit_MIGRAD_KB': 'Brights only',
          'Millipede2ndPass': 'Scan @ true dir',
          'Millipede3rdPass': 'Seed @ true dir + iter. fit',
          'cc': 'Truth',
          'EventGenerator_cascade_7param_noise_tw_BFRv1Spice321_01_I3Particle': 'EventGenerator orig.',
          'MonopodFit_SIMPLEX': 'Monopod (SIMPLEX)',
          'MonopodFit_MIGRAD': 'Monopod (MIGRAD)',
          'MonopodFit_iMIGRAD_PPB0': 'Monopod (iMIGRAD)',
          'MonopodFit_iMIGRAD_PPB0_t': 'No time mod.',
          'MonopodFit_iMIGRAD_PPB0_bulk': 'No tilt or anisotropy correction',
          'MonopodFit_iMIGRAD_PPB0_flat': 'No tilt correction',
          'MonopodFit_iMIGRAD_PPB0_mie': 'Old reco.',
          'MonopodFit_iMIGRAD_PPB0_lea': 'Lea reco.',
          'MonopodFit_iMIGRAD_PPB0_p13p20': 'Reco. (p1=0.3, p2=0)',
          'MonopodFit_iMIGRAD_PPB0_p135p20': 'Reco. (p1=0.35, p2=0)',
          'MonopodFit_iMIGRAD_PPB0_bfrv2': 'Bfrv2 reco.',
          'MonopodFit_iMIGRAD_BS1': 'w. bright DOMs',
          'MonopodFit_iMIGRAD_BS1SeedBF': 'w/o bright DOMs',
          'EventGenerator_cascade_7param_noise_ftpv3m__big_model_01_I3Particle': 'EGen v2 (ftpv3m big)'}
    return dd.get(node_name, node_name.replace('_', '.'))


def alt_node_name(fname):
    """ h5 node name for secondary line
    """
    dd = defaultdict(lambda: 'MonopodFit_iMIGRAD_PPB0')
    dd.update({'emc.h5': 'EMC',
               'skymap_test.h5': 'SPEFit16',
               'cascades.30TeV.h5': 'cscdSBU_MonopodFit4',
               # 'a.h5': 'HESETaupedeFit',
               # 'a.h5': 'EventGenerator_cascade_7param_noise_ftpv3m__big_model_01_I3Particle',
               'a.h5': 'EventGeneratorSelectedRecoNN_I3Particle',
               # 'a.h5': 'DNNC_I3Particle',
               'b.h5': 'MonopodFit_iMIGRAD_PPB0',
               # 'x.h5': 'EventGeneratorFit_I3Particle',
               'x.h5': 'Taupede_spice3',
               'dnncv1.h5': 'EventGeneratorSelectedRecoNN_I3Particle',
               'ftpv1.compare.bdthres15.h5': 'MonopodFit_iMIGRAD_PPB0_mie',
               'ftpv1.vs.mie.h5': 'MonopodFit_iMIGRAD_PPB0_mie',
               'ftpv1.imigrad.tau.bdthres15.h5': 'MonopodFit_iMIGRAD_PPB0',
               'ftpv1.imigrad.tau.idc.bdthres15.h5': 'MonopodFit_iMIGRAD_PPB0',
               'usetables.ftpv1.h5': 'MonopodFit_iMIGRAD_PPB0',
               'usetables.bfrv2.ideal.h5': 'MonopodFit_iMIGRAD_BS1SeedBF',
               'usetables.bfrv2.halfdense.3x.ideal.h5': 'MonopodFit_iMIGRAD_BS1SeedBF',
               'usetables.bfrv2.relerr0.05.h5': 'cc',
               'usetables.bfrv2.ibr.relerr0.05.h5': 'cc',
               'usetables.bfrv2.halfdense.relerr0.05.h5': 'cc',
               'usetables.bfrv2.halfdense.domeff3.relerr0.05.h5': 'cc',
               'usetables.bfrv2.halfdense.domeff5.relerr0.05.h5': 'cc',
               'usetables.bfrv2.halfdense.domeff10.relerr0.05.h5': 'cc',
               'usetables.bfrv2.halfdense.ibr.relerr0.05.h5': 'cc',
               'bfrv2.relerr0.05.effdz10.h5': 'MonopodFit_iMIGRAD_PPB0_b',
               'bfrv2flat.relerr0.05.h5': 'cc',
               'bfrv2tilt.relerr0.05.h5': 'cc',
               'bfrv2.mie.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0_mie',
               'bfrv2.relerr0.05.egen.h5': 'EveGenFit_I3Particle',
               'bfrv2.relerr0.05.egen.oldwavecal.h5': 'EveGenFit_I3Particle',
               'bfrv2.relerr0.05.egen.oldwavecal.bfrv1set0.h5': 'EveGenFit_I3Particle',
               'bfrv2.relerr0.05.bfrv2p10.3p20.h5': 'CombinedCascadeSeed_L3',
               'bfrv2.relerr0.05.bfrv2p10.3p2-1.h5': 'CombinedCascadeSeed_L3',
               'bfrv2.relerr0.05.bfrv2p10.3p2+1.h5': 'CombinedCascadeSeed_L3',
               'bfrv2.relerr0.05.bfrv2p10.3p2-2.h5': 'CombinedCascadeSeed_L3',
               'bfrv2.relerr0.05.bfrv2p10.3p2-3.h5': 'CombinedCascadeSeed_L3',
               'inel.h5': 'MonopodFit_iMIGRAD_PPB0_d'})
    return dd[fname]


def fit_node_name(fname):
    """ h5 node name for primary line
    """
    dd = defaultdict(lambda: 'TaupedeFit_iMIGRAD_PPB0')
    dd.update({'skymap_test.h5': 'Millipede3rdPass',
               'cascades.30TeV.h5': 'MonopodFit_iMIGRAD_PPB0',
               'a.h5': 'TaupedeFit_iMIGRAD_PPB0',
               'b.h5': 'PreferredFit',
               'x.h5': 'TaupedeFit_iMIGRAD',
               'dnncv1.h5': 'EventGeneratorSelectedRecoNN_I3Particle',
               'ftpv1.compare.bdthres15.h5': 'MonopodFit_iMIGRAD_PPB0',
               'ftpv1.vs.mie.h5': 'MonopodFit_iMIGRAD_PPB0',
               'ftpv1.imigrad.tau.bdthres15.h5': 'PreferredFit',
               'ftpv1.imigrad.tau.idc.bdthres15.h5': 'PreferredFit',
               'usetables.ftpv1.h5': 'PreferredFit',
               'usetables.bfrv2.ideal.h5': 'MonopodFit_iMIGRAD_BS1',
               'usetables.bfrv2.halfdense.3x.ideal.h5': 'MonopodFit_iMIGRAD_BS1',
               'usetables.bfrv2.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'usetables.bfrv2.ibr.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'usetables.bfrv2.halfdense.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'usetables.bfrv2.halfdense.domeff3.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'usetables.bfrv2.halfdense.domeff5.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'usetables.bfrv2.halfdense.domeff10.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'usetables.bfrv2.halfdense.ibr.relerr0.05.h5': 'MonopodFit_iMIGRAD_',
               'bfrv2.relerr0.05.effdz10.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2flat.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2tilt.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.mie.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.relerr0.05.egen.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.relerr0.05.egen.oldwavecal.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.relerr0.05.egen.oldwavecal.bfrv1set0.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.relerr0.05.bfrv2p10.3p20.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.relerr0.05.bfrv2p10.3p2-1.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.relerr0.05.bfrv2p10.3p2+1.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.relerr0.05.bfrv2p10.3p2-2.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.relerr0.05.bfrv2p10.3p2-3.h5': 'MonopodFit_iMIGRAD_PPB0',
               'inel.h5': 'MonopodFit_iMIGRAD_PPB0_a'})
    return dd[fname]

def fit_node_name_neha(fname):
    """ h5 node name for primary line
    """
    dd = defaultdict(lambda: 'HESETaupedeFit')
    dd.update({'skymap_test.h5': 'Millipede3rdPass',
               'cascades.30TeV.h5': 'MonopodFit_iMIGRAD_PPB0',
               'a.h5': 'TaupedeFit_iMIGRAD_PPB0',
               'b.h5': 'PreferredFit',
               'x.h5': 'TaupedeFit_iMIGRAD',
               'dnncv1.h5': 'EventGeneratorSelectedRecoNN_I3Particle',
               'ftpv1.compare.bdthres15.h5': 'MonopodFit_iMIGRAD_PPB0',
               'ftpv1.vs.mie.h5': 'MonopodFit_iMIGRAD_PPB0',
               'ftpv1.imigrad.tau.bdthres15.h5': 'PreferredFit',
               'ftpv1.imigrad.tau.idc.bdthres15.h5': 'PreferredFit',
               'usetables.ftpv1.h5': 'PreferredFit',
               'usetables.bfrv2.ideal.h5': 'MonopodFit_iMIGRAD_BS1',
               'usetables.bfrv2.halfdense.3x.ideal.h5': 'MonopodFit_iMIGRAD_BS1',
               'usetables.bfrv2.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'usetables.bfrv2.ibr.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'usetables.bfrv2.halfdense.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'usetables.bfrv2.halfdense.domeff3.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'usetables.bfrv2.halfdense.domeff5.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'usetables.bfrv2.halfdense.domeff10.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'usetables.bfrv2.halfdense.ibr.relerr0.05.h5': 'MonopodFit_iMIGRAD_',
               'bfrv2.relerr0.05.effdz10.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2flat.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2tilt.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.mie.relerr0.05.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.relerr0.05.egen.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.relerr0.05.egen.oldwavecal.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.relerr0.05.egen.oldwavecal.bfrv1set0.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.relerr0.05.bfrv2p10.3p20.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.relerr0.05.bfrv2p10.3p2-1.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.relerr0.05.bfrv2p10.3p2+1.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.relerr0.05.bfrv2p10.3p2-2.h5': 'MonopodFit_iMIGRAD_PPB0',
               'bfrv2.relerr0.05.bfrv2p10.3p2-3.h5': 'MonopodFit_iMIGRAD_PPB0',
               'inel.h5': 'MonopodFit_iMIGRAD_PPB0_a'})
    return dd[fname]

def yscale(norm):
    return 'log' if isinstance(norm, SymLogNorm) or isinstance(norm, LogNorm) else 'linear'


def project_vtx_dir(reco, true, true_zen, true_azi):
    """ Computes the longitudinal and transverse distance between true and reco vertex, along the true direction
    """
    direction = -np.asarray(calculator.sphe_to_cart(1, true_zen, true_azi))
    l = np.sum((reco-true)*direction, axis=0)
    r = np.linalg.norm(reco-true, axis=0)
    rho = np.sqrt(r**2-l**2)
    return l, rho, r


def plot_quartiles_vs_x(deltas, lge_tru, lge_bins, label):
    if np.any(np.isnan(deltas)):
        print(
            f'WARN: {len(deltas[np.isnan(deltas)])} nan events. Ignored in quartiles.')
    lge_i = np.digitize(lge_tru, lge_bins)
    digitized_deltas = [deltas[lge_i == ei] for ei in range(1, lge_bins.size)]

    per50 = [np.nanmedian(ca) for ca in digitized_deltas]
    per25 = [np.nanpercentile(ca, 25) if len(
        ca) > 0 else np.nan for ca in digitized_deltas]
    per75 = [np.nanpercentile(ca, 75) if len(
        ca) > 0 else np.nan for ca in digitized_deltas]
    plt.plot(calculator.centers(lge_bins), per50, label=label+' quartiles')
    plt.fill_between(calculator.centers(lge_bins), per25, per75, alpha=0.5)
    return per25, per50, per75


def plot_medangres(lge_tru, lge_bins,
                   cth_md_reco, cth_em_reco,
                   azi_md_reco, azi_em_reco,
                   cth_tru, azi_tru,
                   leg, inclowe, e_xlab='dep',
                   y_up=None):
    meanmed = []
    for reco_zen, reco_azi, _label in zip([np.arccos(cth_md_reco),
                                           np.arccos(cth_em_reco)],
                                          [azi_md_reco, azi_em_reco], leg):
        cas = np.degrees(calculator.center_angle(
            np.arccos(cth_tru), azi_tru,
            reco_zen, reco_azi))
        _, per50, _ = plot_quartiles_vs_x(cas, lge_tru, lge_bins, _label)

        meanmed.append(np.nanmean(per50))
    if max(meanmed) < 2:
        yup = 4 if y_up is None else y_up
        ylo = 0.1
        ysc = 'log'
    else:
        yup = max(30, min(180, 3*max(meanmed))) if y_up is None else y_up
        ylo = 0
        ysc = 'linear'
    xlo = 2 if inclowe else 4
    plt.xlabel(rf'$\log_{{10}}(E_{{{e_xlab}}}$ [GeV]$)$')
    plt.ylabel('Median angular resolution [deg.]')
    plt.ylim(ylo, yup)
    plt.yscale(ysc)
    plt.xlim(xmin=xlo)
    plt.legend()


def plot_wilks_coverage(dlogl, **kwargs):
    probs = np.arange(0, 1.1, 0.01)
    levels = chi2.isf(1-probs, df=2)
    coverage = []
    for level in levels:
        coverage.append(len(dlogl[dlogl < level])/len(dlogl))
    plt.plot(probs, coverage, **kwargs)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xlabel('Expected')
    plt.ylabel('Actual')
    plt.legend()


def get_easymm(node):
    _es = node.cols.energy[:]
    _vs = node.cols.vector_index[:]
    _e1 = _es[_vs==0]
    _e2 = _es[_vs==1]
    return (_e1 - _e2) / (_e1 + _e2)


def lowlevel(nufile, nufilename, outpath):

    iflow = [130, 360-50]
    cth_bins = np.linspace(-1, 1, 50)
    th_bins = calculator.edges(
        np.sort(np.concatenate([calculator.edges(knots_std), knots_std])))
    th_bins = th_bins[(th_bins >= -5) & (th_bins <= 185)]
    azi_bins = np.linspace(0, 2*np.pi, 50)
    dps_bins = np.arange(0, 181)
    # lge_bins = np.linspace(3.052631578947368, 7, 26)
    # np.linspace(1, 7, 39)
    lge_bins = np.linspace(1, np.linspace(1, 7, 39)[26]+3, 46)
    lge_bins_fine = np.linspace(3.052631578947368, 7, 100)
    drl_bins = np.linspace(0, 0.5, 50)
    llh_bins = np.linspace(0, 100, 101)
    zps_bins = np.linspace(-500, 500, 100)
    vtx_bins = np.arange(-10, 60.1, 0.4)
    rho_bins = np.sqrt(np.linspace(0, 3600, 3601))
    drlogl_bins = np.arange(-16, 3, 0.2)
    len_bins = np.arange(0, 101)
    asm_bins = np.linspace(-1., 1., 101)

    with tables.open_file(nufile) as tf:
        fit = get_legend(fit_node_name(nufile))
        alt = get_legend(alt_node_name(nufile))
        slc = np.s_[:]
        try:
            if fit_node_name(nufile) == 'Millipede3rdPass':
                mtr_dlogl = 2 * \
                    (tf.root.Millipede2ndPassFitParams.cols.logl[:] -
                     tf.root.Millipede3rdPassFitParams.cols.logl[:])
                slc = (mtr_dlogl != 0)
                if np.any(~slc):
                    print(
                        f'WARN: {np.count_nonzero(~slc)} out of {len(slc)} dllh are zero, indicating fit did not improve seed')
                # slc &= (75<np.degrees(tf.root.cc.cols.zenith[:])) &(np.degrees(tf.root.cc.cols.zenith[:]) < 120)
                # print(f'INFO: bounding to zenith 75-120')
                mtr_dlogl = mtr_dlogl[slc]
                mig_rlogl = tf.root.Millipede3rdPassFitParams.cols.rlogl[:][slc]
                tru_rlogl = tf.root.Millipede2ndPassFitParams.cols.rlogl[:][slc]
            elif fit_node_name(nufile) == 'SplineMPEIC':
                mtr_dlogl = 2 * \
                    (tf.root.SplineMPEICSeedFitParams.cols.logl[:] -
                     tf.root.SplineMPEICFitParams.cols.logl[:])
                slc = (mtr_dlogl != 0)
                if np.any(~slc):
                    print(
                        f'WARN: {np.count_nonzero(~slc)} out of {len(slc)} dllh are zero, indicating fit did not improve seed')
                # slc &= (75<np.degrees(tf.root.cc.cols.zenith[:])) &(np.degrees(tf.root.cc.cols.zenith[:]) < 120)
                # print(f'INFO: bounding to zenith 75-120')
                mtr_dlogl = mtr_dlogl[slc]
                mig_rlogl = tf.root.SplineMPEICFitParams.cols.rlogl[:][slc]
                tru_rlogl = tf.root.SplineMPEICSeedFitParams.cols.rlogl[:][slc]
            else:
                mig_rlogl = tf.root.MonopodFit_MIGRADFitParams.cols.rlogl[:]
                tru_rlogl = tf.root.MonopodFit_TrueZenithFitParams.cols.rlogl[:]
                mtr_dlogl = 2 * \
                    (tf.root.MonopodFit_TrueZenithFitParams.cols.logl[:] -
                     tf.root.MonopodFit_MIGRADFitParams.cols.logl[:])

        except tables.NoSuchNodeError:
            logging.warning('rlogls not set for skymap checks')
            mig_rlogl = None
            tru_rlogl = None
            mtr_dlogl = None
        # cth_l3_reco = np.cos(
        #     tf.root.CombinedCascadeSeed_L3.cols.zenith[:][slc])
        cth_md_reco = np.cos(
            tf.get_node(f'/{fit_node_name(nufile)}').cols.zenith[:][slc])
        # cth_tz_reco = np.cos(tf.root.MonopodFit_TrueZenith.cols.zenith[:][slc])
        # cth_lb_reco = np.cos(tf.root.MonopodFit_LBFGSB.cols.zenith[:][slc])
        azi_md_reco = tf.get_node(
            f'/{fit_node_name(nufile)}').cols.azimuth[:][slc]
        # azi_tz_reco = tf.root.MonopodFit_TrueZenith.cols.azimuth[:][slc]
        # azi_lb_reco = tf.root.MonopodFit_LBFGSB.cols.azimuth[:][slc]

        contained_length = tf.root.cc_2surf.cols.value[:][slc]
        intact = tf.root.I3MCWeightDict.cols.InteractionType[:][slc]
        try:
            flavor = tf.root.I3MCWeightDict.cols.InIceNeutrinoType[:][slc]
        except AttributeError:
            logging.warning('I3MCWeightDict does not have InIceNeutrinoType, using PrimaryNeutrinoType')
            flavor = tf.root.I3MCWeightDict.cols.PrimaryNeutrinoType[:][slc]
        do_plot_drlogl = True
        try:
            rlogl_fit = tf.get_node(
                f'/{fit_node_name(nufile)}FitParams').cols.rlogl[:][slc]
            rlogl_alt = tf.get_node(
                f'/{alt_node_name(nufile)}FitParams').cols.rlogl[:][slc]
            drlogl = rlogl_fit - rlogl_alt
        except tables.NoSuchNodeError:
            logging.warning('FitParams does not exist for both fit and alt, skipping drlogl calculation')
            do_plot_drlogl = False

        asm_recs = []
        asm_labl = []
        try:
            asm_tru = tf.root.cc_easymm[slc]['value']
            tau_vis = tf.root.cc_tauvis[slc]['type']
        except tables.NoSuchNodeError:
            logging.warning('True tau decay channel or true E_asm nodes not found, is this an older h5 file?')

        try:
            asm_fit = get_easymm(tf.get_node(
                f'/{fit_node_name(nufile)}Particles'))[slc]
            asm_recs.append(asm_fit)
            asm_labl.append(fit)
        except tables.NoSuchNodeError:
            asm_fit = np.empty(cth_md_reco.shape) * np.nan
            logging.warning(f'Reco I3Particles not found for {fit}, skipping E_asm calculation')
            pass
        try:
            asm_alt = get_easymm(tf.get_node(
                f'/{alt_node_name(nufile)}Particles'))[slc]
            asm_recs.append(asm_alt)
            asm_labl.append(alt)
        except tables.NoSuchNodeError:
            asm_alt = np.empty(cth_md_reco.shape) * np.nan
            logging.warning(f'Reco I3Particles not found for {alt}, skipping E_asm calculation')
            pass

        xps_fit = tf.get_node(
            f'/{fit_node_name(nufile)}').cols.x[:][slc]
        yps_fit = tf.get_node(
            f'/{fit_node_name(nufile)}').cols.y[:][slc]
        zps_fit = tf.get_node(
            f'/{fit_node_name(nufile)}').cols.z[:][slc]
        rho_fit = np.sqrt(xps_fit**2+yps_fit**2)
        lge_fit = np.log10(tf.get_node(
            f'/{fit_node_name(nufile)}').cols.energy[:][slc])
        len_fit = tf.get_node(
            f'/{fit_node_name(nufile)}').cols.length[:][slc]

        xps_alt = tf.get_node(
            f'/{alt_node_name(nufile)}').cols.x[:][slc]
        yps_alt = tf.get_node(
            f'/{alt_node_name(nufile)}').cols.y[:][slc]
        zps_alt = tf.get_node(
            f'/{alt_node_name(nufile)}').cols.z[:][slc]
        rho_alt = np.sqrt(xps_alt**2+yps_alt**2)
        lge_alt = np.log10(tf.get_node(
            f'/{alt_node_name(nufile)}').cols.energy[:][slc])
        len_alt = tf.get_node(
            f'/{alt_node_name(nufile)}').cols.length[:][slc]

        xps_tru = tf.root.cc.cols.x[:][slc]
        yps_tru = tf.root.cc.cols.y[:][slc]
        zps_tru = tf.root.cc.cols.z[:][slc]
        rho_tru = np.sqrt(xps_tru**2+yps_tru**2)
        len_tru = tf.root.cc.cols.length[:][slc]
        # distance to closest string (dcs)
        strs = np.loadtxt('geo-f2k', skiprows=2, usecols=range(2, 7))
        strs = np.unique(
            strs[(0 < strs[:, -1]) & (strs[:, -1] < 61)][:, :2], axis=0)
        # tru
        xyst = np.asarray([xps_tru, yps_tru]).T
        dcs_tru = np.min(
            np.sqrt(
                np.sum((xyst[..., None, None]-strs[None, None, ...])**2, axis=-1)),
            axis=-1)[:, 0]
        # rec
        xysr = np.asarray([xps_fit, yps_fit]).T
        dcs_fit = np.min(
            np.sqrt(
                np.sum((xysr[..., None, None]-strs[None, None, ...])**2, axis=-1)),
            axis=-1)[:, 0]

        cth_em_reco = np.cos(tf.get_node(
            f'/{alt_node_name(nufile)}').cols.zenith[:][slc])
        azi_em_reco = tf.get_node(
            f'/{alt_node_name(nufile)}').cols.azimuth[:][slc]

        lge_tru = np.log10(tf.root.cc.cols.energy[:][slc])
        cth_tru = np.cos(tf.root.cc.cols.zenith[:][slc])
        azi_tru = tf.root.cc.cols.azimuth[:][slc]
        try:
            lge_neut = np.log10(
                tf.root.I3MCWeightDict.cols.PrimaryNeutrinoEnergy[:][slc])
            azi_neut = tf.root.I3MCWeightDict.cols.PrimaryNeutrinoAzimuth[:][slc]
            cth_neut = np.cos(
                tf.root.I3MCWeightDict.cols.PrimaryNeutrinoZenith[:][slc])
        except tables.NoSuchNodeError:
            logging.warning('I3MCWeightDict not found, cannot load PrimaryNeutrino properties')
            lge_neut = np.zeros(lge_tru.shape)
            azi_neut = np.zeros(lge_tru.shape)
            cth_neut = np.zeros(lge_tru.shape)

        inclowe = lge_tru.min() < 3.2  # processing ZZhang's cascades

        lon_vtx_fit, trv_vtx_fit, r3d_vtx_fit = project_vtx_dir(np.asarray((xps_fit, yps_fit, zps_fit)),
                                                                np.asarray(
                                                                    (xps_tru, yps_tru, zps_tru)),
                                                                np.arccos(cth_tru), azi_tru)
        lon_vtx_alt, trv_vtx_alt, r3d_vtx_alt = project_vtx_dir(np.asarray((xps_alt, yps_alt, zps_alt)),
                                                                np.asarray(
                                                                    (xps_tru, yps_tru, zps_tru)),
                                                                np.arccos(cth_tru), azi_tru)
        # distance along tilt gradient
        dtg = -xps_tru*np.cos(np.pi/4)-yps_tru*np.sin(np.pi/4)
        if np.all(np.isnan(dtg)):
            # data perchance?
            dtg = -xps_fit*np.cos(np.pi/4)-yps_fit*np.sin(np.pi/4)
        # zshift
        zsf = tf.root.cc_zshift[slc]['value']
        # ratio of scattering coefficient
        scr = tf.root.cc_b400_tilted[slc]['value'] / \
            tf.root.cc_b400_notilt[slc]['value']

    plt.figure()
    for i, (lge_rec, label) in enumerate(zip([lge_fit, lge_alt], [fit, alt])):
        plot_quartiles_vs_x((10**(lge_rec)-10**(lge_tru))/10**(lge_tru),
                            lge_tru,
                            lge_bins,
                            label)
        plt.axhline(0, linewidth=0.5, color='gray', linestyle='--')
        plt.xlabel(r'$\log_{10}(E_{dep}$ [GeV]$)$')
        plt.ylabel('$(E_{rec}-E_{dep})/E_{dep}$')
        plt.xlim(xmin=3 if inclowe else 4.5)
        plt.ylim(-0.5, 0.5)
        plt.legend()
        if i == 0:
            plt.savefig(f'{outpath}/{nufilename}_mederes_fit.png', bbox_inches='tight')
    plt.savefig(f'{outpath}/{nufilename}_mederes.png', bbox_inches='tight')

    plt.figure()
    for i, (len_rec, label) in enumerate(zip([len_fit, len_alt], [fit, alt])):
        plot_quartiles_vs_x((len_rec - len_tru) / len_tru,
                            len_tru,
                            len_bins[::3],
                            label)
    plt.xlabel(r'Length [m]')
    plt.ylabel('$(L_{rec}-L_{tru})/L_{tru}$')
    plt.axhline(0, linewidth=0.5, color='gray', linestyle='--')
    plt.xlim(0, 50)
    plt.ylim(-0.5, 0.5)
    plt.legend()
    plt.savefig(f'{outpath}/{nufilename}_medlenres.png', bbox_inches='tight')

    if len(asm_recs) > 0:
        plt.figure()
        for i, (asm_rec, label) in enumerate(zip(asm_recs, asm_labl)):
            plot_quartiles_vs_x(asm_rec - asm_tru,
                                len_tru,
                                len_bins[::3],
                                label)
        plt.xlabel(r'Length [m]')
        plt.ylabel('$A_{rec}-A_{tru}$')
        plt.axhline(0, linewidth=0.5, color='gray', linestyle='--')
        plt.xlim(0, 50)
        plt.ylim(-0.5, 0.5)
        plt.legend()
        plt.savefig(f'{outpath}/{nufilename}_medasmres_len.png', bbox_inches='tight')

    plt.clf()
    plot_medangres(len_tru, len_bins[::3],
                   cth_md_reco, cth_em_reco,
                   azi_md_reco, azi_em_reco,
                   cth_tru, azi_tru,
                   [fit, alt], inclowe)
    plt.xlabel('Length [m] (truth)')
    plt.xlim(xmin=0)
    plt.savefig(
        f'{outpath}/{nufilename}_medangres_len.png', bbox_inches='tight')

    plt.clf()
    plot_medangres(lge_tru, lge_bins,
                   cth_md_reco, cth_em_reco,
                   azi_md_reco, azi_em_reco,
                   cth_tru, azi_tru,
                   [fit, alt], inclowe)
    plt.savefig(f'{outpath}/{nufilename}_medangres.png', bbox_inches='tight')
    plt.text(0.05, 0.95, 'IceCube Preliminary', fontsize=14,
             transform=plt.gca().transAxes, color='r')
    plt.savefig(
        f'{outpath}/{nufilename}_medangres_prelim.png', bbox_inches='tight')

    plt.clf()
    plot_medangres(lge_neut, lge_bins,
                   cth_md_reco, cth_em_reco,
                   azi_md_reco, azi_em_reco,
                   cth_tru, azi_tru,
                   [fit, alt], inclowe,
                   e_xlab=r'\nu')
    plt.savefig(
        f'{outpath}/{nufilename}_medangres_enu.png', bbox_inches='tight')

    plt.clf()
    plot_medangres(lge_neut, lge_bins,
                   cth_md_reco, cth_em_reco,
                   azi_md_reco, azi_em_reco,
                   cth_neut, azi_neut,
                   [fit, alt], inclowe,
                   e_xlab=r'\nu')
    plt.ylabel('Reco-Nu. angular resolution [deg.]')

    plt.savefig(f'{outpath}/{nufilename}_mednures_enu.png', bbox_inches='tight')
    plt.clf()
    plot_medangres(lge_tru, lge_bins,
                   cth_md_reco, cth_em_reco,
                   azi_md_reco, azi_em_reco,
                   cth_neut, azi_neut,
                   [fit, alt], inclowe)
    plt.ylabel('Reco-Nu. angular resolution [deg.]')

    plt.savefig(f'{outpath}/{nufilename}_mednures.png', bbox_inches='tight')

    # if inclowe:
    #     _ = 'compare/cscd_zz.csv'
    #     if os.path.exists(_):
    #         mai = np.loadtxt(_, delimiter=',')
    #         rgb = np.asarray([92, 159, 92])/256
    #         plt.plot(*mai.T, label='Zelong (3.2.1-tilt-eff-optim)', color='pink')
    #         plt.legend()
    _ = 'compare/medangres_evgen.csv'
    if os.path.exists(_):
        mai = np.loadtxt(_, delimiter=',')
        rgb = np.asarray([2, 56, 88])/256
        plt.plot(*mai.T, label='EGen v1', color=rgb)
        plt.legend()
    _ = 'compare/medangres_cnn.csv'
    if os.path.exists(_):
        mai = np.loadtxt(_, delimiter=',')
        rgb = np.asarray([92, 159, 92])/256
        plt.plot(*mai.T, label='CNN', color=rgb)
        plt.legend()
    _ = 'compare/medangres_mle.csv'
    if os.path.exists(_):
        mai = np.loadtxt(_, delimiter=',')
        rgb = np.asarray([255, 127, 13])/256
        plt.plot(*mai.T, label='MLE (ICRC21.1065)', color=rgb)
        plt.legend()
    plt.ylim(0,25)
    plt.savefig(
        f'{outpath}/{nufilename}_medangres_compare.png', bbox_inches='tight')

    plt.clf()
    deepcore = (xps_tru < 200) & (yps_tru < 100) & (
        xps_tru > -100) & (yps_tru > -200)
    plot_medangres(lge_tru, lge_bins,
                   cth_md_reco, cth_em_reco,
                   azi_md_reco, azi_em_reco,
                   cth_tru, azi_tru,
                   [f'All events'], inclowe)
    plot_medangres(lge_tru[deepcore], lge_bins,
                   cth_md_reco[deepcore], cth_em_reco[deepcore],
                   azi_md_reco[deepcore], azi_em_reco[deepcore],
                   cth_tru[deepcore], azi_tru[deepcore],
                   [f'DeepCore events'], inclowe)

    plt.savefig(f'{outpath}/{nufilename}_medangres_dc.png', bbox_inches='tight')

    plt.clf()
    # from Alina's slides in Aachen
    contained = (rho_tru < 450) & (zps_tru < 450) & (
        zps_tru > -450) & ~((zps_tru > -200) & (zps_tru < -50))
    plot_medangres(lge_tru, lge_bins,
                   cth_md_reco, cth_em_reco,
                   azi_md_reco, azi_em_reco,
                   cth_tru, azi_tru,
                   [f'All events'], inclowe)
    plot_medangres(lge_tru[contained], lge_bins,
                   cth_md_reco[contained], cth_em_reco[contained],
                   azi_md_reco[contained], azi_em_reco[contained],
                   cth_tru[contained], azi_tru[contained],
                   [f'Contained events'], inclowe)

    plt.savefig(
        f'{outpath}/{nufilename}_medangres_innout.png', bbox_inches='tight')

    for dcs_lim in [30, 60]:
        plt.clf()
        plot_medangres(lge_tru[dcs_fit < dcs_lim], lge_bins,
                       cth_md_reco[dcs_fit <
                                   dcs_lim], cth_em_reco[dcs_fit < dcs_lim],
                       azi_md_reco[dcs_fit <
                                   dcs_lim], azi_em_reco[dcs_fit < dcs_lim],
                       cth_tru[dcs_fit < dcs_lim], azi_tru[dcs_fit < dcs_lim],
                       [f'{fit} dcs$<${dcs_lim}m'], inclowe)
        plot_medangres(lge_tru[dcs_fit > dcs_lim], lge_bins,
                       cth_md_reco[dcs_fit >
                                   dcs_lim], cth_em_reco[dcs_fit > dcs_lim],
                       azi_md_reco[dcs_fit >
                                   dcs_lim], azi_em_reco[dcs_fit > dcs_lim],
                       cth_tru[dcs_fit > dcs_lim], azi_tru[dcs_fit > dcs_lim],
                       [f'{fit} dcs$>${dcs_lim}m'], inclowe)

        plt.savefig(
            f'{outpath}/{nufilename}_medangres_dcs{dcs_lim}m.png', bbox_inches='tight')

    plt.clf()
    lge_bins_wide = [4, 5, 6, 7]
    lge_i = np.digitize(lge_tru, lge_bins_wide)
    [plt.hist(np.degrees(np.arccos(cth_md_reco)-np.arccos(cth_tru))[lge_i == ei],
              bins=np.linspace(-180, 180, 50),
              histtype='step',
              label=r'${:.2g} \leq E_{{dep}} < {:.2g}$'.format(
                  10**lge_bins_wide[i], 10**lge_bins_wide[i+1]))
     for i, ei in enumerate(range(1, len(lge_bins_wide)))]
    plt.xlabel(r'$\delta \theta_{zen}$ [deg]')
    plt.ylabel('N')
    plt.xlim(-180, 180)
    plt.yscale('log')
    plt.legend()

    plt.savefig(f'{outpath}/{nufilename}_dzen.png', bbox_inches='tight')

    plt.clf()
    cth_i = np.digitize(cth_tru, cth_bins)
    # plt.hist(np.degrees(np.arccos(cth_md_reco)-np.arccos(cth_tru))[cth_tru < -0.8],
    #           bins=np.linspace(-180, 180, 50),
    #           histtype='step', density=True, color='gray',
    #           linewidth=1,
    #           label=f'{np.nanmedian(np.degrees(np.arccos(cth_md_reco)-np.arccos(cth_tru))[cth_tru < -0.8])}')
    [plt.hist(np.degrees(np.arccos(cth_md_reco)-np.arccos(cth_tru))[cth_i == ei],
              bins=np.linspace(-180, 180, 50),
              histtype='step', density=True, color='gray',
              linewidth=1,
              alpha=0.3+i*0.7/len(cth_bins))
     for i, ei in enumerate(range(1, len(cth_bins)))]
    plt.xlabel(r'$\delta \theta_{zen}$ [deg]')
    plt.ylabel('density')
    plt.xlim(-180, 180)
    # plt.legend()
    # plt.yscale('log')

    plt.savefig(f'{outpath}/{nufilename}_dzen_cths.png', bbox_inches='tight')

    plt.clf()
    dzen_md = np.degrees(np.arccos(cth_md_reco)-np.arccos(cth_tru))
    dzen_em = np.degrees(np.arccos(cth_em_reco)-np.arccos(cth_tru))
    plt.hist(dzen_md,
             bins=np.linspace(-180, 180, 50),
             histtype='step',
             label=rf'{fit} ${np.nanmedian(dzen_md):.2f}^\circ$')
    plt.hist(dzen_em,
             bins=np.linspace(-180, 180, 50),
             histtype='step',
             label=rf'{alt} ${np.nanmedian(dzen_em):.2f}^\circ$')
    plt.xlabel(r'$\delta \theta_{zen}$ [deg]')
    plt.ylabel('N')
    plt.xlim(-60, 60)
    plt.yscale('log')
    plt.legend(loc='lower center')

    plt.savefig(f'{outpath}/{nufilename}_dzen_all.png', bbox_inches='tight')

    plt.clf()
    # dpsi = calculator.center_angle(
    #     np.arccos(cth_tru), azi_tru, reco_zen, reco_azi)
    lge_bins_wide = [2, 4, 6, 8]
    lge_i = np.digitize(lge_tru, lge_bins_wide)
    cas = [calculator.center_angle(
        np.arccos(cth_tru)[lge_i == ei],
        azi_tru[lge_i == ei],
        np.arccos(cth_md_reco)[lge_i == ei],
        azi_md_reco[lge_i == ei])
        for ei in range(1, len(lge_bins_wide))]
    [plt.hist(np.degrees(ca),
              bins=dps_bins, histtype='step',
              label=rf'${10**lge_bins_wide[i]:.2g} \leq E_{{dep}} < {10**lge_bins_wide[i+1]:.2g}$ ${np.nanmedian(np.degrees(ca)):.2f}^\circ$')
     for i, ca in enumerate(cas) if len(ca) > 0]
    plt.xlabel(r'$\delta \Psi$')
    plt.ylabel('N')
    plt.xlim(0, 60)
    plt.legend()

    plt.savefig(f'{outpath}/{nufilename}_dpsi.png', bbox_inches='tight')

    plt.clf()
    cas_md = calculator.center_angle(np.arccos(cth_tru),
                                     azi_tru,
                                     np.arccos(cth_md_reco),
                                     azi_md_reco)
    cas_em = calculator.center_angle(np.arccos(cth_tru),
                                     azi_tru,
                                     np.arccos(cth_em_reco),
                                     azi_em_reco)
    plt.hist(np.degrees(cas_md),
             bins=dps_bins, histtype='step',
             label=rf'{fit} ${np.nanmedian(np.degrees(cas_md)):.2f}^\circ$')
    plt.hist(np.degrees(cas_em),
             bins=dps_bins, histtype='step',
             label=rf'{alt} ${np.nanmedian(np.degrees(cas_em)):.2f}^\circ$')
    plt.xlabel(r'$\delta \Psi$ [deg]')
    plt.ylabel('N')
    plt.xlim(0, 60)
    plt.legend()

    plt.savefig(f'{outpath}/{nufilename}_dpsi_all.png', bbox_inches='tight')
    plt.xlim(0, 180)
    plt.yscale('log')
    plt.savefig(f'{outpath}/{nufilename}_dpsi_all_pi.png', bbox_inches='tight')

    plt.clf()
    plt.scatter(trv_vtx_fit[np.abs(cth_tru) < 0.1],
                azi_tru[np.abs(cth_tru) < 0.1], marker='.')
    plt.xlabel('Transverse shift')
    plt.xscale('log')
    plt.xlim(0.1, 100)
    plt.ylim(0, 2*np.pi)
    plt.ylabel('True azimuth')

    plt.savefig(
        f'{outpath}/{nufilename}_fitvtxbias_proj_scatter.png', bbox_inches='tight')

    plt.clf()
    plt.scatter(trv_vtx_alt[np.abs(cth_tru) < 0.1],
                azi_tru[np.abs(cth_tru) < 0.1], marker='.')
    plt.xlabel('Transverse shift')
    plt.xscale('log')
    plt.xlim(0.1, 100)
    plt.ylim(0, 2*np.pi)
    plt.ylabel('True azimuth')

    plt.savefig(
        f'{outpath}/{nufilename}_altvtxbias_proj_scatter.png', bbox_inches='tight')

    _ = {'m': (dtg, (-400, 400), '_'),
         'Tilt z-correction [m]': (zsf, (-15, 15), '_zsf_'),
         'b400 with tilt/b400 without tilt': (scr, (0.8, 1.2), '_scr_')}
    for k in _:
        if _[k][0] is None:
            continue
        plt.clf()
        hknot = knots_std[18]
        shknot = (np.arccos(cth_tru) < np.radians(hknot+1)
                  ) & (np.arccos(cth_tru) > np.radians(hknot-1))
        [plt.axvline(x, linestyle='--', linewidth=1, alpha=0.5,
                     color='gray') for x in knots_std]
        plt.axvline(hknot, linestyle='--', color='k')
        plt.scatter(np.degrees(np.arccos(cth_md_reco[shknot])), zps_fit[shknot], s=2,
                    c=_[k][0][shknot], vmin=_[k][1][0], vmax=_[k][1][1], cmap='coolwarm')
        plt.colorbar(label=k)
        plt.xlabel('Reco. zenith [deg.]')
        plt.ylabel('Reco. z [m]')
        plt.xlim(0, 180)
        plt.ylim(-650, 400)

        plt.text(0.05, 0.95, 'IceCube Preliminary', fontsize=14,
                 transform=plt.gca().transAxes, color='r')
        plt.savefig(
            f'{outpath}/{nufilename}_recozenith_recoz{_[k][2]}hknot_k9_prelim.png', bbox_inches='tight')

        plt.clf()
        hknot = knots_mie[9]
        shknot = (np.arccos(cth_tru) < np.radians(hknot+1)
                  ) & (np.arccos(cth_tru) > np.radians(hknot-1))
        [plt.axvline(x, linestyle='--', linewidth=1, alpha=0.5,
                     color='gray') for x in knots_mie]
        plt.axvline(hknot, linestyle='--', color='k')
        plt.scatter(np.degrees(np.arccos(cth_em_reco[shknot])), zps_alt[shknot], s=2,
                    c=_[k][0][shknot], vmin=_[k][1][0], vmax=_[k][1][1], cmap='coolwarm')
        plt.colorbar(label=k)
        plt.xlabel('Reco. zenith [deg.]')
        plt.ylabel('Reco. z [m]')
        plt.xlim(0, 180)
        plt.ylim(-650, 400)

        plt.text(0.05, 0.95, 'IceCube Preliminary', fontsize=14,
                 transform=plt.gca().transAxes, color='r')
        plt.savefig(
            f'{outpath}/{nufilename}_recozenith_recoz{_[k][2]}hknotmie_k9_prelim.png', bbox_inches='tight')
    for weights, wlabel, cmax in zip([np.ones(cth_md_reco.shape)], [''], [1e9]):
        for cnorm, clabel in zip([Normalize, LogNorm], ['', '_clog']):
            if do_plot_drlogl:
                plt.clf()
                plt.hist(drlogl, bins=drlogl_bins, histtype='step',
                         label='All', color='black')
                plt.hist(drlogl[(intact == 1) & (np.abs(flavor) == 14)], bins=drlogl_bins,
                         histtype='step', label='numu CC')
                for _ls, cl_choice in zip(['--', ':'], [250, 350]):
                    plt.hist(drlogl[(intact == 1) & (contained_length > cl_choice) & (np.abs(flavor) == 14)],
                             linestyle=_ls,
                             bins=drlogl_bins, histtype='step',
                             label=f'numu CC, contained length > {cl_choice}m')
                plt.xlabel(f'rlogl({fit}) - rlogl({alt})')
                plt.ylabel('N')
                plt.yscale(yscale(cnorm()))
                plt.legend(loc='upper left')

                plt.savefig(
                    f'{outpath}/{nufilename}_drlogl{clabel}{wlabel}.png', bbox_inches='tight')

            plt.clf()
            plt.hist(lon_vtx_fit, histtype='step', label=r'longitudinal shift',
                     bins=vtx_bins)
            plt.hist(trv_vtx_fit, histtype='step', label=r'transverse shift',
                     bins=rho_bins)
            plt.xlabel(r'$\hat{x} - x_{true}$')
            plt.ylabel('N')
            plt.yscale(yscale(cnorm()))
            plt.xlim(vtx_bins[0], vtx_bins[-1])
            plt.legend()

            plt.savefig(
                f'{outpath}/{nufilename}_fitvtxbias_proj{clabel}{wlabel}.png', bbox_inches='tight')

            plt.clf()
            plt.hist(xps_fit-xps_tru, histtype='step', label=r'$\delta x$',
                     bins=vtx_bins)
            plt.hist(yps_fit-yps_tru, histtype='step', label=r'$\delta y$',
                     bins=vtx_bins)
            plt.hist(zps_fit-zps_tru, histtype='step', label=r'$\delta z$',
                     bins=vtx_bins)
            plt.xlabel(r'$\hat{x} - x_{true}$')
            plt.ylabel('N')
            plt.yscale(yscale(cnorm()))
            plt.xlim(vtx_bins[0], -vtx_bins[0])
            plt.legend()

            plt.savefig(
                f'{outpath}/{nufilename}_fitvtxbias{clabel}{wlabel}.png', bbox_inches='tight')

            plt.clf()
            plt.hist(xps_fit-xps_tru, histtype='step', label=r'$\delta x$',
                     bins=vtx_bins)
            plt.hist(yps_fit-yps_tru, histtype='step', label=r'$\delta y$',
                     bins=vtx_bins)
            plt.hist(zps_fit-zps_tru, histtype='step', label=r'$\delta z$',
                     bins=vtx_bins)
            plt.gca().set_prop_cycle(None)
            plt.hist(xps_alt-xps_tru, histtype='step', linestyle='--',
                     bins=vtx_bins)
            plt.hist(yps_alt-yps_tru, histtype='step', linestyle='--',
                     bins=vtx_bins)
            plt.hist(zps_alt-zps_tru, histtype='step', linestyle='--',
                     bins=vtx_bins)
            plt.xlabel(r'$\hat{x} - x_{true}$')
            plt.ylabel('N')
            plt.yscale(yscale(cnorm()))
            plt.xlim(vtx_bins[0], -vtx_bins[0])
            plt.legend()

            plt.savefig(
                f'{outpath}/{nufilename}_vtxbias{clabel}{wlabel}.png', bbox_inches='tight')

            plt.clf()
            plt.hist(lon_vtx_fit, histtype='step', label=r'longitudinal shift',
                     bins=vtx_bins)
            plt.hist(trv_vtx_fit, histtype='step', label=r'transverse shift',
                     bins=rho_bins)
            # plt.hist(r3d_vtx_fit, histtype='step', label=r'radial shift',
            #          bins=vtx_bins)
            plt.gca().set_prop_cycle(None)
            plt.hist(lon_vtx_alt, histtype='step', linestyle='--',
                     bins=vtx_bins)
            plt.hist(trv_vtx_alt, histtype='step', linestyle='--',
                     bins=rho_bins)
            # plt.hist(r3d_vtx_alt, histtype='step', linestyle='--',
            #          bins=vtx_bins)
            plt.xlabel(r'$\hat{x} - x_{true}$')
            plt.ylabel('N')
            plt.yscale(yscale(cnorm()))
            plt.xlim(vtx_bins[0], vtx_bins[-1])
            plt.legend()

            plt.savefig(
                f'{outpath}/{nufilename}_vtxbias_proj{clabel}{wlabel}.png', bbox_inches='tight')

            plt.clf()
            plt.hist(lge_fit, histtype='step', label=fit,
                     bins=lge_bins, range=(lge_bins[0], lge_bins[-1]))
            plt.hist(lge_alt, histtype='step', label=alt,
                     bins=lge_bins, range=(lge_bins[0], lge_bins[-1]))
            plt.xlabel('Energy')
            plt.ylabel('N')
            try:
                plt.yscale(yscale(cnorm()))
                plt.legend()

                plt.savefig(
                    f'{outpath}/{nufilename}_recoenergy{clabel}{wlabel}.png', bbox_inches='tight')
            except ValueError:
                continue

            plt.clf()
            [plt.axvline(x, linestyle='--', linewidth=1, alpha=0.5, color='gray')
             for x in np.cos(np.radians(knots_mie))]
            plt.hist(cth_md_reco, histtype='step', label=fit,
                     bins=cth_bins, range=(cth_bins[0], cth_bins[-1]))
            plt.hist(cth_em_reco, histtype='step', label=alt,
                     bins=cth_bins, range=(cth_bins[0], cth_bins[-1]))
            # plt.hist(cth_tz_reco, histtype='step', label='Truezen',
            #          bins=cth_bins, range=(cth_bins[0],cth_bins[-1]))
            # plt.hist(cth_lb_reco, histtype='step', label='LBFGSB',
            #          bins=cth_bins, range=(cth_bins[0],cth_bins[-1]))
            plt.xlabel(r'$\cos \Theta_{\mathrm{zen}}$')
            plt.ylabel('N')
            plt.yscale(yscale(cnorm()))
            plt.legend()
            plt.xlim(-1, 1)

            plt.savefig(
                f'{outpath}/{nufilename}_recozenith{clabel}{wlabel}.png', bbox_inches='tight')
            plt.hist(cth_tru, histtype='step', label='Truth',
                     bins=cth_bins, range=(cth_bins[0], cth_bins[-1]), linewidth=1, color='grey')
            plt.legend()
            plt.savefig(
                f'{outpath}/{nufilename}_truerecozenith{clabel}{wlabel}.png', bbox_inches='tight')

            plt.clf()
            plt.hist(azi_md_reco, histtype='step', label=fit,
                     bins=azi_bins, range=(azi_bins[0], azi_bins[1]))
            plt.hist(azi_em_reco, histtype='step', label=alt,
                     bins=azi_bins, range=(azi_bins[0], azi_bins[1]))
            # major axis of anisotropy
            # https://icecube.wisc.edu/~dima/work/WISC/papers/2013_ICRC/ice/icrc2013-0580.pdf
            [plt.axvline(x, linestyle='--', color='gray')
             for x in np.radians(iflow)]
            # plt.hist(azi_tz_reco, histtype='step', label='Truezen',
            #          bins=azi_bins, range=(azi_bins[0], azi_bins[1]))
            # plt.hist(azi_lb_reco, histtype='step', label='LBFGSB',
            #          bins=azi_bins, range=(azi_bins[0], azi_bins[1]))
            plt.xlabel('Azimuth')
            plt.ylabel('N')
            plt.yscale(yscale(cnorm()))
            plt.legend(loc='lower left')
            plt.xlim(0, np.pi*2)

            plt.savefig(
                f'{outpath}/{nufilename}_recoazimuth{clabel}{wlabel}.png', bbox_inches='tight')
            plt.hist(azi_tru, histtype='step', label='Truth',
                     bins=azi_bins, range=(azi_bins[0], azi_bins[1]), linewidth=1, color='grey')
            plt.legend()
            plt.savefig(
                f'{outpath}/{nufilename}_truerecoazimuth{clabel}{wlabel}.png', bbox_inches='tight')

            plt.clf()
            h2d, _, _, _ = plt.hist2d(cth_tru,
                                      cth_md_reco, weights=weights,
                                      bins=cth_bins, cmax=cmax, norm=cnorm())
            plt.plot(*[cth_bins]*2, linewidth=0.5, color='gray')
            plt.xlabel('True zenith')
            plt.ylabel(f'Reco zenith ({fit})')
            plt.colorbar()

            plt.savefig(
                f'{outpath}/{nufilename}_zenith{clabel}{wlabel}.png', bbox_inches='tight')

            plt.clf()
            plt.pcolormesh(cth_bins, cth_bins, h2d.T/np.sum(h2d, axis=1), cmap='Blues_r',
                           norm=cnorm(vmax=1))
            plt.plot(*[cth_bins]*2, linewidth=0.5, color='gray')
            plt.xlabel('True zenith')
            plt.ylabel(f'Reco zenith ({fit})')
            plt.colorbar()

            plt.savefig(
                f'{outpath}/{nufilename}_zenith_colpdf{clabel}{wlabel}.png', bbox_inches='tight')

            plt.clf()
            h2d, _, _, _ = plt.hist2d(cth_tru,
                                      cth_em_reco, weights=weights,
                                      bins=cth_bins, cmax=cmax, norm=cnorm())
            plt.pcolormesh(cth_bins, cth_bins, h2d.T/np.sum(h2d, axis=1), cmap='Blues_r',
                           norm=cnorm(vmax=1))
            plt.plot(*[cth_bins]*2, linewidth=0.5, color='gray')
            plt.xlabel('True zenith')
            plt.ylabel(f'Reco zenith ({alt})')
            plt.colorbar()

            plt.savefig(
                f'{outpath}/{nufilename}_altzenith_colpdf{clabel}{wlabel}.png', bbox_inches='tight')

            plt.clf()
            h2d, _, _, _ = plt.hist2d(azi_tru,
                                      azi_md_reco, weights=weights,
                                      bins=azi_bins, cmax=cmax, norm=cnorm())
            plt.plot(*[azi_bins]*2, linewidth=0.5, color='gray')
            plt.xlabel('True azimuth')
            plt.ylabel(f'Reco azimuth ({fit})')
            plt.colorbar()

            plt.savefig(
                f'{outpath}/{nufilename}_azimuth{clabel}{wlabel}.png', bbox_inches='tight')

            plt.clf()
            plt.pcolormesh(azi_bins, azi_bins, h2d.T/np.sum(h2d, axis=1), cmap='Blues_r',
                           norm=cnorm(vmax=1))
            plt.plot(*[azi_bins]*2, linewidth=0.5, color='gray')
            plt.xlabel('True azimuth')
            plt.ylabel(f'Reco azimuth ({fit})')
            plt.colorbar()

            plt.savefig(
                f'{outpath}/{nufilename}_azimuth_colpdf{clabel}{wlabel}.png', bbox_inches='tight')

            plt.clf()
            h2d, _, _, _ = plt.hist2d(azi_tru,
                                      azi_em_reco, weights=weights,
                                      bins=azi_bins, cmax=cmax, norm=cnorm())
            plt.pcolormesh(azi_bins, azi_bins, h2d.T/np.sum(h2d, axis=1), cmap='Blues_r',
                           norm=cnorm(vmax=1))
            plt.plot(*[azi_bins]*2, linewidth=0.5, color='gray')
            plt.xlabel('True azimuth')
            plt.ylabel(f'Reco azimuth ({alt})')
            plt.colorbar()

            plt.savefig(
                f'{outpath}/{nufilename}_altazimuth_colpdf{clabel}{wlabel}.png', bbox_inches='tight')

            plt.clf()
            h2d, _, _, _ = plt.hist2d(lge_tru,
                                      lge_fit, weights=weights,
                                      bins=lge_bins_fine, cmax=cmax, norm=cnorm())
            plt.plot(*[lge_bins_fine]*2,
                     linewidth=0.5, color='gray')
            plt.xlabel('True energy')
            plt.ylabel(f'Reco energy ({fit})')
            try:
                plt.colorbar()
                plt.xlim(xmin=3 if inclowe else 4.5)
                plt.ylim(ymin=3 if inclowe else 4.5)

                plt.savefig(
                    f'{outpath}/{nufilename}_energy{clabel}{wlabel}.png', bbox_inches='tight')
            except ValueError:
                continue

            plt.clf()
            plt.pcolormesh(lge_bins_fine, lge_bins_fine, h2d.T/np.sum(h2d, axis=1), cmap='Blues_r',
                           norm=cnorm(vmax=1))
            plt.plot(*[lge_bins_fine]*2, linewidth=0.5, color='gray')
            plt.xlabel('True energy')
            plt.ylabel(f'Reco energy ({fit})')
            plt.colorbar()
            plt.xlim(xmin=3 if inclowe else 4.5)
            plt.ylim(ymin=3 if inclowe else 4.5)

            plt.savefig(
                f'{outpath}/{nufilename}_energy_colpdf{clabel}{wlabel}.png', bbox_inches='tight')

            plt.clf()
            h2d, _, _, _ = plt.hist2d(lge_tru,
                                      len_fit, weights=weights,
                                      bins=[lge_bins_fine, len_bins], cmax=cmax, norm=cnorm())
            plt.xlabel('True energy')
            plt.ylabel(f'Reco length ({fit})')
            plt.ylim(0, 100)
            try:
                plt.colorbar()
                plt.xlim(xmin=3 if inclowe else 4.5)

                plt.savefig(
                    f'{outpath}/{nufilename}_evl{clabel}{wlabel}.png', bbox_inches='tight')
            except ValueError:
                continue

            plt.clf()
            plt.pcolormesh(lge_bins_fine,
                           len_bins,
                           h2d.T/np.sum(h2d, axis=1),
                           cmap='Blues_r',
                           norm=cnorm(vmax=1))
            plt.xlabel('True energy')
            plt.ylabel(f'Reco length ({fit})')
            plt.colorbar()
            plt.xlim(xmin=3 if inclowe else 4.5)
            plt.ylim(0, 100)

            plt.savefig(
                f'{outpath}/{nufilename}_evl_colpdf{clabel}{wlabel}.png', bbox_inches='tight')

            plt.clf()
            h2d, _, _, _ = plt.hist2d(len_tru,
                                      len_fit, weights=weights,
                                      bins=[len_bins, len_bins], cmax=cmax, norm=cnorm())

            plt.xlabel('True length [m]')
            plt.ylabel(f'Reco length [m] ({fit})')
            plt.xlim(xmin=0)
            plt.ylim(ymin=0)
            try:
                plt.colorbar()
                plt.savefig(
                    f'{outpath}/{nufilename}_length{clabel}{wlabel}.png', bbox_inches='tight')
            except ValueError:
                continue

            plt.clf()
            plt.pcolormesh(len_bins,
                           len_bins,
                           h2d.T/np.sum(h2d, axis=1),
                           cmap='Blues_r',
                           norm=cnorm(vmax=1))
            plt.xlabel('True length [m]')
            plt.ylabel(f'Reco length [m] ({fit})')
            plt.colorbar()
            plt.xlim(xmin=0)
            plt.ylim(ymin=0)

            plt.savefig(
                f'{outpath}/{nufilename}_length_colpdf{clabel}{wlabel}.png', bbox_inches='tight')

            if len(asm_recs) > 0:
                asm_sel = asm_recs[0] < 0.3
                plt.clf()
                h2d, _, _, _ = plt.hist2d(len_tru[asm_sel],
                                          len_fit[asm_sel], weights=weights[asm_sel],
                                          bins=[len_bins, len_bins], cmax=cmax, norm=cnorm())

                plt.xlabel('True length [m]')
                plt.ylabel(f'Reco length [m] ({fit})')
                plt.xlim(xmin=0)
                plt.ylim(ymin=0)
                try:
                    plt.colorbar()
                    plt.savefig(
                        f'{outpath}/{nufilename}_lenasm{clabel}{wlabel}.png', bbox_inches='tight')
                except ValueError:
                    continue

                plt.clf()
                plt.pcolormesh(len_bins,
                               len_bins,
                               h2d.T/np.sum(h2d, axis=1),
                               cmap='Blues_r',
                               norm=cnorm(vmax=1))
                plt.xlabel('True length [m]')
                plt.ylabel(f'Reco length [m] ({fit})')
                plt.colorbar()
                plt.xlim(xmin=0)
                plt.ylim(ymin=0)

                plt.savefig(
                    f'{outpath}/{nufilename}_lenasm_colpdf{clabel}{wlabel}.png', bbox_inches='tight')

                avldir = f'{outpath}/{nufilename}_avl_tauvis{clabel}{wlabel}'
                os.makedirs(avldir, exist_ok=True)
                for tdc in np.unique(np.abs(tau_vis)):
                    _pfxs = ['', 'contained_']
                    _sels = [np.abs(tau_vis) == tdc,
                             (np.abs(tau_vis) == tdc) & (len_tru < contained_length)]
                    if do_plot_drlogl:
                        _pfxs.append('drlogl_')
                        _sels.append((np.abs(tau_vis) == tdc) & (drlogl < -0.02))
                    for _pfx, _sel in zip(_pfxs, _sels):
                        plt.clf()
                        h2d, _, _, _ = plt.hist2d(len_fit[_sel],
                                                  asm_fit[_sel], weights=weights[_sel],
                                                  bins=[len_bins, asm_bins], cmax=cmax, norm=cnorm())
                        plt.ylabel(rf'$A_{{rec}}$ ({fit})')
                        plt.xlabel(rf'$L_{{rec}}$ ({fit})')
                        plt.ylim(0, 100)
                        try:
                            plt.colorbar()
                            plt.ylim(-1., 1.)
                            plt.xlim(0, 100)

                            plt.savefig(
                                f'{avldir}/{_pfx}tdc{tdc:03}.png', bbox_inches='tight')
                        except ValueError:
                            continue

                        plt.clf()
                        plt.pcolormesh(len_bins,
                                       asm_bins,
                                       h2d.T/np.sum(h2d, axis=1),
                                       cmap='Blues_r',
                                       norm=cnorm(vmax=1))
                        plt.ylabel(rf'$A_{{rec}}$ ({fit})')
                        plt.xlabel(rf'$L_{{rec}}$ ({fit})')
                        plt.colorbar()
                        plt.ylim(-1., 1.)
                        plt.xlim(0, 100)

                        plt.savefig(
                            f'{avldir}/{_pfx}tdc{tdc:03}_colpdf.png', bbox_inches='tight')

            if mig_rlogl is not None and tru_rlogl is not None:
                plt.clf()
                inds = np.digitize(np.degrees(np.arccos(cth_tru)), th_bins)
                drl = tru_rlogl-mig_rlogl
                dth = np.abs(np.degrees(np.arccos(cth_tru)) -
                             np.degrees(np.arccos(cth_md_reco)))
                meddrl = [np.median(drl[inds == i+1])
                          for i in range(len(th_bins)-1)]
                plt.plot(calculator.centers(th_bins), meddrl)
                # H, xedges, yedges = np.histogram2d(cth_tru,
                #                                    tru_rlogl-mig_rlogl, weights=weights,
                #                                    bins=(cth_bins,drl_bins))
                # Hnormed = H / np.sum(H, axis=1)
                # plt.pcolormesh(xedges,yedges,Hnormed.T, norm=cnorm())
                [plt.axvline(x, linestyle='--', color='gray')
                 for x in knots_std]
                plt.xlabel('True zenith')
                plt.ylabel('Median dRlogl (Truth-MIGRAD)')
                # plt.colorbar()

                plt.savefig(
                    f'{outpath}/{nufilename}_drlogl{clabel}{wlabel}.png', bbox_inches='tight')

                plt.clf()
                hh = plt.hist(mtr_dlogl, bins=llh_bins, histtype='step',
                              label=f'All; p={kstest(mtr_dlogl, chi2(df=2).cdf)[-1]:.2g}')
                for i in range(1, len(lge_bins_wide)):
                    try:
                        plt.hist(
                            mtr_dlogl[lge_i == i],
                            bins=llh_bins, histtype='step',
                            label=rf'${10**lge_bins_wide[i-1]:.2g} \leq E_{{dep}} < {10**lge_bins_wide[i]:.2g}; p={kstest(mtr_dlogl[lge_i==i], chi2(df=2).cdf)[-1]:.2g}$')
                    except ValueError:
                        pass
                x2x = calculator.centers(llh_bins)
                plt.plot(x2x, chi2(2).pdf(x2x)*len(mtr_dlogl), 'k-',
                         label=r'$\chi^2(k=2)$')
                plt.xlabel(r'$2 (l(\hat{\theta})-l(\theta_{t}))$')
                plt.ylabel('N')
                plt.xlim(llh_bins[0], llh_bins[-1])
                plt.ylim(0 if yscale(cnorm()) ==
                         'linear' else 0.9, hh[0].max()*1.1)
                plt.yscale(yscale(cnorm()))
                plt.legend()

                plt.savefig(
                    f'{outpath}/{nufilename}_dllh{clabel}{wlabel}.png', bbox_inches='tight')

                plt.figure(figsize=(6, 6))
                plot_wilks_coverage(mtr_dlogl, color='k', label='All')
                # plot_wilks_coverage(mtr_dlogl[contained],color='k',linestyle='--',label='Contained')
                [plot_wilks_coverage(mtr_dlogl[lge_i == i],
                                     label=r'${:.2g} \leq E_{{dep}} < {:.2g}$'.format(
                                         10**lge_bins_wide[i-1], 10**lge_bins_wide[i])) for i in range(1, len(lge_bins_wide)) if len(mtr_dlogl[lge_i == i]) > 0]
                plt.yscale(yscale(cnorm()))
                plt.xscale(yscale(cnorm()))
                plt.tight_layout()
                plt.savefig(
                    f'{outpath}/{nufilename}_coverage{clabel}{wlabel}.png', bbox_inches='tight')
                plt.close()

            plt.clf()
            plt.hist(azi_md_reco, histtype='step',
                     weights=weights, range=(-1, 1),
                     bins=azi_bins)
            for rho_max in [100, 200, 300]:
                selection = rho_fit < rho_max
                plt.hist(azi_md_reco[selection], histtype='step',
                         weights=weights[selection], label=r'$\rho_{{max}}={}$'.format(
                             rho_max),
                         bins=azi_bins)
            plt.legend()
            plt.xlabel('Reco azimuth')
            plt.ylabel('N')
            plt.yscale(yscale(cnorm()))

            plt.savefig(
                f'{outpath}/{nufilename}_recoazimuthrho{clabel}{wlabel}.png', bbox_inches='tight')

            for k, hknot in enumerate(knots_std):
                shknot = (np.arccos(cth_tru) < np.radians(hknot+1)
                          ) & (np.arccos(cth_tru) > np.radians(hknot-1))
                plt.clf()
                _contents, _, _, _ = plt.hist2d(cth_md_reco[shknot],
                                                zps_fit[shknot], weights=weights[shknot],
                                                bins=(cth_bins, zps_bins), norm=cnorm())
                plt.xlabel('Reco zenith')
                plt.ylabel('Reco z')
                [plt.axvline(x, linestyle='--', color='gray')
                 for x in np.cos(np.radians(knots_std))]
                if np.any(_contents):
                    # check there are contents to prevent lognorm error
                    plt.colorbar()
                plt.grid(False)

                _ = f'{outpath}/{nufilename}_recozenith_recoz_hknot_hist2d{clabel}{wlabel}'
                os.makedirs(_, exist_ok=True)
                plt.savefig(f'{_}/k{k}.png', bbox_inches='tight')

                if mig_rlogl is not None and tru_rlogl is not None:
                    plt.clf()
                    plt.scatter(xps_fit[shknot], yps_fit[shknot], s=2,
                                c=dth[shknot], norm=cnorm(0.01, 20))
                    plt.colorbar()
                    plt.xlabel(f'x [{fit}]')
                    plt.ylabel(f'y [{fit}]')

                    _ = f'{outpath}/{nufilename}_recox_recoy_dth_hknot{clabel}{wlabel}'
                    os.makedirs(_, exist_ok=True)
                    plt.savefig(f'{_}/k{k}.png', bbox_inches='tight')

                    plt.clf()
                    plt.scatter(lge_tru[shknot], drl[shknot], s=2,
                                c=dth[shknot], norm=cnorm(1e-3, 20))
                    plt.xlabel('True E')
                    plt.ylabel('dRlogl (True-MIGRAD)')
                    plt.ylim(-0.02, 0.02)
                    plt.colorbar()

                    _ = f'{outpath}/{nufilename}_truee_drlogl_hknot{clabel}{wlabel}'
                    os.makedirs(_, exist_ok=True)
                    plt.savefig(f'{_}/k{k}.png', bbox_inches='tight')

                if cnorm is Normalize:
                    plt.clf()
                    [plt.axvline(x, linestyle='--', linewidth=1,
                                 alpha=0.5, color='gray') for x in knots_std]
                    plt.axvline(hknot, linestyle='--', color='k')
                    # plt.scatter(np.degrees(np.arccos(cth_md_reco[shknot])),zps_fit[shknot],s=2,
                    #             c=drl[shknot],vmin=-0.02,vmax=0.02,cmap='coolwarm')
                    plt.scatter(np.degrees(np.arccos(cth_md_reco[shknot])), zps_fit[shknot], s=2,
                                c=dtg[shknot], vmin=-400, vmax=400, cmap='coolwarm')
                    plt.colorbar()
                    plt.xlabel('Reco zenith')
                    plt.ylabel('Reco z')
                    plt.xlim(0, 180)
                    plt.ylim(-650, 400)

                    _ = f'{outpath}/{nufilename}_recozenith_recoz_hknot{clabel}{wlabel}'
                    os.makedirs(_, exist_ok=True)
                    plt.savefig(f'{_}/k{k}.png', bbox_inches='tight')

                    plt.clf()
                    [plt.axvline(x, linestyle='--', linewidth=1,
                                 alpha=0.5, color='gray') for x in knots_std]
                    plt.axvline(hknot, linestyle='--', color='k')
                    dazi = np.degrees(azi_md_reco-azi_tru)
                    dazi = np.min([360-dazi % 360, dazi % 360], axis=0)
                    plt.scatter(np.degrees(np.arccos(cth_md_reco[shknot])), dazi[shknot], s=2,
                                c=dtg[shknot], vmin=-400, vmax=400, cmap='coolwarm')
                    plt.colorbar(label='m')
                    plt.xlabel('Reco zenith')
                    plt.ylabel('Reco azi - True azi')
                    plt.xlim(0, 180)
                    plt.ylim(1e-2, 180)
                    plt.yscale('log')

                    _ = f'{outpath}/{nufilename}_recozenith_deltaazi_hknot{clabel}{wlabel}'
                    os.makedirs(_, exist_ok=True)
                    plt.savefig(f'{_}/k{k}.png', bbox_inches='tight')

                    plt.clf()
                    plt.scatter(dazi[shknot], zps_fit[shknot], s=2,
                                c=dtg[shknot], vmin=-400, vmax=400, cmap='coolwarm')
                    plt.colorbar(label='m')
                    plt.ylabel('Reco z (MIGRAD)')
                    plt.xlabel('Reco azi - True azi (MIGRAD)')
                    plt.ylim(-650, 400)
                    plt.xlim(1e-2, 180)
                    plt.xscale('log')

                    _ = f'{outpath}/{nufilename}_deltaazi_recoz_hknot{clabel}{wlabel}'
                    os.makedirs(_, exist_ok=True)
                    plt.savefig(f'{_}/k{k}.png', bbox_inches='tight')

                    plt.clf()
                    [plt.axvline(x, linestyle='--', linewidth=1, alpha=0.5, color='gray')
                     for x in np.cos(np.radians(knots_std))]
                    plt.axvline(np.cos(np.radians(hknot)),
                                linestyle='--', color='k')
                    plt.scatter(cth_md_reco[shknot], lge_tru[shknot], s=2,
                                c=dtg[shknot], vmin=-400, vmax=400, cmap='coolwarm')
                    plt.colorbar(label='m')
                    plt.xlabel('Reco zenith (MIGRAD)')
                    plt.xlim(-1, 1)
                    plt.ylabel('True E')

                    _ = f'{outpath}/{nufilename}_recozenith_truee_hknot{clabel}{wlabel}'
                    os.makedirs(_, exist_ok=True)
                    plt.savefig(f'{_}/k{k}.png', bbox_inches='tight')

                    plt.clf()
                    plt.scatter(azi_tru[shknot], lge_tru[shknot], s=2,
                                c=dtg[shknot], vmin=-400, vmax=400, cmap='coolwarm')
                    plt.colorbar(label='m')
                    plt.xlabel('True azimuth')
                    plt.ylabel('True E')
                    _ = f'{outpath}/{nufilename}_trueazi_truee_hknot{clabel}{wlabel}'
                    os.makedirs(_, exist_ok=True)
                    plt.savefig(f'{_}/k{k}.png', bbox_inches='tight')

                    plt.clf()
                    plt.scatter(xps_fit[shknot], yps_fit[shknot], s=2,
                                c=dtg[shknot], vmin=-400, vmax=400, cmap='coolwarm')
                    plt.colorbar(label='m')
                    plt.xlabel(f'{fit} x [m]')
                    plt.ylabel(f'{fit} y [m]')
                    _ = f'{outpath}/{nufilename}_recox_recoy_hknot{clabel}{wlabel}'
                    os.makedirs(_, exist_ok=True)
                    plt.savefig(f'{_}/k{k}.png', bbox_inches='tight')

                    plt.clf()
                    plt.scatter(xps_tru[shknot], yps_tru[shknot], s=2,
                                c=dtg[shknot], vmin=-400, vmax=400, cmap='coolwarm')
                    plt.colorbar(label='m')
                    plt.xlabel('True x [m]')
                    plt.ylabel('True y [m]')
                    plt.annotate('tilt', (350, -400), xytext=(450, -300),
                                 arrowprops=dict(arrowstyle="->"))
                    plt.text(0.05, 0.95, 'IceCube Preliminary', fontsize=14,
                             transform=plt.gca().transAxes, color='r')
                    _ = f'{outpath}/{nufilename}_truex_truey_hknot{clabel}{wlabel}'
                    os.makedirs(_, exist_ok=True)
                    plt.savefig(f'{_}/k{k}.png', bbox_inches='tight')


def main():
    parser = argparse.ArgumentParser(
        description='Create lowlevel plots')
    parser.add_argument('inputs', nargs='+', help='input hd5')

    parser.add_argument('-o', '--out', default='/data/user/tvaneede/GlobalFit/reco_processing/performance/output/v8.0',
                        type=str, help='output path')
    args = parser.parse_args()

    # nufiles = sys.argv[1:]
    nufiles = args.inputs

    for nufile in nufiles:

        nufilename = os.path.splitext(os.path.basename(nufile))[0]
        outpath = f"{args.out}/{nufilename}"
        os.system(f"mkdir -p {outpath}")

        print("Running nufile", nufile)
        print("nufilename", nufilename)
        print("outpath", outpath)

        lowlevel(nufile = nufile, nufilename = nufilename, outpath = outpath)


if __name__ == '__main__':
    # plt.style.use('present')
    main()
