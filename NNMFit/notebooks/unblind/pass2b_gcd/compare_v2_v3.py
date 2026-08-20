#!/usr/bin/env python3
"""
Compare CausalQTot and VHESelfVeto between v2 and v3 filter outputs
for seasons IC79_2010 – IC86_2015.

Run with:
    /cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell \
        /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
        compare_v2_v3.py
"""
from icecube import dataio, icetray
import glob
import os

SEASONS = [
    'IC79_2010', 'IC86_2011', 'IC86_2012',
    'IC86_2013', 'IC86_2014', 'IC86_2015',
]

V2_BASE = '/data/user/tvaneede/GlobalFit/reco_processing/data/hese/filter/output/v2'
V3_BASE = '/data/user/tvaneede/GlobalFit/reco_processing/data/hese/filter/output/v3'


def read_events(i3_path):
    """Return dict keyed by event_id → (CausalQTot, VHESelfVeto)."""
    events = {}
    f = dataio.I3File(i3_path)
    while f.more():
        frame = f.pop_frame()
        if frame.Stop != icetray.I3Frame.Physics:
            continue
        hdr = frame['I3EventHeader']
        key = (hdr.run_id, hdr.event_id)
        qtot = frame['CausalQTot'].value if 'CausalQTot' in frame else None
        veto = frame['VHESelfVeto'].value if 'VHESelfVeto' in frame else None
        events[key] = (qtot, veto)
    f.close()
    return events


# Accumulators
rows = []   # (season, run_file, run_id, event_id, qtot_v2, qtot_v3, veto_v2, veto_v3)

for season in SEASONS:
    v2_dir = os.path.join(V2_BASE, season)
    v3_dir = os.path.join(V3_BASE, season)

    v2_files = {os.path.basename(p): p for p in sorted(glob.glob(os.path.join(v2_dir, 'Run*.i3*')))}
    v3_files = {os.path.basename(p): p for p in sorted(glob.glob(os.path.join(v3_dir, 'Run*.i3*')))}

    common = sorted(set(v2_files) & set(v3_files))
    print(f'{season}: {len(common)} common run files')

    for fname in common:
        ev_v2 = read_events(v2_files[fname])
        ev_v3 = read_events(v3_files[fname])

        all_keys = sorted(set(ev_v2) | set(ev_v3))
        for key in all_keys:
            run_id, event_id = key
            qtot_v2, veto_v2 = ev_v2.get(key, (None, None))
            qtot_v3, veto_v3 = ev_v3.get(key, (None, None))
            rows.append((season, fname, run_id, event_id, qtot_v2, qtot_v3, veto_v2, veto_v3))

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

n_total   = len(rows)
n_v2_only = sum(1 for r in rows if r[5] is None)
n_v3_only = sum(1 for r in rows if r[4] is None)
n_both    = sum(1 for r in rows if r[4] is not None and r[5] is not None)

print()
print('=' * 70)
print(f'Total events seen : {n_total}')
print(f'  In both v2 & v3 : {n_both}')
print(f'  In v2 only      : {n_v2_only}')
print(f'  In v3 only      : {n_v3_only}')

# --- CausalQTot ---
qtot_changed = [r for r in rows if r[4] is not None and r[5] is not None and abs(r[4] - r[5]) > 0]
print()
print(f'Events with different CausalQTot (v2 vs v3): {len(qtot_changed)}')
if qtot_changed:
    print(f'  {"Season":<12} {"Run":>10} {"Event":>12} {"v2 QTot":>12} {"v3 QTot":>12} {"Diff":>10}')
    print('  ' + '-' * 64)
    for season, fname, run_id, event_id, q2, q3, _, _ in qtot_changed:
        print(f'  {season:<12} {run_id:>10} {event_id:>12} {q2:>12.1f} {q3:>12.1f} {q3-q2:>+10.1f}')

# --- VHESelfVeto ---
veto_changed = [r for r in rows if r[6] is not None and r[7] is not None and r[6] != r[7]]
print()
print(f'Events with different VHESelfVeto (v2 vs v3): {len(veto_changed)}')
if veto_changed:
    print(f'  {"Season":<12} {"Run":>10} {"Event":>12} {"v2 Veto":>10} {"v3 Veto":>10}')
    print('  ' + '-' * 52)
    for season, fname, run_id, event_id, q2, q3, v2, v3 in veto_changed:
        print(f'  {season:<12} {run_id:>10} {event_id:>12} {str(v2):>10} {str(v3):>10}')

# --- Events only in one version ---
if n_v2_only:
    print()
    print('Events only in v2 (dropped in v3):')
    print(f'  {"Season":<12} {"Run":>10} {"Event":>12} {"v2 QTot":>12} {"v2 Veto":>10}')
    print('  ' + '-' * 52)
    for season, fname, run_id, event_id, q2, q3, v2, v3 in rows:
        if q3 is None:
            print(f'  {season:<12} {run_id:>10} {event_id:>12} {q2:>12.1f} {str(v2):>10}')

if n_v3_only:
    print()
    print('Events only in v3 (new in v3):')
    print(f'  {"Season":<12} {"Run":>10} {"Event":>12} {"v3 QTot":>12} {"v3 Veto":>10}')
    print('  ' + '-' * 52)
    for season, fname, run_id, event_id, q2, q3, v2, v3 in rows:
        if q2 is None:
            print(f'  {season:<12} {run_id:>10} {event_id:>12} {q3:>12.1f} {str(v3):>10}')
