#!/data/user/tvaneede/software/py_venvs/py3-v4.4.1_reco-v1.1.0/bin/python

# icecube imports
from icecube import dataio, icetray, dataclasses
from icecube import phys_services, photonics_service, millipede, VHESelfVeto
from icecube.photonics_service import I3PhotoSplineService
from icecube.dataclasses import I3Double, I3Particle, I3Direction, I3Position, I3VectorI3Particle, I3Constants, I3VectorOMKey
from icecube.dataclasses import I3RecoPulse, I3RecoPulseSeriesMap, I3RecoPulseSeriesMapMask, I3TimeWindow, I3TimeWindowSeriesMap
from icecube.icetray import I3Units, I3Frame, I3ConditionalModule, traysegment
from icecube.icetray import I3Tray

from icecube.millipede import HighEnergyExclusions

from segments.MillipedeWrapper import MillipedeWrapper
from segments.FinalEventClassification import checkfinaltopology
from segments.RecoObservables import calculaterecoobservables

# python system imports
import sys, os, datetime
from glob import glob
from os.path import join
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import numpy as np
import pickle
from optparse import OptionParser

parser = OptionParser()
usage = """%prog [options]"""
parser.set_usage(usage)

parser.add_option("-i","--infile",type=str,help="Input Files",dest="infile",action='store')
parser.add_option("-o","--outfile",type=str,help="Output File",dest="outfile",action='store')
(args, extra_args) = parser.parse_args()

tray = I3Tray()

# ice model
base_dir = os.path.expandvars('$I3_DATA/photon-tables/splines')
base = os.path.join(base_dir, 'cascade_single_spice_ftp-v1_flat_z20_a5.%s.fits')
base_eff = os.path.join(base_dir, 'cascade_effectivedistance_spice_ftp-v1_z20.%s.fits')
tiltdir = os.path.expandvars('$I3_SRC/photonics-service/resources/tilt/')
pxs = I3PhotoSplineService(base % "abs", base % "prob",
                        effectivedistancetable=base_eff % "eff",
                        timingSigma=0, tiltTableDir=tiltdir,
                        effectivedistancetableprob=base_eff % "prob",
                        effectivedistancetabletmod=base_eff % "tmod")

# gcd
gcdfilepath = "/data/user/tvaneede/GlobalFit/reco_processing/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz"
gcdfile = dataio.I3File(gcdfilepath)
frame = gcdfile.pop_frame()
while 'I3Geometry' not in frame:
    frame = gcdfile.pop_frame()
geometry = frame['I3Geometry'].omgeo

tray.AddModule('I3Reader', 'reader', FilenameList=[gcdfilepath, args.infile])

# some definitions for energy
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

# init reco
pulses = "SplitInIcePulses" # SplitInIcePulsesIC SplitInIcePulses SplitInIcePulsesICPulseCleaned

tray.Add('Delete', keys=['BrightDOMs', 'DeepCoreDOMs', 'SaturatedDOMs'])
excludedDOMs = tray.Add(HighEnergyExclusions,
    Pulses = pulses,
    BadDomsList = 'BadDomsList',
    CalibrationErrata = 'CalibrationErrata',
    ExcludeBrightDOMs = 'BrightDOMs',
    ExcludeDeepCore = False,
    ExcludeSaturatedDOMs = 'SaturatedDOMs',
    SaturationWindows = 'SaturationTimes') 
millipede_params = {'Pulses': pulses, 'PartialExclusion' : False , 'CascadePhotonicsService' : pxs, 'ExcludedDOMs': excludedDOMs}

# ################################################################
#       ########## MILLIPEDE ENERGY RECONSTRUCTIONS ###########
# ################################################################

tray.Add(MillipedeWrapper, 'HESEMillipedeFit',
    Seeds = ['MonopodFit_iMIGRAD_PPB0', 'TaupedeFit_iMIGRAD_PPB0', 'CscdL3_SPEFit16'],
    PhotonsPerBin = 5,
    ShowerSpacing = 5,
    innerboundary=550,
    outerboundary=650,
    outeredge_x=outeredge_x,
    outeredge_y=outeredge_y,
    **millipede_params)

tray.AddModule(calculaterecoobservables,
	   'calc_reco_observables',
	   innerboundary=550,
	   outeredge_x=outeredge_x,
	   outeredge_y=outeredge_y)

tray.Add(checkfinaltopology)

# ###
# ### zheyang bdt
# ###

# add Qtot/MaxQtotRatio calculations, 
from segments.cscdSBU_misc import misc
tray.AddSegment(misc, 'misc', pulses="OfflinePulses")

# taken from /data/user/tvaneede/GlobalFit/selection/bdt/tau/cascade-final-filter/cscdSBU_vars.py
# and mlb_DelayTime_noNoise.py
from segments.mlb_DelayTime_noNoise import calc_dt_nearly_ice 
tray.AddModule(calc_dt_nearly_ice,'delaytime_monopod_noDC',name='MonopodFit_iMIGRAD_PPB0',
                reconame='MonopodFit_iMIGRAD_PPB0',pulsemapname='OfflinePulsesHLC_noSaturDOMs')

from segments.bdt_var import taupede_monopod_bdt_var
tray.Add(taupede_monopod_bdt_var)

# ### seems to break, invalid pointer problems. I will apply the bdt later
# # from apply_bdt import apply_bdt
# # tray.AddSegment(apply_bdt, "apply_bdt")

###
### cleanup
###

deletekeys= []

tray.Add('Delete', keys=deletekeys)                                                                   

tray.AddModule('I3Writer', 'writer',DropOrphanStreams=[icetray.I3Frame.DAQ],
               Streams=[icetray.I3Frame.Geometry, icetray.I3Frame.Calibration,icetray.I3Frame.Simulation,
                        icetray.I3Frame.DetectorStatus, icetray.I3Frame.DAQ, icetray.I3Frame.Physics, icetray.I3Frame.Stream('M')],
                   Filename=args.outfile)

tray.AddModule('TrashCan', 'yeswecan')
tray.Execute()
tray.Finish()