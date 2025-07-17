#!/usr/bin/env python
import os,sys
import argparse
import numpy as np
from snowflake import library
from reco import truth
from icecube import clsim, MuonGun, dataclasses, millipede
from icecube.dataclasses import I3Double, I3Particle, I3Direction
from icecube.icetray import I3Bool
import glob

# import nehas functions
sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")

### Neha's trays, do I actually need them?
from segments.AddOutgoingParticles import mctreeinfo
from segments.MCinfo_NL import mcinfo
from segments.MCInfoWrapper import MCInfoWrapper
from segments.TrueObservables import calculatetrueobservables # requires work to reproduce

from segments.PassingFraction import penetrating_depth, PassingFraction, add_primary
from segments.Glashow import glashow_correction
from segments.TauPol import tau_polarization

MED = clsim.MakeIceCubeMediumProperties(
    iceDataDirectory=os.path.expandvars('$I3_BUILD/ice-models/resources/models/ICEMODEL/spice_ftp-v3/'),
    )


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
    classification = frame['FinalTopology'].value
    if classification != 2:
        frame['FinalEventClass']= dataclasses.I3Double(classification)
    else:
        if frame['RecoL']<=20 and frame['RecoETot']>=3000000:
            frame['FinalEventClass']=dataclasses.I3Double(1)
        else:
            frame['FinalEventClass']= dataclasses.I3Double(classification)

