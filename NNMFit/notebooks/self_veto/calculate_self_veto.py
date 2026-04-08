#!/usr/bin/env python3
from icecube import dataio, icetray, dataclasses, simclasses
from icecube.icetray import I3Tray
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import glob
import sys, os, datetime
import pickle

sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")
from segments.VHESelfVeto import SelfVetoWrapper
from segments.PassingFraction import penetrating_depth, PassingFraction, add_primary

### neha
import sys
sys.path.append("/data/user/nlad/PassingFractions/")
from spline_evaluator import Spline_Evaluator

parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("--Inputfile",type=str,help='Input file',dest="inputfile")
parser.add_argument("--Outputfile",type=str,help='Output file',dest="outputfile")
opts = parser.parse_args()

gcdfilepath = "/cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz"

files = [gcdfilepath, opts.inputfile]

tray = I3Tray()
tray.Add("I3Reader", FileNameList=files)

################################################################
############## HESE Event selection ###########
################################################################

# tray.Add(SelfVetoWrapper)
# tray.Add(lambda frame : 'HESE_VHESelfVeto' in frame and not frame['HESE_VHESelfVeto'].value)
# tray.Add(lambda frame : 'HESE_CausalQTot' in frame and frame['HESE_CausalQTot'].value >= 6000)

tray.Add(lambda frame : frame["I3MCWeightDict"]["PrimaryNeutrinoEnergy"] >= 1e7)


tray.Add(add_primary)
tray.Add(penetrating_depth)

# for crosscheck, add calculation with gcd as done in SnowStorm v1
gcdfile_v1 = "/cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_AVG_55697-57531_PASS2_SPE_withScaledNoise.i3.gz"
tray.AddModule(penetrating_depth, gcd=gcdfile_v1, depth_name_suffix='_v1_gcd')

tray.Add(PassingFraction)

### print
def print_passing(frame):
    print(10*"-", "completed event")
    print("PrimaryNeutrinoType",frame["I3MCWeightDict"]["PrimaryNeutrinoType"])
    print("PrimaryNeutrinoEnergy",frame["I3MCWeightDict"]["PrimaryNeutrinoEnergy"])
    print("PrimaryNeutrinoZenith",frame["I3MCWeightDict"]["PrimaryNeutrinoZenith"])
    print("penetrating_depth",frame["penetrating_depth"])
    print("penetrating_depth_old",frame["penetrating_depth_old"])
    print("ConventionalAtmosphericPassingFractions",frame["ConventionalAtmosphericPassingFractions"])
    print("PromptAtmosphericPassingFractions",frame["PromptAtmosphericPassingFractions"])

tray.Add(print_passing)

################################################################
########################### Wrap it up #########################
################################################################

tray.AddModule('I3Writer',
                'writer',
                filename=opts.outputfile,
                DropOrphanStreams=[icetray.I3Frame.DAQ, icetray.I3Frame.Stream('M'), icetray.I3Frame.TrayInfo],
                streams=[icetray.I3Frame.TrayInfo,
                        icetray.I3Frame.Physics,
                        icetray.I3Frame.Simulation,
                        icetray.I3Frame.Stream('M'),
                        icetray.I3Frame.Stream('X'),
                        icetray.I3Frame.DAQ])

tray.Execute()
tray.Finish()


import numpy as np

spline_hdl = Spline_Evaluator()

pid = np.asarray(12)
Depth = np.asarray(2227.94)
zenith = np.asarray(0.5898462186684095)
energy = np.asarray(18999134.486152586)
x= spline_hdl.evaluate_all(pid,Depth,zenith,energy)