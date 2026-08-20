#!/usr/bin/env python3
"""
Compare pass2a and pass2b GCDs for a given run number.

Reads I3Geometry, I3Calibration, and I3DetectorStatus from both files
and prints a diff of every quantity that differs.

Usage:
    compare_gcd.py --run 121501

Run with:
    /cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/RHEL_7_x86_64_v2/metaprojects/icetray/v1.14.0/bin/icetray-shell \
        /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv/py3-v4.4.1_reco-v1.1.0/bin/python \
        compare_gcd.py --run 121501
"""
import argparse
import glob
import os
import sys
from icecube import dataio, icetray

parser = argparse.ArgumentParser()
parser.add_argument('--run', required=True, type=int, help='Run number (e.g. 121501)')
args = parser.parse_args()

run_str = f'Run{args.run:08d}'

PASS2A_BASE = '/data/exp/IceCube'
PASS2B_BASE = '/data/ana/IceCube'


def find_pass2a_gcd(run_str):
    """Find pass2a GCD, trying variants in order of preference."""
    for variant in ['level2pass2a', 'level2pass2', 'level2']:
        matches = glob.glob(
            os.path.join(PASS2A_BASE, '*', 'filtered', variant, '*', f'{run_str}*', '*GCD*.i3*')
        )
        if matches:
            return matches[0], variant
    return None, None


def find_pass2b_gcd(run_str):
    matches = glob.glob(
        os.path.join(PASS2B_BASE, '*', 'filtered', 'level2pass2b', 'GCD', f'*{run_str}*GCD*.i3*')
    )
    return matches[0] if matches else None


pass2a_path, pass2a_variant = find_pass2a_gcd(run_str)
pass2b_path = find_pass2b_gcd(run_str)

if not pass2a_path:
    sys.exit(f'ERROR: no pass2a/pass2 GCD found for {run_str} under {PASS2A_BASE}')
if not pass2b_path:
    sys.exit(f'ERROR: no pass2b GCD found for {run_str} under {PASS2B_BASE}')

print(f'pass2a ({pass2a_variant}): {pass2a_path}')
print(f'pass2b              : {pass2b_path}')


def read_gcd(path):
    """Return (geo, cal, status, d_frame_keys) from a GCD file."""
    geo = cal = status = None
    d_keys = {}
    f = dataio.I3File(path)
    while f.more():
        frame = f.pop_frame()
        if frame.Stop == icetray.I3Frame.Geometry and geo is None:
            geo = frame['I3Geometry']
        elif frame.Stop == icetray.I3Frame.Calibration and cal is None:
            cal = frame['I3Calibration']
        elif frame.Stop == icetray.I3Frame.DetectorStatus and status is None:
            status = frame['I3DetectorStatus']
            d_keys = {k: frame[k] for k in frame.keys() if k != 'I3DetectorStatus'}
        if geo and cal and status:
            break
    f.close()
    return geo, cal, status, d_keys


geo_a, cal_a, sta_a, d_keys_a = read_gcd(pass2a_path)
geo_b, cal_b, sta_b, d_keys_b = read_gcd(pass2b_path)

print()
print('=' * 70)


# ── I3Geometry ───────────────────────────────────────────────────────────────
print('\n### I3Geometry ###')

keys_a = set(geo_a.omgeo.keys())
keys_b = set(geo_b.omgeo.keys())
only_a = keys_a - keys_b
only_b = keys_b - keys_a
print(f'  DOMs in pass2a only : {len(only_a)}')
if only_a:
    for k in sorted(only_a):
        print(f'    {k}')
print(f'  DOMs in pass2b only : {len(only_b)}')
if only_b:
    for k in sorted(only_b):
        print(f'    {k}')

pos_diffs = []
type_diffs = []
for key in sorted(keys_a & keys_b):
    om_a = geo_a.omgeo[key]
    om_b = geo_b.omgeo[key]
    dx = om_b.position.x - om_a.position.x
    dy = om_b.position.y - om_a.position.y
    dz = om_b.position.z - om_a.position.z
    dr = (dx**2 + dy**2 + dz**2) ** 0.5
    if dr > 1e-6:
        pos_diffs.append((key, dr, dx, dy, dz))
    if om_a.omtype != om_b.omtype:
        type_diffs.append((key, om_a.omtype, om_b.omtype))