def fn(frame):
    fensurecc(frame)
    fenergy(frame)
    ftaudec(frame)
    fice(frame)
    flen(frame)
    
    # neha's functions HESE_Taupede.py, do I actually need them?
    # mctreeinfo(frame)
    # MCInfoWrapper(frame, name="Add MC info")
    # mcinfo(frame)
    # calculatetrueobservables(frame) # not working now, do I actually want it?

    add_primary(frame)
    penetrating_depth(frame) # problem in this icectray with MuonGun
    PassingFraction(frame)
    # reclassify_double(frame)
    glashow_correction(frame)
    tau_polarization(frame)

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
    parser.add_argument('--simwrite', default=False,
                        action='store_true',
                        help='book objects in DAQ frames')
    args = parser.parse_args()

    if args.simwrite:
        library.simhdfwriter(args.i3s, args.out,
                             keys=['I3MCWeightDict',
                                   'I3EventHeader']+args.add)
        return

    inputfiles = glob.glob( f"{args.inpath}/*.i3.*" )

    print("Writing output to", args.out)
    print(f"found {len(inputfiles)}")

    inputfiles = remove_corrupt_files(inputfiles)

    library.hdfwriter(inputfiles, args.out,
                      subeventstreams=args.splits,
                      fn=fn,
                      keys=['cc',
                            'cc_2surf',
                            'cc_zshift',
                            'cc_b400_notilt',
                            'cc_b400_tilted',
                            'cc_aDust400_notilt',
                            'cc_aDust400_tilted',
                            'cc_easymm',
                            'cc_tauvis',
                            'CombinedCascadeSeed_L3',
                            'I3MCWeightDict',
                            'I3EventHeader',
                            'PreferredFit',
                            'MonopodFit_iMIGRAD',
                            'MonopodFit_iMIGRADFitParams',
                            'TaupedeFit_iMIGRAD',
                            'TaupedeFit_iMIGRADParticles',
                            'TaupedeFit_iMIGRADFitParams',
                            'MillipedeFit_iMIGRAD',
                            'MillipedeFit_iMIGRADParticles',
                            'MillipedeFit_iMIGRADFitParams',
                            'seed_iMIGRAD_BestMonopod',
                            'seed_iMIGRAD_BestAltnFit',
                            'LineFit',
                            'SPEFit2',
                            'l2_online_SplineMPE',
                            'OnlineL2_SplineMPE',
                            'EventGeneratorFit_I3Particle',
                            'EventGeneratorSelectedReco_I3Particle',
                            'EventGeneratorSelectedRecoNN_I3Particle',
                            'EventGeneratorSelectedRecoNNCircularUncertainty',

                            # thijs
                            'TaupedeFit_iMIGRAD_PPB0',
                            'TaupedeFit_iMIGRAD_PPB0FitParams',
                            'TaupedeFit_iMIGRAD_PPB0Particles',
                            'MonopodFit_iMIGRAD_PPB0',
                            'MonopodFit_iMIGRAD_PPB0FitParams',
                            'CscdL3_SPEFit16',
                            'CscdL3_SPEFit16FitParams',

                            'TaupedeFit_iMIGRAD_PPB0_bright',
                            'TaupedeFit_iMIGRAD_PPB0_brightFitParams',
                            'TaupedeFit_iMIGRAD_PPB0_brightParticles',
                            

                            # neha
                            'HESETaupedeFit',
                            'HESETaupedeFitFitParams',
                            'HESETaupedeFitParticles',

                            'HESEMonopodFit',
                            'HESEMonopodFitFitParams',
                            'HESEMonopodFitParticles',

                            'SPEFit16',
                            'SPEFit16FitParams',

                            'HESEMillipedeFit'
                            'HESEMillipedeFitParticles'

                            'HESEEventclass',
                            'FinalTopology',
                            'FinalEventClass',
                            'MCInteractionEventclass',

                            'ConventionalAtmosphericPassingFractions',
                            'PromptAtmosphericPassingFractions',

                            'RecoL',
                            'RecoEConfinement',
                            'RecoERatio',
                            'RecoETot',
                            "RecoAzimuth",
                            "RecoZenith",

                            "TrueAzimuth",
                            "TrueETot",
                            "TrueL",
                            "TrueZenith",

                            # event generator
                            'EventGeneratorDC_Max',
                            'EventGeneratorDC_Thijs',
                            
                            # bdt
                            'TauMonoDiff_rlogl',
                            'Taupede_Asymmetry',
                            'Taupede_Distance',
                            'Taupede1_Particles_energy',
                            'Taupede2_Particles_energy',
                            'cscdSBU_MonopodFit4_noDC_zenith',
                            'MonopodFit_iMIGRAD_PPB0_Delay_ice',
                            'CVStatistics_q_max_doms',
                            'cscdSBU_VertexRecoDist_CscdLLh',
                            'cscdSBU_Qtot_HLC_log',
                            'Taupede_ftpFitParams_rlogl',
                            'cscdSBU_MonopodFit4_noDCFitParams_rlogl',

                            # HESE
                            'HESE_VHESelfVeto',
                            'HESE_CausalQTot',
                            'HESE_HomogenizedQTot',
                            'VHESelfVeto',
                            'CausalQTot',
                            'HomogenizedQTot',
                            'QFilterMask',
                            'QFilterMask_HESEFilter_15_condition_passed',

                            # more Neha stuff
                            'Filenum',
                            'HESEMillipedeFitTruncatedDepositedEnergy',
                            'HESEMillipedeFitDepositedEnergy',
                            'RecoLogL',
                            'RecoLogE1',
                            'RecoLogE2',
                            'RecoLogETot',
                            'TaupedeFitManualFitStatus',
                            'HESEMillipedeFitFitParams',
                            'MCInteractionDepth',
                            'issingle',
                            'isdouble',
                            'istrack',
                            'RecoE1',
                            'RecoE2',
                            'RecoLbyE',
                            'TaupedeFitParticles',
                            'TaupedeFit',
                            'TaupedeFitFitParams',
                            'SnowstormParameterDict',
                            'RecoParticle',
                            'RecoEnergy',
                            'RecoDirection',
                            'RecoLength',
                            'TrueLength',
                            'MCReconstructionEventclass',
                            'RecoLbyE',
                            'TotalWeight',
                            'TotalWeightPol',
                            'VertexOutgoingHadronNew',
                            'VertexOutgoingLeptonNew',
                            'y_lep',
                            'y_had',

                            'DNNC_I3Particle']+args.add)

    
if __name__ == '__main__':
    main()
