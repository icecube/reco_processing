#!/usr/bin/env python3
"""
Evaluate the taupede or monopod millipede likelihood at a fixed particle
hypothesis — no minimisation, no file write.

Uses PyMillipede directly to bypass the gulliver/MINUIT framework: the tau (or
cascade) hypothesis is built from --hypo-key, cascade energies are optimised
analytically, and the resulting logl is compared to a stored MillipedeFitParams
key in the frame.

The geometry (direction / vertex / time / length) is taken from --hypo-key.
Individual coordinates can be overridden on the command line to probe a
different hypothesis.

Examples
--------
# Sanity-check: reproduce the stored taupede logl
python eval_likelihood.py /path/to/Run00126320.i3.zst

# Evaluate monopod likelihood at the stored best-fit position
python eval_likelihood.py /path/to/Run00126320.i3.zst --reco monopod

# Probe a different zenith for a single event
python eval_likelihood.py /path/to/Run00126320.i3.zst \\
    --zenith 45.0 --azimuth 180.0 --event-id 12345
"""

import argparse
import math
import os
import numpy as np

from icecube import icetray, dataio, dataclasses, photonics_service
from icecube import millipede, recclasses, gulliver  # noqa: F401 — needed for deserialisation
from icecube.icetray import I3Tray, I3Units
from reco.mlpd import define_splines
from snowflake import library

# ── constants ─────────────────────────────────────────────────────────────────

EVAL_TAG = 'LLHEval'
SEED_KEY = f'{EVAL_TAG}_seed'

DEFAULT_HYPO_KEY = {
    'taupede': 'TaupedeFit_iMIGRAD_PPB0',
    'monopod': 'MonopodFit_iMIGRAD_PPB0',
}
DEFAULT_COMPARE_KEY = {
    'taupede': 'TaupedeFit_iMIGRAD_PPB0FitParams',
    'monopod': 'MonopodFit_iMIGRAD_PPB0FitParams',
}

