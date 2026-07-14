#!/usr/bin/sh /cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/icetray-start
#METAPROJECT /cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/${OS_ARCH}/metaprojects/icetray/v1.12.0/
import os
import argparse
import math

import logging
from pprint import pformat
import numpy as np

from icecube import dataclasses, dataio, VHESelfVeto, mue
from icecube.filterscripts import filter_globals
from icecube.filterscripts.offlineL2 import Recalibration
from icecube.icetray import I3Tray, I3Units
from icecube import photonics_service, icetray
from icecube.millipede import HighEnergyExclusions

# for srt cleaning
from icecube.STTools.seededRT.configuration_services import I3DOMLinkSeededRTConfigurationService

# for level 3 muon (pulse cleaning needed for splinempe)
from icecube import level3_filter_muon

# for gulliver
from icecube import lilliput
from icecube.gulliver_modules import gulliview

from snowflake import library, unfold
# from reco import skymap, splinempe, dom
from reco import skymap, dom
from reco.masks import (earlypulses,
                        maskdc,
                        maskunhits,
                        maskstrings,
                        maskdust,
                        pulse_cleaning)
from reco.truth import truth, druth
from reco.mlpd import (#MonopodWrapper,
                       #TaupedeWrapper,
                       #MillipedeWrapper,
                       define_splines)
from reco.seed import (convert_to_track_seed,
                       convert_to_cascade_seed,
                       Level2ReconstructionWrapper,
                       Level3ReconstructionWrapper)

#path_to_plot_directory = '/data/user/zchen/Fittings/analysis/ftp_v3_mc/new_reco/code/'
#sys.path.insert(0, path_to_plot_directory)
from taupede_utils import deletekey, Taupede_ftp

from add_variables import Add_calculated_variables


def print_ftp_output(frame):
    if not frame.Has('I3EventHeader'):
        return
    hdr = frame['I3EventHeader']
    print(f'\n--- Run {hdr.run_id}  Event {hdr.event_id} ---')
    particles_key = 'Taupede_ftpParticles'
    if frame.Has(particles_key):
        particles = frame[particles_key]
        print(f'  {particles_key} ({len(particles)} particles):')
        for i, p in enumerate(particles):
            print(f'    [{i}]  pos=({p.pos.x:.2f}, {p.pos.y:.2f}, {p.pos.z:.2f}) m'
                  f'  zen={math.degrees(p.dir.zenith):.3f} deg'
                  f'  az={math.degrees(p.dir.azimuth):.3f} deg'
                  f'  E={p.energy:.2f} GeV'
                  f'  t={p.time:.2f} ns'
                  f'  L={p.length:.2f} m')
    else:
        print(f'  (no {particles_key} in frame)')
    fitparams_key = 'Taupede_ftpFitParams'
    if frame.Has(fitparams_key):
        fp = frame[fitparams_key]
        print(f'  Stored  logl={fp.logl:.6f}  rlogl={fp.rlogl:.6f}  ndof={fp.ndof}')
    else:
        print(f'  (no {fitparams_key} in frame)')


def print_logl_comparison(frame, eval_key, stored_key, label=''):
    if not frame.Has('I3EventHeader') or not frame.Has(eval_key + 'FitParams'):
        return
    ev = frame[eval_key + 'FitParams']
    label_str = f' ({label})' if label else ''
    print(f'  PyMillipede{label_str}:  logl={ev.logl:.6f}  ndof={ev.ndof}')
    if frame.Has(stored_key):
        st = frame[stored_key]
        print(f'  Delta logl: {ev.logl - st.logl:+.6f}')


def good_frame(frame):
    if frame['I3EventHeader'].sub_event_stream != filter_globals.InIceSplitter:
        return False

    return True


def fixed_dir(filelist, isdata, hypo, nframes=None):
    truths = []

    def pullout(frame):
        truths.append(frame['cc'].dir)
    tray = I3Tray()
    tray.Add('I3Reader', Filenamelist=filelist)
    tray.Add(good_frame)
    if isdata:
        tray.Add(druth, hypo=hypo)
    else:
        tray.Add(truth, hypo=hypo)
    tray.Add(pullout)
    if nframes is None:
        tray.Execute()
    else:
        tray.Execute(nframes)
    if len(set([(_.zenith, _.azimuth) for _ in truths])) != 1:
        logging.warning(
            'The number of extracted, unique true dirs is not 1, not updating stepXYZ')
        return None
    return truths[0]

