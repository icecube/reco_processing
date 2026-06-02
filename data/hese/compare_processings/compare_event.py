#!/usr/bin/env python3
"""
Compare a specific event between two icetray i3 files.
Finds RunID==122649, EventID==63903532 in both files and compares:
  - G, C, D frames (byte-for-byte serialisation)
  - SplitInIcePulses, SplitInIcePulsesIC, SplitInIcePulsesICPulseCleaned
    from the P frame, pulse by pulse per DOM
  - All TaupedeFit_iMIGRAD_PPB0* keys from the P frame, field by field
"""

import sys
import os
import tempfile
from icecube import icetray, dataio, dataclasses

FILE_A = "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/data/hese/output/v1/IC86_2013/EvtGen/EvtGen.i3.zst"
FILE_B = "/mnt/ceph1-npx/user/tvaneede/GlobalFit/reco_processing/data/hese/output/test/IC86_2013/EvtGen/EvtGen.i3.zst"

TARGET_RUN_ID   = 122649
TARGET_EVENT_ID = 63903532

FRAME_STOPS  = ["G", "C", "D"]
PULSE_SERIES = [
    "SplitInIcePulses",
    "SplitInIcePulsesIC",
    "SplitInIcePulsesICPulseCleaned",
    "SRTSplitInIcePulses",
    "SRTSplitInIcePulses_IC_Singles_PPB0",
]

PHYSICS_KEYS = [
    "LineFit",
    "SPEFit2",
    "SPEFitSingle",
    "CascadeLlhVertexFit_L2",
    "CascadeLlhVertexFit_L3",
    "CascadeLast_L2",
    "CombinedCascadeSeed_L3",
    "MonopodFit_iMIGRAD_PPB0",
    "TaupedeFit_iMIGRAD_PPB0",
]


# ---------------------------------------------------------------------------
# File scanning
# ---------------------------------------------------------------------------

def extract_event_frames(filepath):
    """
    Walk an i3 file and return {stop: frame} for the target event plus the
    G/C/D frames that immediately precede it.
    """
    f = dataio.I3File(filepath)

    current_g = None
    current_c = None
    current_d = None
    result    = {}

    while f.more():
        frame = f.pop_frame()
        stop  = frame.Stop.id

        if stop == "G":
            current_g = frame
            current_c = None
            current_d = None
        elif stop == "C":
            current_c = frame
            current_d = None
        elif stop == "D":
            current_d = frame
        elif stop in ("Q", "P"):
            if "I3EventHeader" in frame:
                hdr = frame["I3EventHeader"]
                if hdr.run_id == TARGET_RUN_ID and hdr.event_id == TARGET_EVENT_ID:
                    result["G"] = current_g
                    result["C"] = current_c
                    result["D"] = current_d
                    result["Q"] = frame
                    # Collect the P sub-frame(s) that follow this Q frame.
                    while f.more():
                        sub = f.pop_frame()
                        if sub.Stop.id in ("G", "C", "D", "Q"):
                            break  # next event/run started
                        if sub.Stop.id == "P":
                            result.setdefault("P", sub)
                    break

    f.close()

    if not result:
        print(f"  WARNING: event not found in {filepath}")

    return result


# ---------------------------------------------------------------------------
# GCD frame comparison (serialised bytes)
# ---------------------------------------------------------------------------

