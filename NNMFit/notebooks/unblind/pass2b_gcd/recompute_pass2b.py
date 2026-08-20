#!/usr/bin/env python3
"""
Recompute CausalQTot and VHESelfVeto using pass2b GCDs for HESE v3 output files.

The v3 files have an old GCD embedded in their G/C/D frames. This script replaces
those frames with the matching pass2b GCD from /data/ana/IceCube/ and recomputes
the veto/charge quantities, storing results as CausalQTot_pass2b and
VHESelfVeto_pass2b alongside the original values.

Usage:
    icetray-shell python recompute_pass2b.py \
        --InputFile <v3_file.i3.zst> \
        --Season IC86_2011 \
        --OutputDir <output_dir>
"""
from icecube import dataio, icetray, dataclasses, DomTools, VHESelfVeto
from icecube.icetray import I3Tray
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import glob
import sys
import os
import re

GCD_BASE = '/data/ana/IceCube'

# Calendar year folders to search for each IceCube season's pass2b GCDs.
# Each season spans two calendar years; we search both to handle run-number
# boundaries that fall near the season transition.
SEASON_SEARCH_YEARS = {
    'IC79_2010':  ['2010', '2011'],
    'IC86_2011':  ['2011', '2012'],
    'IC86_2012':  ['2012', '2013'],
    'IC86_2013':  ['2013', '2014'],
    'IC86_2014':  ['2014', '2015'],
    'IC86_2015':  ['2015', '2016'],
    'IC86_2016':  ['2016', '2017'],
    'IC86_2017':  ['2017', '2018'],
    'IC86_2018':  ['2018', '2019'],
    'IC86_2019':  ['2019', '2020'],
    'IC86_2020':  ['2020', '2021'],
    'IC86_2021':  ['2021', '2022'],
    'IC86_2022':  ['2022', '2023'],
}


def find_pass2b_gcd(input_file, season):
    """Find the pass2b GCD file whose run number matches the input filename."""
    m = re.search(r'Run(\d+)', os.path.basename(input_file))
    if not m:
        raise ValueError(f"Cannot extract run number from {os.path.basename(input_file)}")
    run_str = f'Run{int(m.group(1)):08d}'

    years = SEASON_SEARCH_YEARS.get(season, [])
    for year in years:
        gcd_dir = os.path.join(GCD_BASE, year, 'filtered', 'level2pass2b', 'GCD')
        if not os.path.isdir(gcd_dir):
            continue
        matches = glob.glob(os.path.join(gcd_dir, f'*{run_str}*GCD*.i3*'))
        if matches:
            return matches[0]

    raise FileNotFoundError(
        f"No pass2b GCD found for {run_str} in season {season} "
        f"(searched: {[os.path.join(GCD_BASE, y, 'filtered', 'level2pass2b', 'GCD') for y in years]})"
    )


def load_gcd_objects(gcd_path):
    """Return I3Geometry, I3Calibration, I3DetectorStatus from a GCD file."""
    objects = {}
    f = dataio.I3File(gcd_path)
    while f.more():
        frame = f.pop_frame()
        if frame.Stop == icetray.I3Frame.Geometry and 'I3Geometry' in frame:
            objects['I3Geometry'] = frame['I3Geometry']
        elif frame.Stop == icetray.I3Frame.Calibration and 'I3Calibration' in frame:
            objects['I3Calibration'] = frame['I3Calibration']
        elif frame.Stop == icetray.I3Frame.DetectorStatus and 'I3DetectorStatus' in frame:
            objects['I3DetectorStatus'] = frame['I3DetectorStatus']
    f.close()

    for key in ('I3Geometry', 'I3Calibration', 'I3DetectorStatus'):
        if key not in objects:
            raise RuntimeError(f"{gcd_path} is missing {key}")

    return objects


