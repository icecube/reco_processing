#!/usr/bin/env python3
import os
import argparse
from importlib.metadata import version

from pprint import pformat
import numpy as np

from icecube import dataio
from icecube import (icetray,
                     photonics_service,
                     mue)  # noqa: F401
from icecube.icetray import I3Tray, I3Units
from icecube.phys_services.which_split import which_split
from icecube.millipede import HighEnergyExclusions
from icecube.spline_reco import SplineMPE

# for level 3 muon (pulse cleaning needed for splinempe)
from icecube import level3_filter_muon  # noqa: F401

# for srt cleaning
from icecube.STTools.seededRT.configuration_services import I3DOMLinkSeededRTConfigurationService

# for gulliver
from icecube import lilliput
from icecube.gulliver_modules import gulliview

from snowflake import library, unfold
from reco import skymap, dom
from reco.masks import (earlypulses,
                        maskdc,
                        maskunhits,
                        maskstrings,
                        maskdust,
                        pulse_cleaning)
from reco.truth import truth, druth
from reco.mlpd import (MonopodWrapper,
                       TaupedeWrapper,
                       MillipedeWrapper,
                       preferred,
                       define_splines)
from reco.seed import default_seeds


def sane(frame, split_names):
    for split_name in split_names:
        if which_split(split_name=split_name)(frame):
            return True
    return False


def fixed_dir(filelist, isdata, hypo, split_names, nframes=None):
    truths = []

    def extract(frame):
        truths.append(frame['cc'].dir)
    tray = I3Tray()
    tray.Add('I3Reader', Filenamelist=filelist)
    tray.Add(sane, split_names=split_names)
    if isdata:
        tray.Add(druth, hypo=hypo)
    else:
        tray.Add(truth, hypo=hypo)
    tray.Add(extract)
    if nframes is None:
        tray.Execute()
    else:
        tray.Execute(nframes)
    if len(set([(_.zenith, _.azimuth) for _ in truths])) != 1:
        icetray.logging.log_warn(
            'The number of extracted, unique true dirs is not 1, not updating stepXYZ')
        return None
    return truths[0]


