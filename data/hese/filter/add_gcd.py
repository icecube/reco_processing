#!/usr/bin/env python3
"""Prepend the correct pass2b GCD to a GCD-stripped i3 file."""

import argparse
import os

from icecube import icetray, dataio
from icecube.icetray import I3Tray

parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("gcdfile")
parser.add_argument("outfile")
opts = parser.parse_args()

os.makedirs(os.path.dirname(os.path.abspath(opts.outfile)), exist_ok=True)

tray = I3Tray()

tray.AddModule('I3Reader', 'reader', filenamelist=[opts.gcdfile, opts.infile])

tray.AddModule('I3Writer', 'writer',
               filename=opts.outfile,
               streams=[icetray.I3Frame.Geometry,
                        icetray.I3Frame.Calibration,
                        icetray.I3Frame.DetectorStatus,
                        icetray.I3Frame.DAQ,
                        icetray.I3Frame.Physics])

tray.Execute()
tray.Finish()
