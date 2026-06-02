#!/usr/bin/env python3
from icecube import dataio, icetray, dataclasses, simclasses
from icecube.icetray import I3Tray
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import glob
import sys, os

sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")
from segments.VHESelfVeto import SelfVetoWrapper

parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("--RunDir", type=str, help="Run directory containing i3 subrun files", dest="rundir")
parser.add_argument("--GCDfile", type=str, help="GCD file for this run", dest="gcdfile")
parser.add_argument("--Outputfile", type=str, help="Output file", dest="outputfile")
opts = parser.parse_args()

# Collect all data i3 files in the run directory (exclude GCD and IceTop files)
data_files = sorted([
    f for f in glob.glob(os.path.join(opts.rundir, "*.i3*"))
    if "GCD" not in os.path.basename(f) and "_IT." not in os.path.basename(f)
])

if not data_files:
    print(f"No data files found in {opts.rundir}")
    sys.exit(1)

files = [opts.gcdfile] + data_files

n_events = [0]

def count_event(frame):
    n_events[0] += 1
    return True

tray = I3Tray()
tray.Add("I3Reader", FileNameList=files)

################################################################
############## HESE Event selection ###########
################################################################

tray.Add(SelfVetoWrapper)
tray.Add(lambda frame : 'HESE_VHESelfVeto' in frame and not frame['HESE_VHESelfVeto'].value)
tray.Add(lambda frame : 'HESE_CausalQTot' in frame and frame['HESE_CausalQTot'].value >= 6000)

tray.Add(count_event, Streams=[icetray.I3Frame.Physics])

################################################################
########################### Wrap it up #########################
################################################################

tray.AddModule('I3Writer',
                'writer',
                filename=opts.outputfile,
                   DropOrphanStreams=[icetray.I3Frame.DAQ, 
                                      icetray.I3Frame.Stream('M'), 
                                      icetray.I3Frame.TrayInfo, 
                                      icetray.I3Frame.Calibration, 
                                      icetray.I3Frame.DetectorStatus,
                                      icetray.I3Frame.Geometry],
                   streams=[icetray.I3Frame.TrayInfo,
                            icetray.I3Frame.Physics,
                            icetray.I3Frame.Geometry,
                            icetray.I3Frame.Calibration,
                            icetray.I3Frame.Simulation,
                            icetray.I3Frame.Stream('M'),
                            icetray.I3Frame.Stream('X'),
                            icetray.I3Frame.DetectorStatus,
                            icetray.I3Frame.DAQ])

tray.Execute()
tray.Finish()

if n_events[0] > 0:
    print(f"Written {n_events[0]} HESE events to {opts.outputfile}")
else:
    if os.path.exists(opts.outputfile):
        os.remove(opts.outputfile)
    print("No HESE events found, skipping output")
