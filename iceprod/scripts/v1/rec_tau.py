#!/usr/bin/env python3
import os
import argparse
from importlib.metadata import version

from pprint import pformat
import numpy as np

from icecube import dataio
from icecube import (icetray,
                     dataclasses,
                     photonics_service,
                     mue)  # noqa: F401
from icecube.icetray import I3Tray, I3Units
from icecube.phys_services.which_split import which_split
from icecube.millipede import HighEnergyExclusions
from icecube.spline_reco import SplineMPE
from icecube.level3_filter_cascade.level3_Recos import SPEFit

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


def print_frameid(frame):
    eventid = frame['I3EventHeader'].event_id
    print("*******Currently processing frame %s*******" %eventid)


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
    parser.add_argument('--corner', default=False, action='store_true',
                        help='make mcmc corner plots')
    parser.add_argument('--unfold', default=False, action='store_true',
                        help='unfold expectations from reconstructed particle')
    parser.add_argument('--plot-minq', default=10., type=float,
                        help='minq for plot')
    parser.add_argument('--earlypulses', default=False, action='store_true',
                        help='create a mask of early pulses and use for all steps')
    parser.add_argument('--skyit', default=0, type=int,
                        help='number of seeds for it. reco with skymap (expert)')
    parser.add_argument('--skymin', default='imigrad', choices=('imigrad', 'migrad'),
                        help='pick a minimizer to use for the final step in skymap (expert)')

    args = parser.parse_args()
    icetray.set_log_level(args.loglevel)

    cascade_service = define_splines(args.icemodel,
                                     args.tilt,
                                     args.effd,
                                     args.effp,
                                     args.qepsilon,
                                     args.tsig)

    wrapperfn = TaupedeWrapper
    specifier = 'TaupedeFit'
    loss_vector_suffix = 'Particles'
    iterations = args.iterations if args.iterations is not None else 2

    tray = I3Tray()
    tray.Add('I3Reader', Filenamelist=args.infiles)
    tray.Add(sane, split_names=args.splits)

    tray.Add(print_frameid)

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
        tray.Add(druth, hypo="tau", If=lambda frame: not frame.Has('cc'))
    else:
        tray.Add(truth, hypo="tau", If=lambda frame: not frame.Has('cc'))
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
    print(f"cleaning pulses with {args.residual} residual")
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

    if args.ibr:
        sfx += "_ibr"
    if args.idc:
        sfx += "_idc"

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

    prefs = [_ for tup in [[f'TaupedeFit_{mini}_{sfx}',
                            f'MonopodFit_{mini}_{sfx}']
                           for mini in minis]
             for _ in tup]
    tray.Add(preferred,
             i3_particles_fitparams=[(_, f'{_}FitParams') for _ in prefs],
             If=lambda f: len(prefs) > 0 and any([f.Has(_) for _ in prefs]))

    ###
    ### Let's rename
    ###
    print( prefs )

    print("running HESE, with printing modules")      
    from segments.MillipedeWrapper import MillipedeWrapper
            
    # energy definition
    gcdfilepath = "/cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz"
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

    print(sfx)

    # track reco
    tray.Add('I3OMSelection<I3RecoPulseSeries>', 'omselection_HESE',
        InputResponse = 'SRT' + "SplitInIcePulses",
        OmittedStrings = [79,80,81,82,83,84,85,86], # deepcore strings
        OutputOMSelection = f'SRTSplitInIcePulses_BadOMSelectionString_{sfx}',
        OutputResponse = f"SRTSplitInIcePulses_IC_Singles_{sfx}")
    
    tray.Add(SPEFit, f'SPEFit16_{sfx}',
            Pulses = f"SRTSplitInIcePulses_IC_Singles_{sfx}",
            Iterations = 16)

    del millipede_params["PhotonsPerBin"] # also input to MillipedeWrapper next, gives error if entered twice

    # HESE millipede
    tray.Add(MillipedeWrapper, f'HESEMillipedeFit_{sfx}',
        seed_cascade = f'MonopodFit_iMIGRAD_{sfx}', 
        seed_tau = f'TaupedeFit_iMIGRAD_{sfx}',
        seed_track =  f'SPEFit16_{sfx}',
        PhotonsPerBin = 0,
        ShowerSpacing = 5,
        innerboundary=550,
        outerboundary=650,
        outeredge_x=outeredge_x,
        outeredge_y=outeredge_y,
        **millipede_params)

    # rename
    tray.Add('Rename', 
             Keys=['SRTSplitInIcePulses_IC_Singles', f'SRTSplitInIcePulses_IC_Singles_{sfx}',
                   'PreferredFit_key', f'PreferredFit_key_{sfx}',
                   'PreferredFit', f"PreferredFit_{sfx}"])
    
    if args.loglevel not in ['debug', 'trace']:
        tray.Add('Delete', keystarts=['seed_'])
    if not args.qs:
        tray.Add("I3OrphanQDropper")
    tray.AddModule('I3Writer',
                   'writer',
                   filename=args.out,
                   DropOrphanStreams=[icetray.I3Frame.DAQ, icetray.I3Frame.Stream('M'), icetray.I3Frame.TrayInfo],
                   streams=[icetray.I3Frame.TrayInfo,
                            icetray.I3Frame.Physics,
                            icetray.I3Frame.Simulation,
                            icetray.I3Frame.Stream('M'),
                            icetray.I3Frame.Stream('X'),
                            icetray.I3Frame.DAQ])
    if args.nframes is None:
        print("processing all frames")
        tray.Execute()
    else:
        print("processing nframes", args.nframes)
        tray.Execute(args.nframes)
    tray.PrintUsage()


if __name__ == '__main__':
    main()