def makedeletekey(name):
  deletekeylist = []
  for tag in ['forward', 'backward', 'center']:
    fittag = name+'_%s' % (tag)
    fitparticlestag = name+'_%sParticles' % (tag)
    fitparamstag  = name+'_%sFitParams' % (tag)
    recotag = fittag+'reco'
    fitparticlesrecotag = recotag + 'Particles'
    fitparamsrecotag = recotag + 'FitParams'
    seedtag = fittag + 'seed'
    deletekeylist.extend([fittag,recotag,fitparticlestag,fitparticlesrecotag,fitparamstag,fitparamsrecotag,seedtag])
  return deletekeylist


def require_millipede_params(millipede_params):
    required = [
        'Pulses',
        'CascadePhotonicsService',
        'ExcludedDOMs',
        'ReadoutWindow',
    ]
    missing = [key for key in required if key not in millipede_params]
    if missing:
        raise RuntimeError(f"Missing required millipede params: {missing}")


def log_run_summary(args, seed_fit, seed_key, millipede_params):
    summary = {
        'infiles': args.infiles,
        'out': args.out,
        'hypo': args.hypo,
        'pulse_type': args.pulse_type,
        'pulses_for_reco': millipede_params['Pulses'],
        'icemodel': args.icemodel,
        'tilt': args.tilt,
        'effd': args.effd,
        'effp': args.effp,
        'seed_fit': seed_fit,
        'seed_key': seed_key,
        'taupede_segment': 'Taupede_ftp',
    }
    logging.info('Reconstruction run summary:\n%s', pformat(summary))

