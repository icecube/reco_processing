#!/usr/bin/env python3
"""
Minimal example: evaluate the taupede millipede likelihood at the stored
best-fit position using the two-particle hypothesis stored directly in
TaupedeFit_iMIGRAD_PPB0Particles — no manual hypothesis construction needed.

TaupedeFit stores the [cc_cascade, decay_cascade] list as an I3VectorI3Particle
under '<name>Particles', so we can pass it straight to PyMillipede as-is.

Run with:
    icetray-shell python example_taupede_logl_particles.py
"""

import os
import numpy as np

from icecube import icetray, dataio, dataclasses, photonics_service
from icecube import millipede, recclasses, gulliver  # noqa: F401 — needed for frame deserialisation
from icecube.icetray import I3Tray, I3Units
from reco.mlpd import define_splines
from snowflake import library

# ── configuration ─────────────────────────────────────────────────────────────

I3FILE        = '/data/user/tvaneede/GlobalFit/reco_processing/data/hese/output/v3/IC86_2014/Taupede/Run00126320.i3.zst'
PARTICLES_KEY = 'TaupedeFit_iMIGRAD_PPB0Particles'   # [cc_cascade, decay_cascade]
STORE_KEY     = 'TaupedeFit_iMIGRAD_PPB0FitParams'   # stored result to compare against
EVAL_KEY      = 'TaupedeFit_eval'

MILLIPEDE_PARAMS = {
    'Pulses':               'SplitInIcePulsesICPulseCleaned',
    'MuonPhotonicsService': None,
    'ExcludedDOMs': [
        'BrightDOMs', 'SaturatedDOMs', 'DeepCoreDOMs',
        'BadDomsList', 'CalibrationErrata',
        'SaturationWindows',
        'SplitInIcePulsesICPulseCleanedTimeWindows',
    ],
    'ReadoutWindow':    'SplitInIcePulsesICPulseCleanedTimeRange',
    'PartialExclusion': True,
    'PhotonsPerBin':    0,
    'UseUnhitDOMs':     True,
    'MinTimeWidth':     16,
    'BinSigma':         np.nan,
    'RelUncertainty':   0.05,
}

# ── result printer ─────────────────────────────────────────────────────────────

def print_result(frame):
    hdr = frame['I3EventHeader']
    eval_params_key = EVAL_KEY + 'FitParams'
    if not frame.Has(eval_params_key) or not frame.Has(STORE_KEY):
        print(f'Run {hdr.run_id}  Event {hdr.event_id}: missing keys')
        return
    ev = frame[eval_params_key]
    st = frame[STORE_KEY]
    print(f'Run {hdr.run_id}  Event {hdr.event_id}')
    print(f'  Evaluated  logl={ev.logl:.4f}  ndof={ev.ndof}')
    print(f'  Stored     logl={st.logl:.4f}  ndof={st.ndof}')
    print(f'  Delta logl: {ev.logl - st.logl:+.4f}')

# ── main ──────────────────────────────────────────────────────────────────────

print('Loading photon splines (ftp-v1, tilt+effd+effp) ...')
cascade_service = define_splines('ftp-v1',
                                 tilt=True, effd=True, effp=True,
                                 qepsilon=1.0, tsig=0.)

rde_map = library.get_rde_map(os.path.expandvars(
    '$I3_BUILD/ice-models/resources/models/PPCTABLES/misc/eff-f2k.FTP125max'))

tray = I3Tray()
tray.Add('I3Reader', Filenamelist=[I3FILE])
tray.Add(library.update_dom_eff, rde_map=rde_map,
         Streams=[icetray.I3Frame.Calibration])

tray.Add('PyMillipede', EVAL_KEY,
         Hypothesis=lambda f: list(f[PARTICLES_KEY]) if f.Has(PARTICLES_KEY) else [],
         Output=EVAL_KEY,
         CascadePhotonicsService=cascade_service,
         If=lambda f: f.Stop == icetray.I3Frame.Physics and f.Has(PARTICLES_KEY),
         **MILLIPEDE_PARAMS)

tray.Add(print_result,
         If=lambda f: f.Stop == icetray.I3Frame.Physics and f.Has(PARTICLES_KEY))

tray.Execute()