# Mirror the millipede parameters used in rec_tau_data_hese.py (ftp-v1, PPB0).
# CascadePhotonicsService is injected at runtime after define_splines().
BASE_MILLIPEDE_PARAMS = {
    'Pulses':               'SplitInIcePulsesICPulseCleaned',
    'MuonPhotonicsService': None,
    'ExcludedDOMs': [
        'BrightDOMs',
        'SaturatedDOMs',
        'DeepCoreDOMs',
        'BadDomsList',
        'CalibrationErrata',
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

# ── hypothesis builders ───────────────────────────────────────────────────────

def tau_hypothesis_sources(tau):
    """
    Replicate TauMillipedeHypothesis from TauMillipede.cxx:
    convert a tau I3Particle into [cc_cascade, decay_cascade].
    """
    zenith = tau.dir.zenith
    azimuth = tau.dir.azimuth
    speed = tau.speed

    xspeed = speed * math.sin(zenith) * math.cos(azimuth)
    yspeed = speed * math.sin(zenith) * math.sin(azimuth)
    zspeed = speed * math.cos(zenith)

    # CC cascade at the tau vertex (copies all fields; shape overridden to Cascade)
    cc = dataclasses.I3Particle(tau)
    cc.shape = dataclasses.I3Particle.Cascade

    # Decay cascade displaced by length along the direction of travel
    delta_t = tau.length / speed
    decay = dataclasses.I3Particle()
    decay.dir = dataclasses.I3Direction(zenith, azimuth)
    decay.length = 0.0
    decay.speed = speed
    decay.shape = dataclasses.I3Particle.Cascade
    decay.time = tau.time + delta_t
    decay.pos = dataclasses.I3Position(
        tau.pos.x - xspeed * delta_t,
        tau.pos.y - yspeed * delta_t,
        tau.pos.z - zspeed * delta_t,
    )

    return [cc, decay]


def mono_hypothesis_sources(particle):
    """Single cascade at the given particle position."""
    p = dataclasses.I3Particle(particle)
    p.shape = dataclasses.I3Particle.Cascade
    return [p]

# ── tray modules ──────────────────────────────────────────────────────────────

def build_seed(frame, hypo_map, overrides):
    """
    Inject SEED_KEY into the frame from hypo_map, applying coordinate overrides.
    hypo_map is keyed by (run_id, event_id) -> I3Particle.
    """
    hdr = frame['I3EventHeader']
    eid = (hdr.run_id, hdr.event_id)
    if eid not in hypo_map:
        icetray.logging.log_warn(
            f'No hypothesis for run {hdr.run_id} event {hdr.event_id} — skipping',
            'eval_likelihood')
        return

    p = dataclasses.I3Particle(hypo_map[eid])

    if overrides['zenith'] is not None:
        p.dir = dataclasses.I3Direction(
            overrides['zenith']  * I3Units.deg,
            overrides['azimuth'] * I3Units.deg)
    if overrides['x'] is not None:
        p.pos = dataclasses.I3Position(overrides['x'], overrides['y'], overrides['z'])
    if overrides['time'] is not None:
        p.time = overrides['time'] * I3Units.ns
    if overrides['length'] is not None:
        p.length = overrides['length'] * I3Units.m

    frame[SEED_KEY] = p


def print_comparison(frame, eval_params_key, stored_map):
    """Print the evaluated logl alongside the stored logl and their difference."""
    hdr = frame['I3EventHeader']
    run, evt = hdr.run_id, hdr.event_id
    eid = (run, evt)

    if not frame.Has(eval_params_key):
        print(f'Run {run}  Event {evt}: missing {eval_params_key}')
        return

    ev = frame[eval_params_key]
    st = stored_map.get(eid)

    print(f'Run {run}  Event {evt}')
    print(f'  Evaluated  ({eval_params_key}):  '
          f'logl={ev.logl:.6f}  rlogl={ev.rlogl:.6f}  ndof={ev.ndof}')
    if st is not None:
        print(f'  Stored     logl={st.logl:.6f}  rlogl={st.rlogl:.6f}  ndof={st.ndof}')
        print(f'  Delta logl: {ev.logl - st.logl:+.6f}')
    else:
        print(f'  (no stored FitParams found for this event)')

# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=(
            'Evaluate taupede or monopod millipede likelihood at a fixed particle '
            'hypothesis using PyMillipede (no minimisation, no file write).'
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('i3file',
                        help='Input .i3[.zst] file — provides pulses and calibration')
    parser.add_argument('--gcd', default=None,
                        help='GCD file to prepend before i3file. Only needed when '
                             'the data file does not contain embedded GCD frames.')
    parser.add_argument('--hypo-file', default=None,
                        help='File to read the hypothesis particle and stored FitParams from. '
                             'Defaults to i3file (same file for everything).')
    parser.add_argument('--reco', choices=('taupede', 'monopod'), default='taupede',
                        help='Likelihood to evaluate')
    parser.add_argument('--particles-key', default=None,
                        help='If set, read hypothesis directly from this I3VectorI3Particle key '
                             '(e.g. TaupedeFit_iMIGRAD_PPB0Particles or Taupede_ftpParticles). '
                             'Bypasses --hypo-key and coordinate overrides.')
    parser.add_argument('--hypo-key', default=None,
                        help='Frame key holding the hypothesis I3Particle (ignored when '
                             '--particles-key is set).')
    parser.add_argument('--compare-key', default=None,
                        help='MillipedeFitParams key to compare against.')
    parser.add_argument('--icemodel', default='ftp-v1',
                        choices=('1', 'mie', 'lea', '3.2.1', 'bfr-v2', 'ftp-v1'),
                        help='Ice model for photon spline tables')
    parser.add_argument('--event-id', type=int, default=None,
                        help='Process only this event ID (all events if not set)')

    # Optional coordinate overrides
    parser.add_argument('--zenith',  type=float, default=None, help='Override zenith [deg]')
    parser.add_argument('--azimuth', type=float, default=None, help='Override azimuth [deg]')
    parser.add_argument('--x',       type=float, default=None, help='Override vertex x [m]')
    parser.add_argument('--y',       type=float, default=None, help='Override vertex y [m]')
    parser.add_argument('--z',       type=float, default=None, help='Override vertex z [m]')
    parser.add_argument('--time',    type=float, default=None, help='Override vertex time [ns]')
    parser.add_argument('--length',  type=float, default=None,
                        help='Override tau decay length [m] (taupede only)')

    args = parser.parse_args()

    compare_key     = args.compare_key or DEFAULT_COMPARE_KEY[args.reco]
    output_key      = f'TaupedeFit_{EVAL_TAG}' if args.reco == 'taupede' else f'MonopodFit_{EVAL_TAG}'
    eval_params_key = output_key + 'FitParams'

    overrides = dict(
        zenith=args.zenith, azimuth=args.azimuth,
        x=args.x, y=args.y, z=args.z,
        time=args.time, length=args.length)

    # ── pre-load hypothesis from hypo-file (or i3file) ───────────────────────
    hypo_source   = args.hypo_file or args.i3file
    particles_map = {}  # (run_id, event_id) -> list[I3Particle]  (--particles-key path)
    hypo_map      = {}  # (run_id, event_id) -> I3Particle        (--hypo-key path)

    print(f'Reading hypothesis from {hypo_source} ...')
    hf = dataio.I3File(hypo_source)
    while hf.more():
        frame = hf.pop_frame()
        if frame.Stop != icetray.I3Frame.Physics:
            continue
        if not frame.Has('I3EventHeader'):
            continue
        hdr = frame['I3EventHeader']
        eid = (hdr.run_id, hdr.event_id)
        if args.particles_key and frame.Has(args.particles_key):
            particles_map[eid] = list(frame[args.particles_key])
        elif not args.particles_key:
            hypo_key = args.hypo_key or DEFAULT_HYPO_KEY[args.reco]
            if frame.Has(hypo_key):
                hypo_map[eid] = dataclasses.I3Particle(frame[hypo_key])
    hf.close()
    n_hypo = len(particles_map) if args.particles_key else len(hypo_map)
    print(f'  Loaded {n_hypo} hypothesis(es).')

    # ── pre-load stored FitParams from the pulses file (i3file) ──────────────
    stored_map = {}  # (run_id, event_id) -> MillipedeFitParams

    pulses_source = args.i3file
    print(f'Reading stored FitParams ({compare_key}) from {pulses_source} ...')
    df = dataio.I3File(pulses_source)
    while df.more():
        frame = df.pop_frame()
        if frame.Stop != icetray.I3Frame.Physics:
            continue
        if not frame.Has('I3EventHeader'):
            continue
        hdr = frame['I3EventHeader']
        eid = (hdr.run_id, hdr.event_id)
        if frame.Has(compare_key):
            stored_map[eid] = frame[compare_key]
    df.close()
    print(f'  Loaded {len(stored_map)} stored FitParams.')

    for (run, evt), particles in (particles_map if args.particles_key else {}).items():
        print(f'  Run {run}  Event {evt}  ({len(particles)} particles):')
        for i, p in enumerate(particles):
            print(f'    [{i}]  pos=({p.pos.x:.2f}, {p.pos.y:.2f}, {p.pos.z:.2f}) m'
                  f'  zen={math.degrees(p.dir.zenith):.3f} deg'
                  f'  az={math.degrees(p.dir.azimuth):.3f} deg'
                  f'  E={p.energy:.2f} GeV'
                  f'  t={p.time:.2f} ns'
                  f'  L={p.length:.2f} m')
    for (run, evt), p in (hypo_map if not args.particles_key else {}).items():
        print(f'  Run {run}  Event {evt}:'
              f'  pos=({p.pos.x:.2f}, {p.pos.y:.2f}, {p.pos.z:.2f}) m'
              f'  zen={math.degrees(p.dir.zenith):.3f} deg'
              f'  az={math.degrees(p.dir.azimuth):.3f} deg'
              f'  E={p.energy:.2f} GeV'
              f'  t={p.time:.2f} ns'
              f'  L={p.length:.2f} m')

    # ── splines and RDE calibration ───────────────────────────────────────────
    print(f'Setting up {args.reco} likelihood with ice model {args.icemodel!r} ...')
    cascade_service = define_splines(args.icemodel, tilt=True, effd=True, effp=True,
                                     qepsilon=1.0, tsig=0.)
    millipede_params = {**BASE_MILLIPEDE_PARAMS, 'CascadePhotonicsService': cascade_service}

    rde_map = library.get_rde_map(os.path.expandvars(
        '$I3_BUILD/ice-models/resources/models/PPCTABLES/misc/eff-f2k.FTP125max'))

    # ── hypothesis function ───────────────────────────────────────────────────
    if args.particles_key:
        # Use stored particle list directly — no seed injection needed.
        def hypothesis_fn(frame):
            hdr = frame['I3EventHeader']
            return particles_map.get((hdr.run_id, hdr.event_id), [])

        def has_hypothesis(frame):
            hdr = frame['I3EventHeader']
            return (hdr.run_id, hdr.event_id) in particles_map
    else:
        # Build hypothesis from a single I3Particle seed.
        if args.reco == 'taupede':
            def hypothesis_fn(frame):
                return tau_hypothesis_sources(frame[SEED_KEY]) if frame.Has(SEED_KEY) else []
        else:
            def hypothesis_fn(frame):
                return mono_hypothesis_sources(frame[SEED_KEY]) if frame.Has(SEED_KEY) else []

        def has_hypothesis(frame):
            return frame.Has(SEED_KEY)

    def is_p_target(frame):
        if frame.Stop != icetray.I3Frame.Physics:
            return True
        if args.event_id is None:
            return True
        return frame.Has('I3EventHeader') and frame['I3EventHeader'].event_id == args.event_id

    filelist = ([args.gcd] if args.gcd else []) + [args.i3file]

    tray = I3Tray()
    tray.Add('I3Reader', Filenamelist=filelist)
    tray.Add(library.update_dom_eff, rde_map=rde_map,
             Streams=[icetray.I3Frame.Calibration])
    tray.Add(is_p_target)

    if not args.particles_key:
        tray.Add(build_seed,
                 hypo_map=hypo_map,
                 overrides=overrides,
                 If=lambda f: f.Stop == icetray.I3Frame.Physics)

    # PyMillipede: builds hypothesis from callable, solves cascade energies
    # analytically, then computes FitStatistics — no minimiser involved.
    tray.Add('PyMillipede', output_key,
             Hypothesis=hypothesis_fn,
             Output=output_key,
             If=lambda f: f.Stop == icetray.I3Frame.Physics and has_hypothesis(f),
             **millipede_params)

    tray.Add(print_comparison,
             eval_params_key=eval_params_key,
             stored_map=stored_map,
             If=lambda f: f.Stop == icetray.I3Frame.Physics and has_hypothesis(f))

    tray.Execute()


if __name__ == '__main__':
    main()
