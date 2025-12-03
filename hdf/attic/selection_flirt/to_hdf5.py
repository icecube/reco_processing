#!/usr/bin/env python
import os,sys
import argparse
import numpy as np
from snowflake import library
from reco import truth
from icecube import clsim, MuonGun, dataclasses, millipede
from icecube.dataclasses import I3Double, I3Particle, I3Direction
from icecube.icetray import I3Bool
from I3Tray import I3Tray
from icecube.hdfwriter import I3HDFWriter
from icecube import dataio
from icecube import icetray, phys_services
import glob
from datetime import datetime, timedelta


# import nehas functions
sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")

### Neha's trays, do I actually need them?
import segments
from segments.AddOutgoingParticles import AddOutGoingParticles # previously mctreeinfo
from segments.AddMCInfo import AddMCInfo # Previously MCInfoWrapper.py with MCInfoWrapper

from segments.MCinfo_NL import mcinfo
from segments.TrueObservables import calculatetrueobservables # requires work to reproduce

from segments.PassingFraction import penetrating_depth, PassingFraction, add_primary
from segments.Glashow import glashow_correction
from segments.TauPol import tau_polarization
from segments.VHESelfVeto import SelfVetoWrapper
from segments.FinalEventClassification import checkfinaltopology
from segments.RecoObservables import calculaterecoobservables

from segments.MuonGunWeighter import Get_MuonWeight
from segments.PropagateMuons import PropagateMuons

# bdt
from segments.cscdSBU_misc import misc
from segments.mlb_DelayTime_noNoise import calc_dt_nearly_ice 
from segments.bdt_var import taupede_monopod_bdt_var

# cv statistics
from icecube.filterscripts.offlineL2.Globals import muon_wg, wimp_wg
from icecube.filterscripts.offlineL2.level2_Reconstruction_Muon import add_hit_verification_info_muon_and_wimp
from icecube.phys_services.which_split import which_split

MED = clsim.MakeIceCubeMediumProperties(
    iceDataDirectory=os.path.expandvars('$I3_BUILD/ice-models/resources/models/ICEMODEL/spice_ftp-v3/'),
    )


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

def print_frameid(frame):
    eventid = frame['I3EventHeader'].event_id
    runid = frame['I3EventHeader'].run_id
    print(f"*******Currently processing frame {eventid} run {runid} *******")


def fensurecc(frame):
    if not frame.Has('cc'):
        truth.truth(frame, "tau")


def fenergy(frame):
    if frame.Has('I3MCTree'):
        frame['cc'].energy = library.get_deposit_energy(frame['I3MCTree'])
        epre = library.get_deposit_energy(
            frame['I3MCTree'],
            frame['cc'].time + 0.99 * frame['cc'].length / dataclasses.I3Constants.c)
        etot = frame['cc'].energy
        frame['cc_easymm'] = I3Double((2 * epre - etot) / etot)
    else:
        try:
            frame['cc'].energy = frame['PreferredFit'].energy
        except KeyError:
            pass
        frame['cc_easymm'] = I3Double(1.)

    try:
        frame['SplineMPEICSeed'].energy = frame['SplineMPEICMuEXDifferential'].energy
        frame['SplineMPEIC'].energy = frame['SplineMPEICMuEXDifferential'].energy
    except KeyError:
        pass
    try:
        erec = 0
        for p in frame['MillipedeStarting3rdPassParticles']:
            erec += p.energy
        frame['MillipedeStarting3rdPass'].energy = erec
        frame['MillipedeStarting2ndPass'].energy = frame['cc'].energy
    except KeyError:
        pass


def ftaudec(frame):
    if not frame.Has('I3MCTree'):
        frame['cc_tauvis'] = I3Particle()
        return

    if not truth.is_tau(frame['cc']):
        frame['cc_tauvis'] = I3Particle()
        return

    daughters = frame['I3MCTree'].get_daughters(frame['cc'])
    if frame['cc'].type == I3Particle.TauMinus:
        okd = [I3Particle.MuMinus,
               I3Particle.EMinus,
               I3Particle.PiMinus,
               I3Particle.Hadrons]
    else:
        okd = [I3Particle.MuPlus,
               I3Particle.EPlus,
               I3Particle.PiPlus,
               I3Particle.Hadrons]
    frame['cc_tauvis'] = I3Particle(truth.get_first(daughters, okd))


