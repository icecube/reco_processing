#!/usr/bin/env python3
"""Strip GCD frames from i3 files by writing only Q and P frames."""

import argparse
import os

from icecube import icetray, dataio
from icecube.icetray import I3Tray

parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("outfile")
opts = parser.parse_args()

os.makedirs(os.path.dirname(os.path.abspath(opts.outfile)), exist_ok=True)

tray = I3Tray()

tray.AddModule('I3Reader', 'reader', filename=opts.infile)

tray.AddModule('I3Writer', 'writer',
               filename=opts.outfile,
               streams=[icetray.I3Frame.DAQ,
                        icetray.I3Frame.Physics])

tray.Execute()
tray.Finish()
