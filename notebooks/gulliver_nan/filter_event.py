from icecube import dataio, icetray, dataclasses, simclasses
from icecube.icetray import I3Tray
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from glob import glob
import sys, os, datetime


inputfile = ["/data/sim/IceCube/2023/filtered/level2/neutrino-generator/22634/0000000-0000999/Level2_NuTau_NuGenCCNC.022634.000001.i3.zst"]
event_id = 3327
outputfile = f"/data/user/tvaneede/GlobalFit/reco_processing/notebooks/gulliver_nan/Level2_NuTau_NuGenCCNC.022634.000001.event_id_{event_id}.i3.zst"


tray = I3Tray()
tray.Add("I3Reader", FileNameList=inputfile)

################################################################
############## Energy cut and Final Event selections ###########
################################################################

tray.Add( lambda frame: frame['I3EventHeader'].event_id == event_id )

################################################################
########################### Wrap it up #########################
################################################################                                                      

tray.AddModule( 'I3Writer', 'writer',DropOrphanStreams=[icetray.I3Frame.DAQ, icetray.I3Frame.Stream('M')],
                Streams=[icetray.I3Frame.Geometry, icetray.I3Frame.Calibration,
                        icetray.I3Frame.DetectorStatus, icetray.I3Frame.DAQ, icetray.I3Frame.Physics, icetray.I3Frame.Simulation, icetray.I3Frame.Stream('M')],
                Filename=outputfile)

tray.Execute()
tray.Finish()