def fice(frame):
    pos = frame['cc'].pos
    if np.any(np.isnan([pos.x, pos.y, pos.z])):
        return

    zshifter = MED.GetIceTiltZShift()
    zshift = zshifter.GetValue(pos.x, pos.y, pos.z)

    get_layer = lambda z: int((z-MED.GetLayersZStart())/MED.GetLayersHeight())
    min_layer = 0
    max_layer = MED.GetLayersNum()-1
    layer_notilt = max(min(get_layer(pos.z), min_layer), max_layer)
    layer_tilted = max(min(get_layer(pos.z-zshift), min_layer), max_layer)

    frame['cc_zshift'] = I3Double(-zshift)
    frame['cc_b400_notilt'] = I3Double(MED.GetScatteringLength(layer_notilt).b400)
    frame['cc_b400_tilted'] = I3Double(MED.GetScatteringLength(layer_tilted).b400)

    frame['cc_aDust400_notilt'] = I3Double(MED.GetAbsorptionLength(layer_notilt).aDust400)
    frame['cc_aDust400_tilted'] = I3Double(MED.GetAbsorptionLength(layer_tilted).aDust400)


def flen(frame):
    """ calculate length inside detector from true position
    """
    cc = frame['cc']
    pos = cc.pos
    if np.any(np.isnan([pos.x, pos.y, pos.z])):
        # data event doesn't have set cc
        return

    # A surface approximating the actual detector (make it smaller if you only care e.g. about DeepCore)
    surface = MuonGun.Cylinder(1000,500)
    intersections = surface.intersection(cc.pos, cc.dir)
    frame['cc_2surf'] = I3Double(intersections.second-max(0, intersections.first))


def fdnn(frame):
    pmap = frame['DNNCascadeAnalysis_version_001_p01']
    ppar = I3Particle()
    ppar.dir = I3Direction(pmap['zen'], pmap['azi'])
    ppar.energy = pmap['energy']
    ppar.time = pmap['time']
    ppar.fit_status = I3Particle.FitStatus.OK
    ppar.shape = I3Particle.ParticleShape.Cascade
    frame['DNNC_I3Particle'] = ppar


def reclassify_double(frame):
    """
    Neha's removal of high-energy single cascades in double cascade sample
    Doesn't seem necessary anymore
    """
    if 'FinalTopology' not in frame: return # for old reco
    classification = frame['FinalTopology'].value
    if classification != 2:
        frame['FinalEventClass']= dataclasses.I3Double(classification)
    else:
        if frame['RecoL']<=20 and frame['RecoETot']>=3000000:
            frame['FinalEventClass']=dataclasses.I3Double(1)
        else:
            frame['FinalEventClass']= dataclasses.I3Double(classification)

def fn(frame):    
    # tianlu scripts
    fensurecc(frame)
    fenergy(frame)
    ftaudec(frame)
    fice(frame)
    flen(frame)

    if frame.Has('DNNCascadeAnalysis_version_001_p01'):
        fdnn(frame)


corrupt_files = [
    "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator/22043/0000000-0000999/Level3_NuMu_NuGenCCNC.022043.000196.i3.zst",

    # my own processing
    "/data/sim/IceCube/2023/filtered/level7/cascade/neutrino-generator/cascade/22634/0001000-0001999/Level7_NuTau_NuGenCCNC.022634.001137_cascade.i3.zst",

    # lets see what is wrong here


]

#Using the scaling factor used in HESE 7.5 
#that was derived using data-driven method
#eseentially for conventional weights
#we do MuonWeightConv*2.1
def MuonWeight_Scaling(frame):
    if frame.Has('MuonWeightConv'):
         MuonWeightConv = frame['MuonWeightConv'].value
         frame['MuonWeightScaled'] = dataclasses.I3Double(MuonWeightConv*2.1)
    return True    