def serialize_frame_object(frame, key):
    """Write one frame object to a temp .i3 file and return the raw bytes."""
    fd, path = tempfile.mkstemp(suffix=".i3")
    os.close(fd)
    try:
        tmp = icetray.I3Frame(frame.Stop)
        tmp[key] = frame[key]
        f = dataio.I3File(path, "w")
        f.push(tmp)
        f.close()
        with open(path, "rb") as fh:
            return fh.read()
    except Exception:
        return None
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def compare_gcd_frame(stop, frame_a, frame_b, label_a="File A", label_b="File B"):
    print(f"\n{'='*70}")
    print(f"  Frame stop: {stop}")
    print(f"{'='*70}")

    if frame_a is None and frame_b is None:
        print("  Both frames absent.")
        return
    if frame_a is None:
        print(f"  Frame absent in {label_a}, present in {label_b}.")
        return
    if frame_b is None:
        print(f"  Frame absent in {label_b}, present in {label_a}.")
        return

    keys_a  = set(frame_a.keys())
    keys_b  = set(frame_b.keys())
    only_a  = sorted(keys_a - keys_b)
    only_b  = sorted(keys_b - keys_a)
    common  = sorted(keys_a & keys_b)

    if only_a:
        print(f"\n  Keys only in {label_a} ({len(only_a)}): {', '.join(only_a)}")
    if only_b:
        print(f"\n  Keys only in {label_b} ({len(only_b)}): {', '.join(only_b)}")
    if not only_a and not only_b:
        print(f"  Key sets are identical ({len(common)} keys).")

    print(f"\n  Comparing {len(common)} common keys (serialised bytes):")
    identical, different, errors = [], [], []

    for key in common:
        blob_a = serialize_frame_object(frame_a, key)
        blob_b = serialize_frame_object(frame_b, key)
        if blob_a is None or blob_b is None:
            errors.append(key)
        elif blob_a == blob_b:
            identical.append(key)
        else:
            different.append((key, len(blob_a), len(blob_b)))

    if identical:
        print(f"    Identical ({len(identical)}): {', '.join(identical)}")
    if errors:
        print(f"    Could not compare ({len(errors)}): {', '.join(errors)}")
    if not different and not errors:
        print("    All keys are byte-for-byte identical.")
    elif different:
        print(f"    DIFFER ({len(different)}):")
        for key, sz_a, sz_b in different:
            print(f"      {key}  [{label_a}={sz_a} B, {label_b}={sz_b} B]")


# ---------------------------------------------------------------------------
# Pulse series comparison
# ---------------------------------------------------------------------------

def apply_pulse_mask(frame, key):
    """
    Apply an I3RecoPulseSeriesMapMask (or return a plain map) to get a
    concrete {OMKey -> [I3RecoPulse]} dict.
    Returns None if the key is absent.
    """
    if key not in frame:
        return None
    obj = frame[key]
    # If it's a mask, apply it to get the concrete series.
    if isinstance(obj, dataclasses.I3RecoPulseSeriesMapMask):
        psm = obj.apply(frame)
    else:
        psm = obj

    result = {}
    for omkey in psm.keys():
        result[omkey] = list(psm[omkey])
    return result


def pulse_str(p):
    return f"t={p.time:.2f} ns  q={p.charge:.4f} PE  w={p.width:.2f} ns  flags={int(p.flags)}"