def main():
    """ run reco or emc with a variety of settings
    """
    parser = argparse.ArgumentParser(
        description='This program will optionally run monopod/millipede/taupede/splinempe reco')
    parser.add_argument('infiles', nargs='+')
    parser.add_argument('-o', '--out', default='rec.i3.zst')
    parser.add_argument('-s', '--seed', default=None, nargs='+',
                        help='user specified seeds for the *pod based recos')
    parser.add_argument('--isdata', default=False, action='store_true',
                        help='running on data')
    parser.add_argument('--hypo', default='cascade', choices=('cascade', 'track', 'tau','old_tau'),
                        help='process different Millipede hypo')
    parser.add_argument('--binsigma', default=np.nan, type=float,
                        help='set the binsigma parameter for BBlocks')
    parser.add_argument('--mintimewidth', default=8, type=float,
                        help='set the min time width parameter for millipede')
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
    parser.add_argument('--migrad', default=False, action='store_true',
                        help='run reco with MIGRAD')
    parser.add_argument('--simplex', default=False, action='store_true',
                        help='run reco with SIMPLEX')
    parser.add_argument('--imigrad', default=False, action='store_true',
                        help='run reco with iminuit MIGRAD')
    parser.add_argument('--unfold', default=False, action='store_true',
                        help='unfold expectations from reconstructed particle')
    parser.add_argument('--plot', default=False, action='store_true',
                        help='plot pulses and expectations if they exist')
    parser.add_argument('--plot-minq', default=10., type=float,
                        help='minq for plot')
    parser.add_argument('--nframes', type=int, default=None,
                        help='number of frames to process')
    parser.add_argument('--residual', type=float, default=1500 *
                        I3Units.ns, help='time residual for PulseCleaning')
    parser.add_argument('--bdthres', type=float, default=15,
                        help='bright DOMs threshold')
    # original default relerr=0
    parser.add_argument('--relerr', type=float, default=0.05,
                        help='relative error for LLH')
    parser.add_argument('--qepsilon', type=float, default=1.,
                        help='quantile above which use double precision')
    parser.add_argument('--tsig', type=float, default=0.,
                        help='jitter in [ns] for B-spline convolution')
    parser.add_argument('-p', '--pulse_type', dest='pulse_type', type=str,
                        default='SplitInIcePulses',
                        help='specify the pulse_type type (default SplitInIcePulses)')
    parser.add_argument('--icemodel', choices=('1', 'mie', 'lea', '3.2.1',
                                               'bfr-v2', 'ftp-v1'),
                        default='ftp-v1', help='The ice model to use for reconstruction.')
    parser.add_argument('--tilt', default=False, action='store_true',
                        help='use the tiltTableDir, based on --icemodel')
    parser.add_argument('--effd', default=False, action='store_true',
                        help='use the effectivedistancetable, based on --icemodel ')
    parser.add_argument('--effp', default=False, action='store_true',
                        help='use the effectivedistancetable for prob and tmod, based on --icemodel')

    parser.add_argument('--tau_mode', default = 'normal',choices=('normal','lengthbound','step'))
    parser.add_argument('--dry-run-config', default=False, action='store_true',
                        help='print the derived reconstruction configuration and exit before adding reconstruction fits')
    parser.add_argument('--eval-file', default=None,
                        help='i3 file with particles for an additional likelihood evaluation')
    parser.add_argument('--eval-particles-key', default=None,
                        help='I3VectorI3Particle key in --eval-file to evaluate')

    args = parser.parse_args()

    ext_particles_map = {}
    if args.eval_file and args.eval_particles_key:
        print(f'Loading {args.eval_particles_key} from {args.eval_file} ...')
        ef = dataio.I3File(args.eval_file)
        while ef.more():
            frame = ef.pop_frame()
            if frame.Stop != icetray.I3Frame.Physics or not frame.Has('I3EventHeader'):
                continue
            hdr = frame['I3EventHeader']
            if frame.Has(args.eval_particles_key):
                ext_particles_map[(hdr.run_id, hdr.event_id)] = list(frame[args.eval_particles_key])
        ef.close()
        print(f'  Loaded {len(ext_particles_map)} event(s).')
        for (run, evt), particles in ext_particles_map.items():
            print(f'  Run {run}  Event {evt}  ({len(particles)} particles):')
            for i, p in enumerate(particles):
                print(f'    [{i}]  pos=({p.pos.x:.2f}, {p.pos.y:.2f}, {p.pos.z:.2f}) m'
                      f'  zen={math.degrees(p.dir.zenith):.3f} deg'
                      f'  az={math.degrees(p.dir.azimuth):.3f} deg'
                      f'  E={p.energy:.2f} GeV'
                      f'  t={p.time:.2f} ns'
                      f'  L={p.length:.2f} m')

    cascade_service = define_splines(args.icemodel,
                                     args.tilt,
                                     args.effd,
                                     args.effp,
                                     args.qepsilon,
                                     args.tsig)
    
    Seed = 'CombinedCascadeSeed_L3'
    
    from taupede_tianlu import MonopodWrapper
    wrapperfn = MonopodWrapper
    specifier = 'MonopodFit'
    loss_vector_suffix = ''

    
    tray = I3Tray()
    tray.Add('I3Reader', Filenamelist=args.infiles)
    tray.Add(good_frame)
    if args.isdata:
        rde_map = library.get_rde_map(os.path.expandvars(
            f'$I3_BUILD/ice-models/resources/models/PPCTABLES/misc/eff-f2k.FTP125max'))
        tray.Add(library.update_dom_eff, rde_map=rde_map, Streams=[icetray.I3Frame.Calibration])
        # rerun for updated calibration errata
        _raw = 'InIceRawData'
        #tray.Add('Delete',
        #         keys=['CalibratedWaveformRange', 'CalibrationErrata', 'SaturationWindows','CalibratedWaveforms'],
        #         If=lambda f: f.Has(_raw))
        #tray.Add(Recalibration.InIceCalibration, InputLaunches=_raw,
        #         OutputPulses='InIcePulses_temp',
        #         WavedeformSPECorrections=True,
        #         If=lambda f: f.Has(_raw))
        #tray.Add('Delete', keys=['InIcePulses_temp'])
        tray.Add('Delete',
                 keys=['CalibratedWaveformRange',
                       'CalibrationErrata',
                       'SaturationWindows',
                       'CalibratedWaveforms'],
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
    
    tray.AddModule('I3LCPulseCleaning', 'cleaning',
                   OutputHLC=args.pulse_type+'HLC',
                   OutputSLC='', Input=args.pulse_type,
                   If=lambda frame: not frame.Has(args.pulse_type+'HLC'))
    tray.AddModule('VHESelfVeto',
                   Pulses=args.pulse_type+'HLC',
                   VetoThreshold=3,
                   VertexThreshold=250,
                   If=lambda frame: not frame.Has('VHESelfVeto'))
    # this only runs if the previous module did not return anything
    tray.AddModule('VHESelfVeto', 'selfveto-emergency-lowen-settings',
                   # usually this is at 250pe - use a much lower setting here to get a seed
                   VertexThreshold=5.,
                   Pulses=args.pulse_type+'HLC',
                   OutputBool='VHESelfVeto_meaningless_lowen',
                   OutputVertexTime='VHESelfVetoVertexTime',
                   OutputVertexPos='VHESelfVetoVertexPos',
                   If=lambda frame: (frame.Stop == icetray.I3Frame.Physics) and not frame.Has("VHESelfVeto"))
    tray.AddModule('HomogenizedQTot',
                   Pulses=args.pulse_type,
                   Output='CausalQTot',
                   VertexTime='VHESelfVetoVertexTime')
    
    if args.seed is None:
        tray.Add(Level2ReconstructionWrapper,
                 'level2reco',
                 Pulses=args.pulse_type)
        tray.Add(Level3ReconstructionWrapper,
                 'CombinedCascadeSeed_L3',
                 Pulses=args.pulse_type)
    else:
        Seed = []
        if args.hypo == 'track':
            _converter = convert_to_track_seed
        else:
            _converter = convert_to_cascade_seed
        for aseed in args.seed:
            aseed_conv = f'{aseed}_converted'
            tray.Add(_converter, inkey=aseed, outkey=aseed_conv, If=lambda frame: frame.Has(aseed))
            Seed.append(aseed_conv)

    tray.Add(maskdc, origpulses=args.pulse_type, maskedpulses=f'{args.pulse_type}IC',
             If=lambda frame: not frame.Has(f'{args.pulse_type}IC'))
    pulses_for_reco = args.pulse_type if args.idc else f'{args.pulse_type}IC'
    tray.Add(pulse_cleaning,
             Pulses=pulses_for_reco, Residual=args.residual,
             If=lambda frame: not frame.Has(pulses_for_reco+'PulseCleaned'))
    excludedDOMs = tray.Add(HighEnergyExclusions,
                            Pulses=pulses_for_reco,
                            BrightDOMThreshold=args.bdthres,
                            ExcludeDeepCore=False if args.idc else 'DeepCoreDOMs',
                            BadDomsList='BadDomsList',
                            CalibrationErrata='CalibrationErrata',
                            SaturationWindows='SaturationWindows')
    # this isn't placed in by default as SaturatedDOMs are excluded fully
    # here we decide later in the MonopodWrapper
    excludedDOMs.append('SaturationWindows')

    # update millipede_params
    excludedDOMs.append(pulses_for_reco+'PulseCleanedTimeWindows')

    millipede_params = {'Pulses': f'{pulses_for_reco}PulseCleaned',
                        'CascadePhotonicsService': cascade_service,
                        'MuonPhotonicsService': None,
                        'ExcludedDOMs': excludedDOMs,
                        'ReadoutWindow': f'{pulses_for_reco}PulseCleanedTimeRange',
                        'PartialExclusion': True,
                        'UseUnhitDOMs': not args.nouh,
                        'MinTimeWidth': args.mintimewidth,
                        'RelUncertainty': args.relerr}
    logging.info(pformat(millipede_params))

    if not np.isnan(args.binsigma):
        biname = f'BS{args.binsigma}'
    else:
        biname = 'PPB0'

    seed_fit = f'{specifier}_iMIGRAD_{biname}'
    seed_key = f'{seed_fit}_Seed'
    require_millipede_params(millipede_params)
    log_run_summary(args, seed_fit, seed_key, millipede_params)
    if args.dry_run_config:
        return

    minis = []
    minis.append('iMIGRAD')
    for mini in minis:
        tray.Add(wrapperfn,
                 f'{specifier}_{mini}_{biname}',
                 Seed=Seed,
                 BrightsFit=args.ibr,
                 SaturatedFit=args.isat,
                 BadTimeWindowsFit=args.itw,
                 Minimizer=mini,
                 Unfold=args.unfold,
                 BinSigma=args.binsigma,
                 AmplitudeFit=args.seed is None,
                 **millipede_params)
    
    for mini in minis:
        # Plot the likelihood space around the minimum.
        seeder = lilliput.segments.add_seed_service(
            tray,
            millipede_params['Pulses'],
            [f'{specifier}_{mini}_{biname}'])
        minispec = mini.lower()
        if args.ibr:
            minispec += '.ibr'
        if args.idc:
            minispec += '.idc'
        if args.isat:
            minispec += '.isat'
        if args.relerr:
            minispec += f'.relerr{args.relerr:.2f}'
    

    #tray.AddModule('Delete', 'Delete_seed', Keys=[seed_key])
    #from reco.seed import convert_to_tau_seed
    #tray.Add(convert_to_tau_seed, inkey=seed_fit, outkey=seed_key)
    #from taupede_tianlu import convert_to_tau_seed_withlength
    #tray.Add(convert_to_tau_seed_withlength, inkey=seed_fit, outkey=seed_key)
    

    #tabledir = '/data/sim/sim-new/spline-tables/'
    #splinetabledir = '/cvmfs/icecube.opensciencegrid.org/data/photon-tables/splines'
    #tables = I3PhotoSplineService(amplitudetable = splinetabledir + '/cascade_single_spice_3.2.1_flat_z20_a10.abs.fits',
    #                                          timingtable = splinetabledir + '/cascade_single_spice_3.2.1_flat_z20_a10.prob.fits',
    #                                          effectivedistancetable = splinetabledir + '/cascade_effectivedistance_spice_3.2.1_z20.eff.fits',
    #                                          tiltTableDir = '/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/metaprojects/combo/V01-01-01/ice-models/resources/models/spice_3.2.1/',
    #                                          timingSigma=0.)
    #print("using spice321 tilt effective distance icemodel")
    #gcd = "/cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz"
    #tray.AddSegment(Taupede_spice3,'Taupede_newmonoseed',seed=seed_key, Pulses=args.pulse_type ,my_photonics_service=tables)
    #newsettingkey = makedeletekey('Taupede_newmonoseed')
    #tray.AddSegment(deletekey,newsettingkey)
    #tray.AddSegment(Add_calculated_variables,'Taupede_newmonoseed')
    
    tray.AddSegment(Taupede_ftp,'Taupede_ftp',seed=seed_key,millipede_params = millipede_params)
    tray.AddSegment(Add_calculated_variables,'Taupede_ftp')
    newsettingkey = makedeletekey('Taupede_ftp')
    tray.AddSegment(deletekey,newsettingkey)
    #tray.AddSegment(Add_calculated_variables,'TaupedeFit_iMIGRAD_testing')

    millipede_params['PhotonsPerBin'] = 0

    FTP_REVAL_KEY = 'Taupede_ftp_reval'
    tray.Add(print_ftp_output,
             If=lambda f: f.Stop == icetray.I3Frame.Physics)
    tray.Add('PyMillipede', FTP_REVAL_KEY,
             Hypothesis=lambda f: list(f['Taupede_ftpParticles']) if f.Has('Taupede_ftpParticles') else [],
             Output=FTP_REVAL_KEY,
             BinSigma=args.binsigma,
             If=lambda f: f.Stop == icetray.I3Frame.Physics and f.Has('Taupede_ftpParticles'),
             **millipede_params)
    tray.Add(print_logl_comparison,
             eval_key=FTP_REVAL_KEY,
             stored_key='Taupede_ftpFitParams',
             label='reval ftp',
             If=lambda f: f.Stop == icetray.I3Frame.Physics)
    if ext_particles_map:
        def print_ext_particles(frame, particles_map=ext_particles_map, key_label=args.eval_particles_key):
            if not frame.Has('I3EventHeader'):
                return
            hdr = frame['I3EventHeader']
            particles = particles_map.get((hdr.run_id, hdr.event_id))
            if particles is None:
                return
            print(f'  {key_label} ({len(particles)} particles):')
            for i, p in enumerate(particles):
                print(f'    [{i}]  pos=({p.pos.x:.2f}, {p.pos.y:.2f}, {p.pos.z:.2f}) m'
                      f'  zen={math.degrees(p.dir.zenith):.3f} deg'
                      f'  az={math.degrees(p.dir.azimuth):.3f} deg'
                      f'  E={p.energy:.2f} GeV'
                      f'  t={p.time:.2f} ns'
                      f'  L={p.length:.2f} m')

        tray.Add(print_ext_particles,
                 If=lambda f: f.Stop == icetray.I3Frame.Physics)

        EXT_REVAL_KEY = 'Taupede_ext_reval'
        tray.Add('PyMillipede', EXT_REVAL_KEY,
                 Hypothesis=lambda f, m=ext_particles_map: m.get(
                     (f['I3EventHeader'].run_id, f['I3EventHeader'].event_id), []
                 ) if f.Has('I3EventHeader') else [],
                 Output=EXT_REVAL_KEY,
                 BinSigma=args.binsigma,
                 If=lambda f: f.Stop == icetray.I3Frame.Physics and f.Has('I3EventHeader') and
                              (f['I3EventHeader'].run_id, f['I3EventHeader'].event_id) in ext_particles_map,
                 **millipede_params)
        tray.Add(print_logl_comparison,
                 eval_key=EXT_REVAL_KEY,
                 stored_key='Taupede_ftpFitParams',
                 label=args.eval_particles_key,
                 If=lambda f: f.Stop == icetray.I3Frame.Physics)


    #tray.AddSegment(Taupede_adjustlength,'Taupede_lengthbound_200',seed=seed_key,lengthbound = 200,millipede_params = millipede_params)
    #tray.AddSegment(Add_calculated_variables,'Taupede_lengthbound_200')
    #newsettingkey = makedeletekey('Taupede_lengthbound_200')
    #tray.AddSegment(deletekey,newsettingkey)
    
    #tray.AddSegment(Taupede_adjustlength,'Taupede_lengthbound_500',seed=seed_key,lengthbound = 500,millipede_params = millipede_params)
    #tray.AddSegment(Add_calculated_variables,'Taupede_lengthbound_500')
    #newsettingkey = makedeletekey('Taupede_lengthbound_500')
    #tray.AddSegment(deletekey,newsettingkey)

    
    step_dict = {
        'StepL':20,
        'StepT':5,
        'StepD':2,
        'StepZenith':10,
        'StepAzimuth':10,
    }

    #millipede_params_withsteps = {**millipede_params, **step_dict}

    #tray.AddSegment(Taupede_adjustlength,'Taupede_tianlu_step',seed=seed_key,millipede_params = millipede_params_withsteps)
    #tray.AddSegment(Add_calculated_variables,'Taupede_tianlu_step')
    #newsettingkey = makedeletekey('Taupede_tianlu_step')
    #tray.AddSegment(deletekey,newsettingkey)

    
    #tray.AddSegment(Taupede_adjustlength,'Taupede_lengthbound_200_tianlu_step',seed=seed_key,lengthbound = 200, millipede_params = millipede_params_withsteps)
    #tray.AddSegment(Add_calculated_variables,'Taupede_lengthbound_200_tianlu_step')
    #newsettingkey = makedeletekey('Taupede_lengthbound_200_tianlu_step')
    #tray.AddSegment(deletekey,newsettingkey)
    
    
    #tray.Add("I3OrphanQDropper")
    tray.AddModule('I3Writer',
                   'writer',
                   filename=args.out,
                   streams=[icetray.I3Frame.TrayInfo,
                            icetray.I3Frame.Physics,
                            icetray.I3Frame.Simulation,
                            icetray.I3Frame.Stream('M'),
                            icetray.I3Frame.DAQ])
    if args.nframes is None:
        tray.Execute()
    else:
        tray.Execute(args.nframes)
    tray.PrintUsage()


if __name__ == '__main__':
    logging.basicConfig(encoding='utf-8', level=logging.INFO)
    main()