def remove_corrupt_files(input_files):
    """Remove known corrupt files from the input list."""
    clean_files = [f for f in input_files if f not in corrupt_files]
    return clean_files

def remove_checksum_files(input_files):
    """Remove known corrupt files from the input list."""
    clean_files = []

    for input_file in input_files:
        try:
            i3file = dataio.I3File(input_file)
            while i3file.more(): frame = i3file.pop_frame()
            clean_files.append(input_file)
            i3file.close()
        except:
            continue
    return clean_files

def main():
    parser = argparse.ArgumentParser(
        description='Extract CausalQTot and MJD data from i3 to h5')

    parser.add_argument('-a', '--add', nargs='+', default=[],
                        type=str, help='additional keys to save')
    parser.add_argument('-o', '--out', default='a.h5',
                        type=str, help='output file')
    parser.add_argument('-i', '--inpath', default='/test',
                        type=str, help='input path')
    parser.add_argument('-f', '--flavor', default='NuTau',
                        type=str, help='flavor')
    parser.add_argument('-sf', '--selection', default=None,
                        type=str, help='selection function')
    parser.add_argument('-c', '--channel', default=None,
                        type=int, help='cascade 1, double 2, track 3')
    parser.add_argument('-S', '--splits', default=['InIceSplit',"Final"], nargs='+',
                        help='which P-frame splits to process')
    parser.add_argument('--spice', default=False, action='store_true',
                        help='creating hdf from spice files')
    parser.add_argument('--nframes', type=int, default=None, help='number of frames to process')
    args = parser.parse_args()

    if args.spice:
        monopod_key = "HESEMonopodFit"
        taupede_key = "HESETaupedeFit"
        millipede_key = "HESEMillipedeFit"
        pulses      = "SplitInIcePulses"
    else:
        monopod_key = "MonopodFit_iMIGRAD_PPB0"
        taupede_key = "TaupedeFit_iMIGRAD_PPB0"
        millipede_key = "HESEMillipedeFit_PPB0"
        pulses      = "SplitInIcePulses"

    inputfiles = glob.glob( f"{args.inpath}/*.i3.*" )
    inputfiles = remove_corrupt_files(inputfiles)
    inputfiles = remove_checksum_files(inputfiles)

    # cutoff_time = datetime.now() - timedelta(hours=1)

    # # Keep only files older than 1 hour
    # inputfiles = [
    #     f for f in inputfiles
    #     if datetime.fromtimestamp(os.path.getmtime(f)) < cutoff_time
    # ]

    print("Writing output to", args.out)
    print(f"found {len(inputfiles)}")
    print("using args.spice", args.spice)

    gcd = ["/data/user/tvaneede/GlobalFit/reco_processing/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz"]

    inputfiles = gcd + inputfiles

    tray = I3Tray()
    tray.Add("I3Reader", FileNameList=inputfiles)
    tray.Add(print_frameid)

    flavor = args.flavor
    print("flavor", flavor)
    
    tray.Add(fn)

    tray.AddModule(calculaterecoobservables,
                    'calc_reco_observables',
                    innerboundary=550,
                    outeredge_x=outeredge_x,
                    outeredge_y=outeredge_y,
                    monopod_key=monopod_key,
                    taupede_key=taupede_key,
                    millipede_key=millipede_key)

    tray.Add(checkfinaltopology,eventclass=f"{taupede_key}HESEEventclass")
    tray.Add(reclassify_double)

    ###
    ### add cascade bdt variables
    ###
    tray.AddSegment(misc, 'misc', pulses=pulses) # was with OfflinePulses, but should be same as SplitInIcePulses

    # taken from /data/user/tvaneede/GlobalFit/selection/bdt/tau/cascade-final-filter/cscdSBU_vars.py
    # and mlb_DelayTime_noNoise.py
    tray.AddModule(calc_dt_nearly_ice,'delaytime_monopod_noDC',name="MonopodFit_iMIGRAD_PPB0",
                    reconame=monopod_key,pulsemapname=f'{pulses}HLC_noSaturDOMs')

    # add cv statistics if we dont have it yet
    tray.AddSegment(add_hit_verification_info_muon_and_wimp, 'CommonVariablesMuonAndWimp',
                    Pulses= pulses,
                    If = which_split(split_name='InIceSplit') & (lambda f: (muon_wg(f) or wimp_wg(f)) and 'CVStatistics' not in f),
                    OutputI3HitMultiplicityValuesName= "CVMultiplicity",
                    OutputI3HitStatisticsValuesName= "CVStatistics",
                    suffix = '')

    tray.AddModule(taupede_monopod_bdt_var,"taupede_monopod_bdt_var",
                   monopod_key=monopod_key, taupede_key=taupede_key)

    if flavor != "MuonGun": # nugen
        tray.Add(add_primary)
        tray.Add(penetrating_depth)

        # for crosscheck, add calculation with gcd as done in SnowStorm v1
        gcdfile_v1 = "/cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_AVG_55697-57531_PASS2_SPE_withScaledNoise.i3.gz"
        tray.AddModule(penetrating_depth, gcd=gcdfile_v1, depth_name_suffix='_v1_gcd')

        tray.Add(PassingFraction)

        tray.Add(glashow_correction)
        tray.Add(tau_polarization)

        tray.AddModule(AddOutGoingParticles,'AddOutGoingParticles')
        tray.Add(AddMCInfo,'AddMCInfo')

    else: # muongun
        ## actually propagate the muons (is that necessary?)
        tray.Add("Rename", "rename", 
                 Keys = ['MMCTrackList', 'MMCTrackList_orig'],
                 If=lambda frame: not frame.Has('I3MCTree') )
        randomService = phys_services.I3SPRNGRandomService(seed = 10000,
                nstreams = 200000000,
                streamnum = 100014318)
        tray.context['I3RandomService'] = randomService
        tray.Add(PropagateMuons, 'PropagateMuons',
                    RandomService=randomService,
                    # RNGStateName=I3MCTree_preMuonProp_RNGState,
                    SaveState=True,
                    InputMCTreeName="I3MCTree_preMuonProp",
                    OutputMCTreeName="I3MCTree",
                    If=lambda frame: not frame.Has('I3MCTree'))

        tray.Add(Get_MuonWeight,'MuonGun_weight',infile=inputfiles,\
                flux_model='GaisserH4a_atmod12_SIBYLL',prefix='Conv')
        tray.Add(Get_MuonWeight,'MuonGun_weight',infile=inputfiles,\
                flux_model='GaisserH4a_atmod12_DPMJET-C',prefix='Prompt')
        tray.AddModule(MuonWeight_Scaling)

    tray.Add(mcinfo, 'mcpreproc_',
                    outeredge_x=outeredge_x, outeredge_y=outeredge_y,
                    innerboundary=550.0, outerboundary=650.0,
                    dataset=flavor,
                    ethreshold=1e3,
                    PhotonsPerBin=5,
                    ShowerSpacing=5)
    tray.Add(calculatetrueobservables,
        'calc_true_observables',
        innerboundary=550.0,
        outeredge_x=outeredge_x, 
        outeredge_y=outeredge_y)

    if args.selection:
        print("using a selection", args.selection, args.channel)
        import importlib
        module = importlib.import_module("selections")
        func = getattr(module, args.selection) 
        tray.Add(lambda frame : func(frame, args.channel))

    from hdf_keys import hdfkeys
    hdfkeys+=args.add

    tray.Add(I3HDFWriter, Output=args.out, Keys=hdfkeys, SubEventStreams=args.splits)
    if args.nframes is None:
        print("processing all frames")
        tray.Execute()
    else:
        print("processing nframes", args.nframes)
        tray.Execute(args.nframes)

if __name__ == '__main__':
    main()