def compare_pulse_series(name, frame_a, frame_b, label_a="File A", label_b="File B"):
    print(f"\n{'='*70}")
    print(f"  Pulse series: {name}")
    print(f"{'='*70}")

    psm_a = apply_pulse_mask(frame_a, name)
    psm_b = apply_pulse_mask(frame_b, name)

    if psm_a is None and psm_b is None:
        print(f"  '{name}' absent in both frames.")
        return
    if psm_a is None:
        print(f"  '{name}' absent in {label_a}.")
        return
    if psm_b is None:
        print(f"  '{name}' absent in {label_b}.")
        return

    total_a = sum(len(v) for v in psm_a.values())
    total_b = sum(len(v) for v in psm_b.values())
    doms_a  = set(psm_a.keys())
    doms_b  = set(psm_b.keys())

    print(f"\n  Total pulses : {label_a}={total_a}   {label_b}={total_b}   "
          f"{'SAME' if total_a == total_b else 'DIFFER'}")
    print(f"  Total DOMs   : {label_a}={len(doms_a)}   {label_b}={len(doms_b)}   "
          f"{'SAME' if doms_a == doms_b else 'DIFFER'}")

    only_a = sorted(doms_a - doms_b)
    only_b = sorted(doms_b - doms_a)

    if only_a:
        print(f"\n  DOMs only in {label_a} ({len(only_a)}):")
        for dom in only_a:
            pulses = psm_a[dom]
            print(f"    {dom}  ({len(pulses)} pulse{'s' if len(pulses)!=1 else ''}):")
            for p in pulses:
                print(f"      {pulse_str(p)}")

    if only_b:
        print(f"\n  DOMs only in {label_b} ({len(only_b)}):")
        for dom in only_b:
            pulses = psm_b[dom]
            print(f"    {dom}  ({len(pulses)} pulse{'s' if len(pulses)!=1 else ''}):")
            for p in pulses:
                print(f"      {pulse_str(p)}")

    # Compare shared DOMs pulse by pulse
    shared = sorted(doms_a & doms_b)
    dom_diffs = []
    for dom in shared:
        pa = psm_a[dom]
        pb = psm_b[dom]
        if len(pa) != len(pb):
            dom_diffs.append((dom, pa, pb, "count"))
        else:
            pulse_mismatch = False
            for i, (a, b) in enumerate(zip(pa, pb)):
                if (a.time != b.time or a.charge != b.charge
                        or a.width != b.width or a.flags != b.flags):
                    pulse_mismatch = True
                    break
            if pulse_mismatch:
                dom_diffs.append((dom, pa, pb, "values"))

    if not dom_diffs and not only_a and not only_b:
        print("\n  Pulse series are identical in both files.")
    elif dom_diffs:
        print(f"\n  DOMs with differing pulses ({len(dom_diffs)} / {len(shared)} shared DOMs):")
        for dom, pa, pb, reason in dom_diffs:
            print(f"\n    {dom}  (reason: {reason}  "
                  f"{label_a}: {len(pa)} pulses, {label_b}: {len(pb)} pulses)")
            max_rows = max(len(pa), len(pb))
            for i in range(max_rows):
                a_str = pulse_str(pa[i]) if i < len(pa) else "<absent>"
                b_str = pulse_str(pb[i]) if i < len(pb) else "<absent>"
                marker = "  " if a_str == b_str else "!!"
                print(f"      {marker} [{label_a}] pulse {i}: {a_str}")
                if a_str != b_str:
                    print(f"      {marker} [{label_b}] pulse {i}: {b_str}")
    else:
        print(f"\n  All {len(shared)} shared DOMs have identical pulses.")


# ---------------------------------------------------------------------------
# TaupedeFit / generic physics-key comparison
# ---------------------------------------------------------------------------

def particle_fields(p):
    """Return an ordered list of (field_name, value_str) for an I3Particle."""
    return [
        ("pos.x",      f"{p.pos.x:.4f} m"),
        ("pos.y",      f"{p.pos.y:.4f} m"),
        ("pos.z",      f"{p.pos.z:.4f} m"),
        ("dir.zenith",  f"{p.dir.zenith:.6f} rad"),
        ("dir.azimuth", f"{p.dir.azimuth:.6f} rad"),
        ("energy",     f"{p.energy:.6g} GeV"),
        ("time",       f"{p.time:.4f} ns"),
        ("length",     f"{p.length:.4f} m"),
        ("fit_status", str(p.fit_status)),
        ("shape",      str(p.shape)),
        ("type",       str(p.type)),
    ]


def print_particle_diff(obj_a, obj_b, label_a, label_b, indent="    "):
    fields_a = particle_fields(obj_a)
    fields_b = particle_fields(obj_b)
    any_diff = False
    for (fn, va), (_, vb) in zip(fields_a, fields_b):
        marker = "!!" if va != vb else "  "
        if va != vb:
            any_diff = True
        print(f"{indent}{marker} {fn:14s}  {label_a}: {va}   {label_b}: {vb}")
    if not any_diff:
        print(f"{indent}(all fields identical)")


def print_vector_particle_diff(vec_a, vec_b, label_a, label_b, indent="    "):
    print(f"{indent}Length: {label_a}={len(vec_a)}  {label_b}={len(vec_b)}"
          f"  {'SAME' if len(vec_a)==len(vec_b) else 'DIFFER'}")
    for i in range(max(len(vec_a), len(vec_b))):
        pa = vec_a[i] if i < len(vec_a) else None
        pb = vec_b[i] if i < len(vec_b) else None
        if pa is None:
            print(f"{indent}  particle {i}: absent in {label_a}")
        elif pb is None:
            print(f"{indent}  particle {i}: absent in {label_b}")
        else:
            print(f"{indent}  particle {i}:")
            print_particle_diff(pa, pb, label_a, label_b, indent=indent + "    ")