class GCDReplacingReader(icetray.I3Module):
    """
    Source module that reads an i3 file and replaces the G/C/D frame objects
    with externally supplied ones before pushing each frame downstream.

    This is necessary because the I3FrameMixer copies parent frames into its
    cache when they are first pushed, so replacing objects after the fact has
    no effect on how P frames inherit GCD content.
    """

    def __init__(self, context):
        icetray.I3Module.__init__(self, context)
        self.AddParameter('Filename', 'Input i3 file to read', '')
        self.AddParameter('NewGeometry', 'Replacement I3Geometry object', None)
        self.AddParameter('NewCalibration', 'Replacement I3Calibration object', None)
        self.AddParameter('NewDetectorStatus', 'Replacement I3DetectorStatus object', None)
        self._file = None

    def Configure(self):
        self._filename = self.GetParameter('Filename')
        self._new_geo = self.GetParameter('NewGeometry')
        self._new_cal = self.GetParameter('NewCalibration')
        self._new_det = self.GetParameter('NewDetectorStatus')
        self._file = dataio.I3File(self._filename)

    def Process(self):
        if not self._file.more():
            self.RequestSuspension()
            return

        frame = self._file.pop_frame()

        if frame.Stop == icetray.I3Frame.Geometry:
            if 'I3Geometry' in frame:
                frame.Delete('I3Geometry')
            frame['I3Geometry'] = self._new_geo

        elif frame.Stop == icetray.I3Frame.Calibration:
            if 'I3Calibration' in frame:
                frame.Delete('I3Calibration')
            frame['I3Calibration'] = self._new_cal

        elif frame.Stop == icetray.I3Frame.DetectorStatus:
            if 'I3DetectorStatus' in frame:
                frame.Delete('I3DetectorStatus')
            frame['I3DetectorStatus'] = self._new_det

        self.PushFrame(frame)

    def Finish(self):
        if self._file is not None:
            self._file.close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('--InputFile',  required=True,
                    help='v3 HESE i3 file to reprocess')
parser.add_argument('--Season',     required=True, choices=list(SEASON_SEARCH_YEARS.keys()),
                    help='IceCube season name, e.g. IC86_2011')
parser.add_argument('--OutputDir',  required=True,
                    help='Directory where the output file will be written')
opts = parser.parse_args()

os.makedirs(opts.OutputDir, exist_ok=True)
output_file = os.path.join(opts.OutputDir, os.path.basename(opts.InputFile))

gcd_path = find_pass2b_gcd(opts.InputFile, opts.Season)
print(f"Input:   {opts.InputFile}")
print(f"GCD:     {gcd_path}")
print(f"Output:  {output_file}")

gcd_objects = load_gcd_objects(gcd_path)

# ---------------------------------------------------------------------------
# Tray
# ---------------------------------------------------------------------------

pulses = 'SplitInIcePulses'

tray = I3Tray()

tray.Add(GCDReplacingReader,
         Filename=opts.InputFile,
         NewGeometry=gcd_objects['I3Geometry'],
         NewCalibration=gcd_objects['I3Calibration'],
         NewDetectorStatus=gcd_objects['I3DetectorStatus'])

# Recompute LC-cleaned pulses, VHE self-veto, and causal charge with pass2b GCD.
# OutputVertexTime is configurable (default: "VHESelfVetoVertexTime"), so we
# use a _pass2b suffix to avoid overwriting the original intermediate values.
tray.AddModule('I3LCPulseCleaning', 'cleaning_pass2b',
               Input=pulses,
               OutputHLC='HLCPulses_pass2b',
               OutputSLC='')

tray.AddModule('VHESelfVeto', 'selfveto_pass2b',
               Pulses='HLCPulses_pass2b',
               Geometry='I3Geometry',
               OutputBool='VHESelfVeto_pass2b',
               OutputVertexTime='VHESelfVetoVertexTime_pass2b',
               OutputVertexPos='VHESelfVetoVertexPos_pass2b')

tray.AddModule('HomogenizedQTot', 'qtot_causal_pass2b',
               Pulses=pulses,
               Output='CausalQTot_pass2b',
               VertexTime='VHESelfVetoVertexTime_pass2b')

tray.AddModule('I3Writer', 'writer',
               filename=output_file,
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

print(f"Done. Written to {output_file}")