def main():
    """ run reco or emc with a variety of settings
    """
    parser = argparse.ArgumentParser(
        description='A program to run monopod/millipede/taupede/splinempe reco',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('infiles', nargs='+', help='Input i3 files note that GCD frames must be at the beginning')
    parser.add_argument('-V', '--version', action='version',
                        version=version('reco'))
    parser.add_argument('--log', default='notice',
                        dest='loglevel',
                        choices=('trace',
                                 'debug',
                                 'info',
                                 'notice',
                                 'warn',
                                 'error',
                                 'fatal'),
                        help='Set the logging level')
    parser.add_argument('-o', '--out', default='rec.i3.zst', required=True,
                        help='path to output .i3.[zst|gz|bz2] file')
    parser.add_argument('--isdata', default=False, action='store_true',
                        help='running on data')
    parser.add_argument('--nframes', type=int, default=None,
                        help='number of frames to process')
    parser.add_argument('-S', '--splits', default=['InIceSplit',], nargs='+',
                        help='which P-frame splits to process')
    parser.add_argument('--qs', default=False, action='store_true',
                        help='keep all Q-frames even if orphaned')
    parser.add_argument('--hypo', default='cascade', choices=('cascade', 'track', 'tau'),
                        help='hypothesis for reconstruction, based on which a sequence '
                        'segment of Monopod (cascade) <- Taupede (tau) <- Millipede '
                        '(track) is run with the former seeding the latter')
    parser.add_argument('-p', '--pulse_type', type=str,
                        default='SplitInIcePulses',
                        help='specify the pulse_type type (default SplitInIcePulses)')
    parser.add_argument('-s', '--seed', default=None, nargs='+',
                        help='user specified seed(s), passed based on --chain')
    parser.add_argument('-c', '--chain', default=1, choices=(0, 1, 2), type=int,
                        help='0 no chain, 1 full chain, 2 chain but no amplitude fit')
    parser.add_argument('-I', '--iterations', default=None, type=int,
                        help='the number of iterations passed to I3IterativeFitter '
                        '(or I3SimpleFitter if set to 1). By default, set based on '
                        'the --hypo.')
    parser.add_argument('--icemodel', choices=('1', 'mie', 'lea', '3.2.1',
                                               'bfr-v2', 'ftp-v1'),
                        default='ftp-v1', help='The ice model to use for reconstruction.')
    parser.add_argument('--tilt', default=False, action='store_true',
                        help='use the tiltTableDir, based on --icemodel')
    parser.add_argument('--effd', default=False, action='store_true',
                        help='use the effectivedistancetable, based on --icemodel ')
    parser.add_argument('--effp', default=False, action='store_true',
                        help='use the effectivedistancetable for prob and tmod, based on --icemodel')
    parser.add_argument('--qepsilon', type=float, default=1.,
                        help='quantile above which use double precision')
    parser.add_argument('--tsig', type=float, default=0.,
                        help='jitter in [ns] for B-spline convolution')
    parser.add_argument('--bdthres', type=float, default=15,
                        help='bright DOMs threshold')
    parser.add_argument('--relerr', type=float, default=0.05,
                        help='relative error for LLH')
    parser.add_argument('--binsigma', default=np.nan, type=float,
                        help='set the binsigma parameter for BBlocks')
    parser.add_argument('--mintimewidth', default=16, type=float,
                        help='set the min time width parameter for millipede')
    parser.add_argument('--residual', type=float, default=1500 *
                        I3Units.ns, help='time residual for PulseCleaning')
    parser.add_argument('--idc', default=False, action='store_true',
                        help='include DeepCore DOMs')
    parser.add_argument('--isat', default=False, action='store_true',
                        help='include Saturated DOMs')
    parser.add_argument('--ibr', default=False, action='store_true',
                        help='include Bright DOMs')
    parser.add_argument('--itw', default=False, action='store_true',
                        help='include Saturation/CalibrationErrata windows')
    parser.add_argument('--nouh', default=False, action='store_true',
                        help='exclude unhit doms')
    parser.add_argument('--compare', default=False, action='store_true',
                        help='run to compare')
    parser.add_argument('--toygen2', default=False, action='store_true',
                        help='make a toy gen2 out of IC by skipping every other string')
    parser.add_argument('--sparseuh', default=False, action='store_true',
                        help='keep a sparse array of unhit DOMs')
    parser.add_argument('--excldust', default=False, action='store_true',
                        help='exclude DustLayerDOMs')
    parser.add_argument('--migrad', default=False, action='store_true',
                        help='run reco with MIGRAD')
    parser.add_argument('--simplex', default=False, action='store_true',
                        help='run reco with SIMPLEX')
    parser.add_argument('--imigrad', default=False, action='store_true',
                        help='run reco with iminuit MIGRAD')
    parser.add_argument('--isimplex', default=False, action='store_true',
                        help='run reco with iminuit SIMPLEX')
    parser.add_argument('--lbfgsb', default=False, action='store_true',
                        help='run reco with LBFGSB')
    parser.add_argument('--emc', default=False, action='store_true',
                        help='run emc')
    parser.add_argument('--nmc', default=False, action='store_true',
                        help='run nmc')
    parser.add_argument('--corner', default=False, action='store_true',
                        help='make mcmc corner plots')
    parser.add_argument('--gulliview', default=False, action='store_true',
                        help='make gulliview plots')
    parser.add_argument('--unfold', default=False, action='store_true',
                        help='unfold expectations from reconstructed particle')
    parser.add_argument('--plot', default=False, action='store_true',
                        help='plot pulses and expectations if they exist')
    parser.add_argument('--plot-minq', default=10., type=float,
                        help='minq for plot')
    parser.add_argument('--earlypulses', default=False, action='store_true',
                        help='create a mask of early pulses and use for all steps')
    parser.add_argument('--splinempe', default=False, action='store_true',
                        help='run splinempe max reco')
    parser.add_argument('--skymap', default=False, action='store_true',
                        help='run skymap seeded with truth, then use as seed for it. reco (expert)')
    parser.add_argument('--skyit', default=0, type=int,
                        help='number of seeds for it. reco with skymap (expert)')
    parser.add_argument('--skymin', default='imigrad', choices=('imigrad', 'migrad'),
                        help='pick a minimizer to use for the final step in skymap (expert)')
    parser.add_argument('--evegen', default=False, action='store_true',
                        help='try run reco with event-generator (WIP)')
    parser.add_argument('--HESE', default=False, action='store_true',
                        help='running HESE Millipede for 3 topologies')

    args = parser.parse_args()
    icetray.set_log_level(args.loglevel)

    cascade_service = define_splines(args.icemodel,
                                     args.tilt,
                                     args.effd,
                                     args.effp,
                                     args.qepsilon,
                                     args.tsig)
    if args.hypo == 'tau':
        wrapperfn = TaupedeWrapper
        specifier = 'TaupedeFit'
        loss_vector_suffix = 'Particles'
        iterations = args.iterations if args.iterations is not None else 2
    elif args.hypo == 'track':
        wrapperfn = MillipedeWrapper
        specifier = 'MillipedeFit'
        loss_vector_suffix = 'Particles'
        iterations = args.iterations if args.iterations is not None else 1
    else:
        wrapperfn = MonopodWrapper
        specifier = 'MonopodFit'
        loss_vector_suffix = ''
        iterations = args.iterations if args.iterations is not None else 4

    tray = I3Tray()
    tray.Add('I3Reader', Filenamelist=args.infiles)
    tray.Add(sane, split_names=args.splits)

    # apply HESE selection
    if args.HESE:
        print("applying hese selection")
        tray.Add(lambda frame : 'HESE_VHESelfVeto' in frame and not frame['HESE_VHESelfVeto'].value)
        tray.Add(lambda frame : 'HESE_CausalQTot' in frame and frame['HESE_CausalQTot'].value >= 6000)

    if args.isdata:
        rde_map = library.get_rde_map(os.path.expandvars(
            '$I3_BUILD/ice-models/resources/models/PPCTABLES/misc/eff-f2k.FTP125max'))
        tray.Add(library.update_dom_eff, rde_map=rde_map,
                 Streams=[icetray.I3Frame.Calibration])
        # rerun for updated calibration errata
        _raw = 'InIceRawData'
        tray.Add('Delete',
                 keys=['CalibratedWaveformRange',
                       'CalibrationErrata',
                       'SaturationWindows'],
                 If=lambda f: f.Has(_raw))
        tray.Add('I3WaveCalibrator',
                 Launches=_raw,
                 If=lambda f: f.Has(_raw))
        tray.Add('I3PMTSaturationFlagger',
                 If=lambda f: f.Has(_raw))
        tray.Add(druth, hypo=args.hypo, If=lambda frame: not frame.Has('cc'))
    else:
        tray.Add(truth, hypo=args.hypo, If=lambda frame: not frame.Has('cc'))
    tray.Add('Delete', keys=['BrightDOMs',
                             'SaturatedDOMs',
                             'DeepCoreDOMs',
                             'CausalQTot'])
    if args.earlypulses:
        epkey = f'{args.pulse_type}_early'
        tray.Add(earlypulses, inpulses=args.pulse_type, outpulses=epkey)
        args.pulse_type = epkey

    Seed = tray.Add(default_seeds,
                    pulse_type=args.pulse_type)
    if args.seed is not None:
        Seed = args.seed

    tray.Add(maskdc, origpulses=args.pulse_type, maskedpulses=f'{args.pulse_type}IC',
             If=lambda frame: not frame.Has(f'{args.pulse_type}IC'))
    pulses_for_reco = args.pulse_type if args.idc else f'{args.pulse_type}IC'
    tray.Add(pulse_cleaning,
             Pulses=pulses_for_reco, Residual=args.residual,
             If=lambda frame: not frame.Has(f"{pulses_for_reco}PulseCleaned"))
    excludedDOMs = tray.Add(HighEnergyExclusions,
                            Pulses=pulses_for_reco,
                            BrightDOMThreshold=args.bdthres,
                            ExcludeDeepCore=False if args.idc else 'DeepCoreDOMs',
                            ExcludeBrightDOMs=False if args.ibr else 'BrightDOMs',
                            ExcludeSaturatedDOMs=False if args.isat else 'SaturatedDOMs',
                            BadDomsList='BadDomsList',
                            CalibrationErrata='CalibrationErrata',
                            SaturationWindows='SaturationWindows')
    # exclude the late pulse time windows
    excludedDOMs.append(f"{pulses_for_reco}PulseCleanedTimeWindows")

    # this isn't placed in by default as SaturatedDOMs are excluded fully
    # here we decide based on --itw
    excludedDOMs.append('SaturationWindows')

    if args.itw:
        # this can be used for testing against MCPEs
        excludedDOMs.remove('CalibrationErrata')
        excludedDOMs.remove('SaturationWindows')

    if args.toygen2:
        tray.Add(maskstrings, output='OtherHalf',
                 streams=[icetray.I3Frame.Geometry])
        excludedDOMs.append('OtherHalf')
    if args.sparseuh:
        tray.Add(maskunhits, output='OtherUnhits',
                 pulses=f"{pulses_for_reco}PulseCleaned")
        excludedDOMs.append('OtherUnhits')
    if args.excldust:
        tray.Add(maskdust, output='DustLayerDOMs',
                 streams=[icetray.I3Frame.Geometry])
        excludedDOMs.append('DustLayerDOMs')
    millipede_params = {'Pulses': f'{pulses_for_reco}PulseCleaned',
                        'CascadePhotonicsService': cascade_service,
                        'MuonPhotonicsService': None,
                        'ExcludedDOMs': excludedDOMs,
                        'ReadoutWindow': f'{pulses_for_reco}PulseCleanedTimeRange',
                        'PartialExclusion': True,
                        'PhotonsPerBin': 0,
                        'UseUnhitDOMs': not args.nouh,
                        'MinTimeWidth': args.mintimewidth,
                        'BinSigma': args.binsigma,
                        'RelUncertainty': args.relerr,}
    icetray.logging.log_info(pformat(millipede_params),
                             __name__)

    if not np.isnan(args.binsigma):
        sfx = f'BS{args.binsigma}'
    else:
        sfx = 'PPB0'

    if args.compare:
        cascade_services = [cascade_service]
        suffixes = ['']
        # mie
        cascade_services.append(define_splines('mie',
                                               False,
                                               False,
                                               False,
                                               qepsilon=args.qepsilon))
        suffixes.append('_mie')

        # ftp-v1 no tilt
        cascade_services.append(define_splines('ftp-v1',
                                               False,
                                               True,
                                               True,
                                               qepsilon=args.qepsilon))
        suffixes.append('_flat')

        # ftp-v1 no tilt no anisotropy
        cascade_services.append(define_splines('ftp-v1',
                                               False,
                                               False,
                                               False,
                                               qepsilon=args.qepsilon))
        suffixes.append('_bulk')

        for _cs, _trail in zip(cascade_services, suffixes):
            millipede_params['CascadePhotonicsService'] = _cs
            tray.Add(wrapperfn,
                     f'iMIGRAD_{sfx}{_trail}',
                     Seed=Seed,
                     Minimizer='iMIGRAD',
                     Unfold=args.unfold,
                     Chain=args.chain,
                     Iterations=iterations,
                     **millipede_params)
        _prefs = [f'MillipedeFit_iMIGRAD_{sfx}',
                  f'TaupedeFit_iMIGRAD_{sfx}',
                  f'MonopodFit_iMIGRAD_{sfx}']
        tray.Add(preferred,
                 i3_particles_fitparams=[(_, f'{_}FitParams') for _ in _prefs],
                 If=lambda f: any([f.Has(_) for _ in _prefs]))

    minis = [_ for _ in ['MIGRAD',
                         'iMIGRAD',
                         'SIMPLEX',
                         'iSIMPLEX',
                         'LBFGSB'] if vars(args)[_.lower()]]
    for mini in minis:
        tray.Add(wrapperfn,
                 f'{mini}_{sfx}',
                 Seed=Seed,
                 Minimizer=mini,
                 Unfold=args.unfold,
                 Chain=args.chain,
                 Iterations=iterations,
                 **millipede_params)

        # Plot the likelihood space around the minimum.
        seeder = lilliput.segments.add_seed_service(
            tray,
            millipede_params['Pulses'],
            [f'{specifier}_{mini}_{sfx}'])
        minispec = mini.lower()
        if args.ibr:
            minispec += '.ibr'
        if args.idc:
            minispec += '.idc'
        if args.isat:
            minispec += '.isat'
        if args.relerr:
            minispec += f'.relerr{args.relerr:.2f}'
        if args.gulliview:
            tray.Add(gulliview.GulliView,
                     SeedService=seeder,
                     Parametrization=f'{specifier}_{mini}_{sfx}_parametrization',
                     LogLikelihood=f'{specifier}_{mini}_{sfx}_likelihood',
                     StepSize=0.5,
                     WithGradients=True,
                     Filename=f'out/gulliview/{minispec}')

        if args.emc:
            from reco.mcmc import emc
            cpn = f'out/corner/emc/{minispec}' if args.corner else None
            tray.Add(emc.EMC,
                     Burnin=100,
                     NSteps=500,
                     NWalkers=20,
                     SeedService=seeder,
                     Parametrization=f'{specifier}_{mini}_{sfx}_parametrization',
                     LogLikelihood=f'{specifier}_{mini}_{sfx}_likelihood',
                     CornerPlotName=cpn,
                     CornerPlotTruth='cc',
                     OutputName='EMC')

        if args.nmc:
            from reco.mcmc import nmc
            cpn = f'out/corner/nmc/{minispec}' if args.corner else None
            tray.Add(nmc.NMC,
                     SeedService=seeder,
                     NLive=1000,
                     Tolerance=100.,
                     # DeclineFactor=0.01,
                     MaxIterations=10000,
                     Parametrization=f'{specifier}_{mini}_{sfx}_parametrization',
                     LogLikelihood=f'{specifier}_{mini}_{sfx}_likelihood',
                     CornerPlotName=cpn,
                     CornerPlotTruth='cc',
                     OutputName='NMC')

        if args.plot:
            from reco import plotting
            tray.Add(plotting.plot_pulses,
                     figdir='out/pulses',
                     pulse_type=millipede_params['Pulses'],
                     exq_key=f'{specifier}_{mini}_{sfx}_{specifier}_{mini}_{sfx}{loss_vector_suffix}_ExQ',
                     obq_key=f'{specifier}_{mini}_{sfx}_{specifier}_{mini}_{sfx}{loss_vector_suffix}_ObQ',
                     min_q=args.plot_minq)

    prefs = [_ for tup in [[f'MillipedeFit_{mini}_{sfx}',
                            f'TaupedeFit_{mini}_{sfx}',
                            f'MonopodFit_{mini}_{sfx}']
                           for mini in minis]
             for _ in tup]
    tray.Add(preferred,
             i3_particles_fitparams=[(_, f'{_}FitParams') for _ in prefs],
             If=lambda f: len(prefs) > 0 and any([f.Has(_) for _ in prefs]))

    if args.skymap:
        tray.Add(skymap.skymap,
                 'skymap',
                 input_particle='cc',
                 hypo=args.hypo,
                 minimizer=args.skymin,
                 truedir=fixed_dir(args.infiles,
                                   args.isdata,
                                   args.hypo,
                                   args.splits,
                                   args.nframes,
                                   ),
                 **millipede_params)
        s2p = 'Millipede2ndPass'
        m3p = 'Millipede3rdPass'

        finer_steps_dir = dict(StepX=2.*I3Units.m,
                               StepY=2.*I3Units.m,
                               StepZ=2.*I3Units.m,
                               StepZenith=1.*I3Units.degree,
                               StepAzimuth=1.*I3Units.degree,
                               StepT=5.*I3Units.ns)
        if args.hypo == 'track':
            pfac = 'MuMillipedeParametrizationFactory'
            finer_steps_dir.update(
                dict(MuonSpacing=0.,
                     ShowerSpacing=2.5*I3Units.m,
                     Boundary=650*I3Units.m))
        elif args.hypo == 'tau':
            pfac = 'TauMillipedeParametrizationFactory'
            vertexBounds = [-200*I3Units.m, 200*I3Units.m]
            finer_steps_dir.update(
                dict(StepLinL=3.*I3Units.m,
                     RelativeBoundsX=vertexBounds,
                     RelativeBoundsY=vertexBounds,
                     RelativeBoundsZ=vertexBounds,
                     BoundsLinL=[0, 2000]))
        else:
            pfac = 'I3SimpleParametrizationFactory'

        tray.AddService('I3BasicSeedServiceFactory', 'secondFitSeed',
                        FirstGuesses=[s2p],
                        TimeShiftType='TNone',
                        PositionShiftType='None')
        tray.AddService(pfac, 'fineStepsWDir',
                        **finer_steps_dir)
        if args.skyit == 0:
            tray.AddModule('I3SimpleFitter',
                           SeedService='secondFitSeed',
                           OutputName='Millipede3rdPass',
                           NonStdName='Millipede3rdPassParticles',
                           Parametrization='fineStepsWDir',
                           LogLikelihood='millipedellh',
                           Minimizer=args.skymin,
                           If=lambda frame: not frame.Has('Millipede3rdPass'))
        elif args.skyit > 0:
            tray.AddModule('I3IterativeFitter',
                           SeedService='secondFitSeed',
                           OutputName='Millipede3rdPass',
                           NonStdName='Millipede3rdPassParticles',
                           Parametrization='fineStepsWDir',
                           LogLikelihood='millipedellh',
                           RandomService="SOBOL",
                           NIterations=args.skyit,
                           Minimizer=args.skymin,
                           If=lambda frame: not frame.Has('Millipede3rdPass'))
        else:
            raise RuntimeError('wtf skyit is negative')

        if args.unfold:
            tray.Add(unfold.Unfold,
                     Loss_Vector_Name=f'{m3p}{loss_vector_suffix}',
                     FitName=m3p,
                     **{k: millipede_params[k] for k in ('ExcludedDOMs',
                                                         'Pulses',
                                                         'CascadePhotonicsService')})
            tray.Add(unfold.Unfold,
                     Loss_Vector_Name=f'{s2p}{loss_vector_suffix}',
                     FitName=s2p,
                     **{k: millipede_params[k] for k in ('ExcludedDOMs',
                                                         'Pulses',
                                                         'CascadePhotonicsService')})
            tray.Add(dom.dllh,
                     key0=s2p,
                     key1=m3p,
                     loss_vector_suffix=loss_vector_suffix)

        if args.plot:
            tray.Add(plotting.plot_pulses,
                     figdir='out/pulses',
                     pulse_type=millipede_params['Pulses'],
                     exq_key=f'{m3p}_{m3p}{loss_vector_suffix}_ExQ',
                     obq_key=f'{m3p}_{m3p}{loss_vector_suffix}_ObQ',
                     min_q=args.plot_minq)
    if args.splinempe:
        tray.Add('Delete', keys=['SplineMPE0',
                                 'SplineMPE0FitParams',
                                 'SplineMPEICMuEXDifferential',
                                 'SplineMPEICMuEXDifferential_list',
                                 'SplineMPEICMuEXDifferential_r',
                                 'SplineMPEICSeed',
                                 'SplineMPEICSeedFitParams',
                                 'SplineMPEICFitParams',
                                 'SplineMPEIC'])
        seededRTConfig = I3DOMLinkSeededRTConfigurationService(
            ic_ic_RTRadius=150.0*I3Units.m,
            ic_ic_RTTime=1000.0*I3Units.ns,
            treat_string_36_as_deepcore=False,
            useDustlayerCorrection=False,
            allowSelfCoincidence=True)
        tray.Add('I3SeededRTCleaning_RecoPulseMask_Module',
                 InputHitSeriesMapName=args.pulse_type,
                 OutputHitSeriesMapName=f"SRT{args.pulse_type}",
                 STConfigService=seededRTConfig,
                 SeedProcedure='HLCCoreHits',
                 NHitsThreshold=2,
                 MaxNIterations=3,
                 Streams=[icetray.I3Frame.Physics],
                 If=lambda frame: not frame.Has(f"SRT{args.pulse_type}"))
        tray.AddModule("StaticDOMTimeWindowCleaning",
                       InputPulses=f"SRT{args.pulse_type}",
                       OutputPulses=f"TWSRT{args.pulse_type}",
                       MaximumTimeDifference=3e3*I3Units.ns,
                       If=lambda frame: frame.Has(f"SRT{args.pulse_type}") and not frame.Has(f"TWSRT{args.pulse_type}"))
        tray.Add(maskdc, origpulses=f"TWSRT{args.pulse_type}", maskedpulses=f"TWSRT{args.pulse_type}IC",
                 If=lambda frame: not frame.Has(f"TWSRT{args.pulse_type}IC"))

        if args.seed is not None:
            splinempe_seeds = args.seed
        elif len(minis) > 0:
            splinempe_seeds = [
                f'{specifier}_{mini}_{sfx}' for mini in minis]
        else:
            splinempe_seeds = ['OnlineL2_SplineMPE',
                               'l2_online_SplineMPE', 'LineFit']

        # muex - differential energy
        tray.Add(SplineMPE,
                 fitname="SplineMPE0",
                 configuration="default",
                 PulsesName=f'TWSRT{args.pulse_type}IC',
                 TrackSeedList=splinempe_seeds)
        tray.Add("muex",
                 pulses=f"TWSRT{args.pulse_type}IC",
                 rectrk="SplineMPE0",
                 result="SplineMPEICMuEXDifferential",
                 detail=True,  # differential
                 energy=True,
                 lcspan=0,
                 badoms="SaturatedDOMs",
                 icedir=os.path.expandvars("$I3_BUILD/mue/resources/ice/sp3"))
        tray.Add(SplineMPE,
                 fitname="SplineMPEIC",
                 configuration="max",
                 PulsesName=f'TWSRT{args.pulse_type}IC',
                 TrackSeedList=["SplineMPE0"],
                 EnergyEstimators=["SplineMPEICMuEXDifferential"])

    if args.evegen:
        # for evegenerator need py3-v4.1.1
        # /data/user/tyuan/temp/tarballs/icetray.main.r24ff21c2.Linux-x86_64.gcc-9.2.0/env-shell.sh
        # source /data/ana/PointSource/DNNCascade/utils/virtualenvs/version-0.0/py3-v4.1.1_tensorflow2.3/bin/activate
        # export PYTHONPATH=$PYTHONPATH:/home/tyuan/.local/lib/python3.7/site-packages
        try:
            from egenerator.ic3.segments import ApplyEventGeneratorReconstruction
            from egenerator.ic3.utils.bright_doms import AddBrightDOMs
            from dnn_reco.ic3.segments import ApplyDNNRecos
            from reco.egen import combine_for_seed, seeder, model_base_dir, dnn_model_names
            tray.Add('Delete',
                     keys=['BrightDOMs'])
            tray.AddModule(AddBrightDOMs, 'AddBrightDOMs')

            # DNN to seed egen
            tray.AddSegment(ApplyDNNRecos, 'ApplyDNNRecoBasic',
                            pulse_key=args.pulse_type,
                            dom_exclusions=[
                                'BrightDOMs', 'SaturationWindows', 'BadDomsList', 'CalibrationErrata'],
                            partial_exclusion=True,
                            model_names=dnn_model_names,
                            output_keys=[
                                f'DNNRecoBasic_{_}' for _ in dnn_model_names],
                            models_dir=os.path.join(
                                model_base_dir, 'dnn_reco'),
                            cascade_key='MCCascade',
                            batch_size=32,
                            ignore_misconfigured_settings_list=['pulse_key'])
            tray.Add(combine_for_seed,
                     prefix='DNNRecoBasic_event_selection_egen_seed')
            tray.Add(combine_for_seed,
                     prefix='DNNRecoBasic_event_selection_cascade')
            tray.Add(
                seeder, i3particle_name='DNNRecoBasic_event_selection_egen_seed')

            # egen fast
            tray.AddSegment(
                ApplyEventGeneratorReconstruction, 'ApplyEventGeneratorReconstructionFast',
                pulse_key=args.pulse_type,
                dom_and_tw_exclusions=['BadDomsList',
                                       'CalibrationErrata', 'SaturationWindows'],
                partial_exclusion=True,
                exclude_bright_doms=False,
                model_names=['cascade_7param_noise_tw_BFRv1Spice321_01'],
                seed_keys=['DNNRecoBasic_event_selection_cascade'],
                output_key='EveGenFit_gtol_10',
                scipy_optimizer_settings={'options': {'gtol': 10}},
                add_circular_err=False,
                add_covariances=False,
                add_goodness_of_fit=False,
                model_base_dir=os.path.join(model_base_dir, 'egenerator'))

            tray.AddSegment(
                ApplyEventGeneratorReconstruction, 'ApplyEventGeneratorReconstruction',
                pulse_key=args.pulse_type,
                dom_and_tw_exclusions=['BadDomsList',
                                       'CalibrationErrata', 'SaturationWindows'],
                partial_exclusion=True,
                exclude_bright_doms=True,
                model_names=['cascade_7param_noise_tw_BFRv1Spice321_01'],
                seed_keys=['DNNRecoBasic_event_selection_egen_seed_original',
                           'EveGenFit_gtol_10_I3Particle'],
                output_key='EveGenFit',
                scipy_optimizer_settings={'options': {'gtol': 1e-3}},
                add_circular_err=True,
                add_covariances=False,
                model_base_dir=os.path.join(model_base_dir, 'egenerator'),
                parameter_boundaries={
                    'cascade_x': [-750, 750],
                    'cascade_y': [-750, 750],
                    'cascade_z': [-800, 750],
                    'cascade_energy': [0, 1e8]})
        except ImportError as e:
            icetray.logging.log_error(str(e), __name__)

    # taken from Neha
    if args.HESE:  
        print("running HESE, with printing modules")      
        from segments.MillipedeWrapper import MillipedeWrapper
        from segments.FinalEventClassification import checkfinaltopology
        from segments.RecoObservables import calculaterecoobservables
                
        # energy definition
        gcdfilepath = "/data/user/tvaneede/GlobalFit/reco_processing/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz"
        gcdfile = dataio.I3File(gcdfilepath)
        frame = gcdfile.pop_frame()
        while 'I3Geometry' not in frame:
            frame = gcdfile.pop_frame()
        geometry = frame['I3Geometry'].omgeo

        strings = [1, 2, 3, 4, 5, 6, 13, 21, 30, 40, 50, 59, 67, 74, 73, 72, 78, 77, 76, 75, 68, 60, 51, 41, 31, 22, 14, 7]

        outerbounds = {}
        cx, cy = [], []
        for string in strings:
            omkey = icetray.OMKey(string, 1)
            # if geometry.has_key(omkey):
            x, y = geometry[omkey].position.x, geometry[omkey].position.y
            outerbounds[string] = (x, y)
            cx.append(x)
            cy.append(y)
        cx, cy = np.asarray(cx), np.asarray(cy)
        order = np.argsort(np.arctan2(cx, cy))
        outeredge_x = cx[order]
        outeredge_y = cy[order]

        # millipede
        millipede_params = {'Pulses': 'SplitInIcePulses', 'PartialExclusion' : False , 'CascadePhotonicsService' : cascade_service, 'ExcludedDOMs': excludedDOMs}
        
        tray.Add(MillipedeWrapper, 'HESEMillipedeFit',
            Seeds = ['MonopodFit_iMIGRAD_PPB0', 'TaupedeFit_iMIGRAD_PPB0', 'CscdL3_SPEFit16'],
            PhotonsPerBin = 5,
            ShowerSpacing = 5,
            innerboundary=550,
            outerboundary=650,
            outeredge_x=outeredge_x,
            outeredge_y=outeredge_y,
            **millipede_params)

        tray.AddModule(calculaterecoobservables,
                        'calc_reco_observables',
                        innerboundary=550,
                        outeredge_x=outeredge_x,
                        outeredge_y=outeredge_y)

        tray.Add(checkfinaltopology)


    if args.loglevel not in ['debug', 'trace']:
        tray.Add('Delete', keystarts=['seed_'])
    if not args.qs:
        tray.Add("I3OrphanQDropper")
    tray.AddModule('I3Writer',
                   'writer',
                   filename=args.out,
                   streams=[icetray.I3Frame.TrayInfo,
                            icetray.I3Frame.Physics,
                            icetray.I3Frame.Simulation,
                            icetray.I3Frame.Stream('M'),
                            icetray.I3Frame.Stream('X'),
                            icetray.I3Frame.DAQ])
    if args.nframes is None:
        tray.Execute()
    else:
        tray.Execute(args.nframes)
    tray.PrintUsage()


if __name__ == '__main__':
    main()
