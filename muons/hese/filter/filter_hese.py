#!/usr/bin/env python3
from icecube import dataio, icetray, dataclasses, simclasses
from icecube.icetray import I3Tray
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import glob
import sys, os, datetime
import pickle

sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")
from segments.VHESelfVeto import SelfVetoWrapper

parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("--Inputpath",type=str,help='Input file',dest="inputpath")
parser.add_argument("--Outputfile",type=str,help='Output file',dest="outputfile")
opts = parser.parse_args()

gcdfilepath = "/cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz"

inputfiles = glob.glob( f"{opts.inputpath}/*" )

print(f"found {len(inputfiles)} files")

files = [gcdfilepath] + inputfiles

tray = I3Tray()
tray.Add("I3Reader", FileNameList=files)

################################################################
############## HESE Event selection ###########
################################################################

def print_veto(frame):
    if "VHESelfVeto" not in frame: return
    print("VHESelfVeto", frame['VHESelfVeto'])
    print("CausalQTot", frame['CausalQTot'])

tray.Add(SelfVetoWrapper)
# tray.Add(print_veto)
tray.Add(lambda frame : 'VHESelfVeto' in frame and not frame['VHESelfVeto'].value)
tray.Add(lambda frame : 'CausalQTot' in frame and frame['CausalQTot'].value >= 6000)

################################################################
########################### Wrap it up #########################
################################################################

tray.AddModule('I3Writer',
                'writer',
                filename=opts.outputfile,
                DropOrphanStreams=[icetray.I3Frame.DAQ, 
                                   icetray.I3Frame.Stream('M'), 
                                   icetray.I3Frame.Stream('S'), 
                                   icetray.I3Frame.TrayInfo],
                streams=[icetray.I3Frame.TrayInfo,
                        icetray.I3Frame.Physics,
                        icetray.I3Frame.Simulation,
                        icetray.I3Frame.Stream('M'),
                        icetray.I3Frame.Stream('X'),
                        icetray.I3Frame.DAQ])

tray.Execute()
tray.Finish()
