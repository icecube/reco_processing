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
from icecube import icetray
import glob

# import nehas functions
sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")

### Neha's trays, do I actually need them?
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
    print("*******Currently processing frame %s*******" %eventid)


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
    # tianlu
    
    fensurecc(frame)
    fenergy(frame)
    ftaudec(frame)
    fice(frame)
    flen(frame)

    if frame.Has('DNNCascadeAnalysis_version_001_p01'):
        fdnn(frame)


corrupt_files = [
    "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator/22043/0000000-0000999/Level3_NuMu_NuGenCCNC.022043.000196.i3.zst"
]

def remove_corrupt_files(input_files):
    """Remove known corrupt files from the input list."""
    clean_files = [f for f in input_files if f not in corrupt_files]
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
    parser.add_argument('-S', '--splits', default=['InIceSplit',], nargs='+',
                        help='which P-frame splits to process')
    parser.add_argument('--spice', default=False, action='store_true',
                        help='creating hdf from spice files')
    parser.add_argument('--nframes', type=int, default=None, help='number of frames to process')
    args = parser.parse_args()

    if args.spice:
        monopod_key = "HESEMonopodFit"
        taupede_key = "HESETaupedeFit"
        pulses      = "SplitInIcePulses"
    else:
        monopod_key = "MonopodFit_iMIGRAD_PPB0"
        taupede_key = "TaupedeFit_iMIGRAD_PPB0"
        pulses      = "SplitInIcePulses"

    inputfiles = glob.glob( f"{args.inpath}/*.i3.*" )

    print("Writing output to", args.out)
    print(f"found {len(inputfiles)}")
    print("using args.spice", args.spice)

    inputfiles = remove_corrupt_files(inputfiles)

    gcd = ["/data/user/tvaneede/GlobalFit/reco_processing/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz"]

    inputfiles = gcd + inputfiles

    tray = I3Tray()
    tray.Add("I3Reader", FileNameList=inputfiles)
    tray.Add(print_frameid)

    flavor = os.path.basename(inputfiles[-1]).split("_")[1] # does this work for MuonGun and data?

    # neha true HESE_Taupede.py
    tray.AddModule(AddOutGoingParticles,'AddOutGoingParticles')
    tray.Add(AddMCInfo,'AddMCInfo')
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

    tray.Add(fn)

    tray.AddModule(calculaterecoobservables,
                    'calc_reco_observables',
                    innerboundary=550,
                    outeredge_x=outeredge_x,
                    outeredge_y=outeredge_y,
                    monopod_key=monopod_key,
                    taupede_key=taupede_key)

    tray.Add(checkfinaltopology)
    tray.Add(reclassify_double)

    # passing fractions
    tray.Add(add_primary)
    tray.Add(penetrating_depth)
    tray.Add(PassingFraction)

    # add some bdt variables
    tray.AddSegment(misc, 'misc', pulses=pulses) # was with OfflinePulses, but should be same as SplitInIcePulses

    # taken from /data/user/tvaneede/GlobalFit/selection/bdt/tau/cascade-final-filter/cscdSBU_vars.py
    # and mlb_DelayTime_noNoise.py
    tray.AddModule(calc_dt_nearly_ice,'delaytime_monopod_noDC',name="MonopodFit_iMIGRAD_PPB0",
                    reconame=monopod_key,pulsemapname=f'{pulses}HLC_noSaturDOMs')

    # add cv statistics if we dont have it yet
    tray.AddSegment(add_hit_verification_info_muon_and_wimp, 'CommonVariablesMuonAndWimp',
                    Pulses= pulses,
                    If = which_split(split_name='InIceSplit') & (lambda f: (muon_wg(f) or wimp_wg(f)) and 'CVStatistics' not in f),
                    OutputI3HitMultiplicityValuesName=  "CVMultiplicity",
                    OutputI3HitStatisticsValuesName= "CVStatistics",
                    suffix = '')

    tray.AddModule(taupede_monopod_bdt_var,"taupede_monopod_bdt_var",
                   monopod_key=monopod_key, taupede_key=taupede_key)

    from hdf_keys import hdfkeys
    hdfkeys+=args.add

    tray.Add(I3HDFWriter, Output=args.out, Keys=hdfkeys, SubEventStreams=['InIceSplit'])
    if args.nframes is None:
        print("processing all frames")
        tray.Execute()
    else:
        print("processing nframes", args.nframes)
        tray.Execute(args.nframes)

if __name__ == '__main__':
    main()
