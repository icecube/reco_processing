#!/usr/bin/env python3
from icecube import icetray
from icecube.icetray import I3Tray
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import glob, sys, os

sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")
from segments.VHESelfVeto import SelfVetoWrapper

parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("--Inputfile", type=str, required=True,
                    help="Input i3 file or directory of i3 subrun files", dest="inputfile")
parser.add_argument("--GCD", type=str, default=None,
                    help="GCD file to prepend (required when --Inputfile is a run directory)", dest="gcdfile")
parser.add_argument("--Outputfile", type=str, required=True,
                    help="Output i3 file", dest="outputfile")
parser.add_argument("--EventID", type=int, default=None,
                    help="Select a single event by I3EventHeader event_id", dest="event_id")
opts = parser.parse_args()

# Build file list — accept either a single file or a run directory
if os.path.isdir(opts.inputfile):
    data_files = sorted([
        f for f in glob.glob(os.path.join(opts.inputfile, "*.i3*"))
        if "GCD" not in os.path.basename(f)
        and "_IT." not in os.path.basename(f)
        and "sha512" not in os.path.basename(f)
        and "gaps" not in os.path.basename(f)
    ])
    if not data_files:
        print(f"No data files found in {opts.inputfile}")
        sys.exit(1)
    for f in data_files:
        print(f"Found data file: {f}")
else:
    data_files = [opts.inputfile]

files = ([opts.gcdfile] if opts.gcdfile else []) + data_files

n_events = [0]

def count_event(frame):
    n_events[0] += 1
    return True

tray = I3Tray()
tray.Add("I3Reader", FileNameList=files)

# Optionally filter to a single event by event_id
if opts.event_id is not None:
    def select_event(frame):
        if 'I3EventHeader' not in frame:
            return True
        return frame['I3EventHeader'].event_id == opts.event_id
    tray.Add(select_event, Streams=[icetray.I3Frame.Physics])

# Delete pre-existing keys that SelfVetoWrapper will recompute, to avoid conflicts
SELFVETO_KEYS = ["QTot", "HLCPulses", "VHESelfVeto", "VHESelfVetoVertexTime", "VHESelfVetoVertexPos", "CausalQTot"]

def delete_existing_keys(frame):
    for key in SELFVETO_KEYS:
        if key in frame:
            del frame[key]

tray.Add(delete_existing_keys, Streams=[icetray.I3Frame.Physics])

# Run SelfVetoWrapper to add VHESelfVeto, CausalQTot, QTot keys
tray.Add(SelfVetoWrapper)

# Apply veto cut only — no QTot threshold, so full QTot distribution is preserved for comparison
tray.Add(lambda frame: 'VHESelfVeto' in frame and not frame['VHESelfVeto'].value)

tray.Add(count_event, Streams=[icetray.I3Frame.Physics])

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
    print(f"Written {n_events[0]} events to {opts.outputfile}")
else:
    if os.path.exists(opts.outputfile):
        os.remove(opts.outputfile)
    print("No events survived veto cut, skipping output")