print(f'  DOMs with different position : {len(pos_diffs)}')
if pos_diffs:
    print(f'  {"DOM":<12} {"dr [m]":>10} {"dx":>8} {"dy":>8} {"dz":>8}')
    for key, dr, dx, dy, dz in pos_diffs[:20]:
        print(f'  {str(key):<12} {dr:>10.4f} {dx:>8.4f} {dy:>8.4f} {dz:>8.4f}')
    if len(pos_diffs) > 20:
        print(f'  ... and {len(pos_diffs)-20} more')

print(f'  DOMs with different OMType   : {len(type_diffs)}')
for key, ta, tb in type_diffs[:10]:
    print(f'    {key}: {ta} -> {tb}')


# ── I3Calibration ────────────────────────────────────────────────────────────
print('\n### I3Calibration ###')


def compare_dom_calib(cal_a, cal_b, attr, tol=1e-9):
    """Compare a scalar attribute in dom_cal for all shared DOMs."""
    keys_a = set(cal_a.dom_cal.keys())
    keys_b = set(cal_b.dom_cal.keys())
    diffs = []
    for key in sorted(keys_a & keys_b):
        va = getattr(cal_a.dom_cal[key], attr, None)
        vb = getattr(cal_b.dom_cal[key], attr, None)
        if va is None or vb is None:
            continue
        try:
            if abs(float(va) - float(vb)) > tol:
                diffs.append((key, float(va), float(vb)))
        except TypeError:
            pass
    return diffs


keys_a = set(cal_a.dom_cal.keys())
keys_b = set(cal_b.dom_cal.keys())
only_a = keys_a - keys_b
only_b = keys_b - keys_a
print(f'  DOMs in pass2a cal only : {len(only_a)}')
if only_a:
    for k in sorted(only_a): print(f'    {k}')
print(f'  DOMs in pass2b cal only : {len(only_b)}')
if only_b:
    for k in sorted(only_b): print(f'    {k}')

attr_tol = {
    'relative_dom_eff': 1e-3,
}
for attr in ['dom_noise_rate', 'dom_noise_thermal_rate', 'dom_noise_decay_rate',
             'dom_noise_scintillation_mean', 'dom_noise_scintillation_sigma',
             'relative_dom_eff', 'mean_atwd_charge', 'mean_fadc_charge']:
    diffs = compare_dom_calib(cal_a, cal_b, attr, tol=attr_tol.get(attr, 1e-9))
    print(f'  {attr}: {len(diffs)} DOMs differ')
    if diffs:
        print(f'    {"DOM":<12} {"pass2a":>14} {"pass2b":>14} {"diff":>14}')
        for key, va, vb in diffs[:5]:
            print(f'    {str(key):<12} {va:>14.6g} {vb:>14.6g} {vb-va:>+14.6g}')
        if len(diffs) > 5:
            print(f'    ... and {len(diffs)-5} more')

# ATWD gain (proxy object — access by channel index directly)
n_atwd_diff = 0
for key in sorted(keys_a & keys_b):
    dc_a = cal_a.dom_cal[key]
    dc_b = cal_b.dom_cal[key]
    for ch in range(3):
        try:
            ga = dc_a.atwd_gain[ch]
            gb = dc_b.atwd_gain[ch]
            if abs(ga - gb) > 1e-9:
                n_atwd_diff += 1
        except Exception:
            pass
print(f'  atwd_gain entries that differ: {n_atwd_diff}')


# ── I3DetectorStatus ─────────────────────────────────────────────────────────
print('\n### I3DetectorStatus ###')

keys_a = set(sta_a.dom_status.keys())
keys_b = set(sta_b.dom_status.keys())
only_a = keys_a - keys_b
only_b = keys_b - keys_a
print(f'  DOMs in pass2a status only : {len(only_a)}')
if only_a:
    for k in sorted(only_a): print(f'    {k}')
print(f'  DOMs in pass2b status only : {len(only_b)}')
if only_b:
    for k in sorted(only_b): print(f'    {k}')

