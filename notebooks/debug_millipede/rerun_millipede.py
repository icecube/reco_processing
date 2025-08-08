#!/usr/bin/env python3
import os, sys
import argparse
from importlib.metadata import version

from pprint import pformat
import numpy as np

from icecube import dataio
from icecube import (icetray,
                     photonics_service,
                     mue)  # noqa: F401
from icecube.icetray import I3Tray, I3Units
from icecube.phys_services.which_split import which_split
from icecube.millipede import HighEnergyExclusions
from icecube.spline_reco import SplineMPE
from icecube.level3_filter_cascade.level3_Recos import SPEFit

sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")

from segments.VHESelfVeto import SelfVetoWrapper

# for level 3 muon (pulse cleaning needed for splinempe)
from icecube import level3_filter_muon  # noqa: F401

# for srt cleaning
from icecube.STTools.seededRT.configuration_services import I3DOMLinkSeededRTConfigurationService

# for gulliver
from icecube import lilliput
from icecube.gulliver_modules import gulliview

# from snowflake import library, unfold
# from reco import skymap, dom
# from reco.masks import (earlypulses,
#                         maskdc,
#                         maskunhits,
#                         maskstrings,
#                         maskdust,
#                         pulse_cleaning)
# from reco.truth import truth, druth
# from reco.mlpd import (MonopodWrapper,
#                        TaupedeWrapper,
#                        MillipedeWrapper,
#                        preferred,
#                        define_splines)
# from reco.seed import default_seeds

from reco.mlpd import define_splines


from segments.MillipedeWrapper import MillipedeWrapper
from segments.FinalEventClassification import checkfinaltopology
from segments.RecoObservables import calculaterecoobservables
        
# energy definition
gcdfilepath = "/data/user/tvaneede/GlobalFit/reco_processing/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz"
gcdfile = dataio.I3File(gcdfilepath)
frame = gcdfile.pop_frame()
while 'I3Geometry' not in frame:
    frame = gcdfile.pop_frame()
geometry = frame['I3Geometry'].omgeo

strings = [1, 2, 3, 4, 5, 6, 13, 21, 30, 40, 50, 59, 67, 74, 73, 72, 78, 77, 76, 75, 68, 60, 51, 41, 31, 22, 14, 7]

outerbounds = {}
cx, cy = [], []
for string in strings:
    omkey = icetray.OMKey(string, 1)
    # if geometry.has_key(omkey):
    x, y = geometry[omkey].position.x, geometry[omkey].position.y
    outerbounds[string] = (x, y)
    cx.append(x)
    cy.append(y)
cx, cy = np.asarray(cx), np.asarray(cy)
order = np.argsort(np.arctan2(cx, cy))
outeredge_x = cx[order]
outeredge_y = cy[order]

icemodel = "ftp-v1"
tilt = True
effd = True
effp = True
qepsilon = 1.0
tsig = 0.

pulses_for_reco = "SplitInIcePulsesIC" # or SplitInIcePulses neha millipede SplitInIcePulsesIC tianlu
bdthres = 15

cascade_service = define_splines(icemodel, tilt, effd, effp, qepsilon, tsig)

infiles = ["/data/user/tvaneede/GlobalFit/reco_processing/output/v5/22634/0000000-0000999/Reco_NuTau_NuGenCCNC.022634.000000.i3.zst_out.i3.bz2"]

tray = I3Tray()
tray.Add('I3Reader', Filenamelist=infiles)

excludedDOMs = tray.Add(HighEnergyExclusions,
                        Pulses=pulses_for_reco,
                        BrightDOMThreshold=bdthres,
                        ExcludeDeepCore='DeepCoreDOMs_redo',
                        ExcludeBrightDOMs='BrightDOMs_redo',
                        ExcludeSaturatedDOMs='SaturatedDOMs_redo',
                        BadDomsList='BadDomsList_redo',
                        CalibrationErrata='CalibrationErrata_redo',
                        SaturationWindows='SaturationWindows_redo')

print(excludedDOMs)

millipede_params = {'Pulses': pulses_for_reco, 'PartialExclusion' : False , 'CascadePhotonicsService' : cascade_service, 'ExcludedDOMs': excludedDOMs}

# HESE millipede
tray.Add(MillipedeWrapper, 'HESEMillipedeFit_redo',
    Seeds = ['MonopodFit_iMIGRAD_PPB0', 'TaupedeFit_iMIGRAD_PPB0', 'SPEFit16'],
    PhotonsPerBin = 5,
    ShowerSpacing = 5,
    innerboundary=550,
    outerboundary=650,
    outeredge_x=outeredge_x,
    outeredge_y=outeredge_y,
    **millipede_params)

def compare_results(frame):
    eventid = frame['I3EventHeader'].event_id
    print("*******Currently processing eventid %s*******" %eventid)
    print("HESEMillipedeFit", frame["HESEMillipedeFit"])
    print("HESEMillipedeFit_redo", frame["HESEMillipedeFit_redo"])

tray.Add(compare_results)
    

tray.AddModule('I3Writer',
                'writer',
                filename="/data/user/tvaneede/GlobalFit/reco_processing/notebooks/compare_spice_ftp/neha_purity/test.i3.bz2",
                DropOrphanStreams=[icetray.I3Frame.DAQ, icetray.I3Frame.Stream('M'), icetray.I3Frame.TrayInfo],
                streams=[icetray.I3Frame.TrayInfo,
                        icetray.I3Frame.Physics,
                        icetray.I3Frame.Simulation,
                        icetray.I3Frame.Stream('M'),
                        icetray.I3Frame.Stream('X'),
                        icetray.I3Frame.DAQ])

tray.Execute()