def print_object_diff(frame_a, frame_b, key, label_a, label_b):
    """Print a detailed field-by-field diff for a single key that is known to differ."""
    obj_a = frame_a[key] if key in frame_a else None
    obj_b = frame_b[key] if key in frame_b else None

    if obj_a is None or obj_b is None:
        print(f"    Key absent in {'A' if obj_a is None else 'B'}.")
        return

    type_a = type(obj_a).__name__

    if type_a == "I3Particle":
        print_particle_diff(obj_a, obj_b, label_a, label_b)

    elif type_a == "I3VectorI3Particle":
        print_vector_particle_diff(obj_a, obj_b, label_a, label_b)

    elif type_a == "I3Double":
        va, vb = obj_a.value, obj_b.value
        marker = "!!" if va != vb else "  "
        print(f"    {marker} value:  {label_a}: {va:.8g}   {label_b}: {vb:.8g}")

    elif type_a in ("I3Bool", "I3Int", "I3String"):
        va, vb = str(obj_a.value), str(obj_b.value)
        marker = "!!" if va != vb else "  "
        print(f"    {marker} value:  {label_a}: {va}   {label_b}: {vb}")

    else:
        print(f"    (type {type_a} — no field-level diff implemented; blobs differ)")


def compare_single_key(key, frame_a, frame_b, label_a="File A", label_b="File B"):
    print(f"\n{'='*70}")
    print(f"  Key: {key}")
    print(f"{'='*70}")

    if frame_a is None or frame_b is None:
        print("  P frame missing in one or both files.")
        return

    in_a = key in frame_a
    in_b = key in frame_b
    if not in_a and not in_b:
        print("  Key absent in both files.")
        return
    if not in_a:
        print(f"  Key absent in {label_a}.")
        return
    if not in_b:
        print(f"  Key absent in {label_b}.")
        return

    blob_a = serialize_frame_object(frame_a, key)
    blob_b = serialize_frame_object(frame_b, key)

    if blob_a is None or blob_b is None:
        print("  Could not serialise for comparison.")
        return

    if blob_a == blob_b:
        obj = frame_a[key]
        print("  Byte-for-byte identical.")
        if type(obj).__name__ == "I3Particle":
            p = obj
            print(f"  pos=({p.pos.x:.4f}, {p.pos.y:.4f}, {p.pos.z:.4f}) m")
            print(f"  zen={p.dir.zenith:.6f} rad  azi={p.dir.azimuth:.6f} rad")
            print(f"  energy={p.energy:.6g} GeV  time={p.time:.4f} ns")
            print(f"  length={p.length:.4f} m  fit_status={p.fit_status}")
    else:
        print_object_diff(frame_a, frame_b, key, label_a, label_b)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Target event  RunID={TARGET_RUN_ID}  EventID={TARGET_EVENT_ID}")
    print(f"\n  File A: {FILE_A}")
    print(f"  File B: {FILE_B}")

    print("\nScanning File A ...")
    frames_a = extract_event_frames(FILE_A)
    print("Scanning File B ...")
    frames_b = extract_event_frames(FILE_B)

    if not frames_a or not frames_b:
        print("\nCould not find event in one or both files. Aborting.")
        sys.exit(1)

    for label, frames in [("File A", frames_a), ("File B", frames_b)]:
        hdr = frames["Q"]["I3EventHeader"]
        print(f"  {label}: found RunID={hdr.run_id} EventID={hdr.event_id}")

    # --- GCD frames ---
    for stop in FRAME_STOPS:
        compare_gcd_frame(
            stop,
            frames_a.get(stop),
            frames_b.get(stop),
            label_a="File A (v1)",
            label_b="File B (test)",
        )

    # --- Pulse series from P frame ---
    p_a = frames_a.get("P")
    p_b = frames_b.get("P")
    for name in PULSE_SERIES:
        compare_pulse_series(name, p_a, p_b, label_a="File A (v1)", label_b="File B (test)")

    # --- Physics keys from P frame ---
    for key in PHYSICS_KEYS:
        compare_single_key(key, p_a, p_b, label_a="File A (v1)", label_b="File B (test)")

    print(f"\n{'='*70}")
    print("Done.")


if __name__ == "__main__":
    main()
