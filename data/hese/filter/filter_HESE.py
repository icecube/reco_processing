#!/usr/bin/env python3
from icecube import dataio, icetray, dataclasses, simclasses
from icecube.icetray import I3Tray
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import glob
import sys, os

parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("--RunDir", type=str, help="Run directory containing i3 subrun files", dest="rundir")
parser.add_argument("--GCDfile", type=str, help="GCD file for this run", dest="gcdfile")
parser.add_argument("--Outputfile", type=str, help="Output file", dest="outputfile")
opts = parser.parse_args()

# Collect all data i3 files in the run directory (exclude GCD and IceTop files)
# addition: making sure to not look in the files with gaps, the sha512 files and gaps files
data_files = sorted([
    f for f in glob.glob(os.path.join(opts.rundir, "*.i3*"))
    if "GCD" not in os.path.basename(f) and "_IT." not in os.path.basename(f) and "sha512" not in os.path.basename(f) and "gaps" not in os.path.basename(f)
])

if not data_files:
    print(f"No data files found in {opts.rundir}")
    sys.exit(1)

for data_file in data_files:
    print(f"Found data file: {data_file}")

files = [opts.gcdfile] + data_files

n_events = [0]

def count_event(frame):
    n_events[0] += 1
    print(10*"-", "found", frame["I3EventHeader"].event_id)
    print('VHESelfVeto' in frame, "VHESelfVeto",frame['VHESelfVeto'].value)
    print('CausalQTot' in frame, "CausalQTot",frame['CausalQTot'].value)
    print('HESE_VHESelfVeto' in frame, "HESE_VHESelfVeto",frame['HESE_VHESelfVeto'].value)
    print('HESE_CausalQTot' in frame, "HESE_CausalQTot",frame['HESE_CausalQTot'].value)
    return True

tray = I3Tray()
tray.Add("I3Reader", FileNameList=files)

################################################################
############## Tray ###########
################################################################

# sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")
# from segments.VHESelfVeto import SelfVetoWrapper

from icecube import dataio, icetray, dataclasses, DomTools
from icecube import phys_services, photonics_service, millipede, VHESelfVeto
from icecube.photonics_service import I3PhotoSplineService
from icecube.dataclasses import I3Double, I3Particle, I3Direction, I3Position, I3VectorI3Particle, I3Constants, I3VectorOMKey
from icecube.dataclasses import I3RecoPulse, I3RecoPulseSeriesMap, I3RecoPulseSeriesMapMask, I3TimeWindow, I3TimeWindowSeriesMap
from icecube.icetray import I3Units, I3Frame, I3ConditionalModule, traysegment
from I3Tray import I3Tray
@traysegment
def SelfVetoWrapper(tray,name ):
    
    
    pulses = 'SplitInIcePulses'

    """
    full self veto
    """
    tray.AddModule('HomogenizedQTot', 
                   'qtot_total', 
                   Pulses=pulses,
                   Output="QTot")
    # run the veto modules
    tray.AddModule('I3LCPulseCleaning', 
                   'cleaning', 
                   OutputHLC='HLCPulses', 
                   OutputSLC='', 
                   Input=pulses)
    tray.AddModule('VHESelfVeto', 
                   'selfveto', 
                   Pulses='HLCPulses',
                   Geometry="I3Geometry",
                   OutputBool = 'VHESelfVeto')
    tray.AddModule('HomogenizedQTot', 
                   'qtot_causal', 
                   Pulses=pulses, 
                   Output='CausalQTot', 
                   VertexTime='VHESelfVetoVertexTime')
    


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
