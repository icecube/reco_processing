from icecube import dataio, icetray, dataclasses, simclasses
from icecube.icetray import I3Tray
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from glob import glob
import sys, os, datetime

parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("--Inputfile",type=str,help='Input file',dest="inputfile")
parser.add_argument("--Outputfile",type=str,help='Output file',dest="outputfile")

opts = parser.parse_args()

files = [opts.inputfile]

tray = I3Tray()
tray.Add("I3Reader", FileNameList=files)

################################################################
############## Energy cut and Final Event selections ###########
################################################################

tray.Add( lambda frame: 'QFilterMask' in frame and frame['QFilterMask']['HESEFilter_15'].condition_passed )

# tray.Add(lambda frame : 'HESE_VHESelfVeto' in frame and not frame['HESE_VHESelfVeto'].value)
# tray.Add(lambda frame : 'HESE_CausalQTot' in frame and frame['HESE_CausalQTot'].value >= 6000)


################################################################
########################### Wrap it up #########################
################################################################

# deletekeys = []
# tray.Add('Delete', keys=deletekeys)                                                                   

tray.AddModule( 'I3Writer', 'writer',DropOrphanStreams=[icetray.I3Frame.DAQ, icetray.I3Frame.Stream('M')],
                Streams=[icetray.I3Frame.Geometry, icetray.I3Frame.Calibration,
                        icetray.I3Frame.DetectorStatus, icetray.I3Frame.DAQ, icetray.I3Frame.Physics, icetray.I3Frame.Simulation, icetray.I3Frame.Stream('M')],
                Filename=opts.outputfile)

tray.Execute()
tray.Finish()