# PMT HV
hv_diffs = []
for key in sorted(keys_a & keys_b):
    va = sta_a.dom_status[key].pmt_hv
    vb = sta_b.dom_status[key].pmt_hv
    if abs(va - vb) > 1e-3:
        hv_diffs.append((key, va, vb))
print(f'  DOMs with different PMT HV : {len(hv_diffs)}')
if hv_diffs:
    print(f'  {"DOM":<12} {"pass2a [V]":>12} {"pass2b [V]":>12}')
    for key, va, vb in hv_diffs[:10]:
        print(f'  {str(key):<12} {va:>12.2f} {vb:>12.2f}')
    if len(hv_diffs) > 10:
        print(f'  ... and {len(hv_diffs)-10} more')

# LC span
lc_diffs = []
for key in sorted(keys_a & keys_b):
    va = sta_a.dom_status[key].lc_span
    vb = sta_b.dom_status[key].lc_span
    if va != vb:
        lc_diffs.append((key, va, vb))
print(f'  DOMs with different LC span : {len(lc_diffs)}')
for key, va, vb in lc_diffs[:10]:
    print(f'    {key}: {va} -> {vb}')

# DOM active/inactive
dom_active_a = {k for k in keys_a if sta_a.dom_status[k].pmt_hv > 0}
dom_active_b = {k for k in keys_b if sta_b.dom_status[k].pmt_hv > 0}
newly_off = dom_active_a - dom_active_b
newly_on  = dom_active_b - dom_active_a
print(f'  DOMs active (HV>0) pass2a  : {len(dom_active_a)}')
print(f'  DOMs active (HV>0) pass2b  : {len(dom_active_b)}')
print(f'  Active in pass2a, off in pass2b : {len(newly_off)}')
for k in sorted(newly_off)[:10]: print(f'    {k}')
print(f'  Active in pass2b, off in pass2a : {len(newly_on)}')
for k in sorted(newly_on)[:10]: print(f'    {k}')

# Trigger status summary
print(f'\n  Trigger configurations:')
print(f'    pass2a triggers: {len(sta_a.trigger_status)}')
print(f'    pass2b triggers: {len(sta_b.trigger_status)}')


# ── BadDomsList ──────────────────────────────────────────────────────────────
print('\n### BadDomsList ###')
print(f'  Extra keys in pass2a D frame: {list(d_keys_a.keys())}')
print(f'  Extra keys in pass2b D frame: {list(d_keys_b.keys())}')

for list_key in ['BadDomsList', 'BadDomsListSLC', 'DeepCoreDOMs']:
    bdl_a = d_keys_a.get(list_key)
    bdl_b = d_keys_b.get(list_key)
    if bdl_a is None and bdl_b is None:
        print(f'  {list_key}: not present in either GCD')
        continue
    set_a = set(bdl_a) if bdl_a is not None else set()
    set_b = set(bdl_b) if bdl_b is not None else set()
    only_a = sorted(set_a - set_b)
    only_b = sorted(set_b - set_a)
    print(f'  {list_key}:')
    print(f'    pass2a count : {len(set_a)}')
    print(f'    pass2b count : {len(set_b)}')
    print(f'    in pass2a only ({len(only_a)}):')
    for k in only_a: print(f'      {k}')
    print(f'    in pass2b only ({len(only_b)}):')
    for k in only_b: print(f'      {k}')

# Derive bad DOMs from HV==0
bad_a = {k for k in sta_a.dom_status.keys() if sta_a.dom_status[k].pmt_hv == 0}
bad_b = {k for k in sta_b.dom_status.keys() if sta_b.dom_status[k].pmt_hv == 0}
only_a = sorted(bad_a - bad_b)
only_b = sorted(bad_b - bad_a)
print(f'\n  Bad DOMs derived from HV==0 in DetectorStatus:')
print(f'    pass2a: {len(bad_a)} bad DOMs')
print(f'    pass2b: {len(bad_b)} bad DOMs')
print(f'    Bad in pass2a only ({len(only_a)}): {only_a[:20]}')
print(f'    Bad in pass2b only ({len(only_b)}): {only_b[:20]}')

print('\n### Done ###')
