#!/usr/bin/env python3
"""
Search for an event in level2 data by MJD and write it to a standalone i3 file.

The MJD is converted to a calendar date, which is used to locate the right year's
GoodRunInfo file and candidate run directories (matched by MMDD in OutDir).
GCD + matching physics frame are written to the output file.

Usage (via icetray-shell):
    icetray-shell python search_event_by_mjd.py --mjd 56221.342402
    icetray-shell python search_event_by_mjd.py --mjd 56221.342402 --tolerance 5 --output my_event.i3.zst
"""
import argparse
import datetime
import glob
import os
import sys

sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing/data/hese")
from sum_livetimes import get_level, get_config

from icecube import icetray, dataio

RUNINFO_BASE = "/data/exp/IceCube"
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))


def mjd_to_date(mjd):
    return datetime.date(1858, 11, 17) + datetime.timedelta(days=int(mjd))


def parse_runinfo(path):
    """Return list of (run_num, out_dir) for good runs (Good_i3 == 1)."""
    runs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or not line[0].isdigit():
                continue
            parts = line.split()
            if len(parts) < 8:
                continue
            run      = int(parts[0])
            good_i3  = int(parts[1])
            out_dir  = parts[7]
            if good_i3 == 1:
                runs.append((run, out_dir))
    return runs


def find_gcd(run_dir):
    gcds = glob.glob(os.path.join(run_dir, "*GCD*.i3*"))
    return sorted(gcds)[0] if gcds else None


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--mjd",       type=float, required=True,
                        help="Target MJD (floating point)")
    parser.add_argument("--tolerance", type=float, default=1.0,
                        help="Search tolerance in seconds (default: 1)")
    parser.add_argument("--output",    type=str,   default=None,
                        help="Output i3 file (default: event_MJD<mjd>.i3.zst in script dir)")
    args = parser.parse_args()

    target_mjd = args.mjd
    tol_days   = args.tolerance / 86400.0

    date      = mjd_to_date(target_mjd)
    year      = date.year
    mmdd      = date.strftime("%m%d")
    prev_mmdd = (date - datetime.timedelta(days=1)).strftime("%m%d")

    print(f"Target MJD : {target_mjd}")
    print(f"Date       : {date}  (checking OutDir dates {prev_mmdd} and {mmdd})")
    print(f"Tolerance  : {args.tolerance} s")

    level        = get_level(year)
    config       = get_config(year)
    runinfo_path = os.path.join(
        RUNINFO_BASE, str(year), "filtered", level,
        f"{config}_{year}_GoodRunInfo.txt",
    )
    if not os.path.exists(runinfo_path):
        sys.exit(f"ERROR: GoodRunInfo not found: {runinfo_path}")

    all_runs   = parse_runinfo(runinfo_path)
    candidates = [
        (run, out_dir.rstrip("/"))
        for run, out_dir in all_runs
        if f"/{mmdd}/" in out_dir or f"/{prev_mmdd}/" in out_dir
    ]

    print(f"\nGoodRunInfo: {runinfo_path}")
    print(f"Good runs  : {len(all_runs)}")
    print(f"Candidates : {len(candidates)}")
    for run, d in candidates:
        print(f"  Run {run:08d}: {d}")

    if not candidates:
        sys.exit("No candidate runs found — event not in any good run on that date.")

    output_path = args.output or os.path.join(
        SCRIPT_DIR, f"event_MJD{target_mjd:.6f}.i3.zst"
    )

    writer = None
    found  = False

    for run_num, run_dir in candidates:
        gcd_file = find_gcd(run_dir)
        if gcd_file is None:
            print(f"\nWARNING: no GCD in {run_dir}, skipping Run {run_num}")
            continue

        subrun_files = sorted(glob.glob(os.path.join(run_dir, "*Subrun*.i3*")))
        print(f"\nRun {run_num:08d}: {len(subrun_files)} subrun files")

        for subrun_file in subrun_files:
            f = dataio.I3File(subrun_file)
            while f.more():
                frame = f.pop_frame()
                if frame.Stop != icetray.I3Frame.Physics:
                    continue
                if "I3EventHeader" not in frame:
                    continue
                hdr     = frame["I3EventHeader"]
                evt_mjd = hdr.start_time.mod_julian_day_double
                if abs(evt_mjd - target_mjd) <= tol_days:
                    print(f"  FOUND: Run={hdr.run_id}, Event={hdr.event_id}, MJD={evt_mjd:.8f}")
                    if writer is None:
                        writer = dataio.I3File(output_path, "w")
                        gcd = dataio.I3File(gcd_file)
                        while gcd.more():
                            writer.push(gcd.pop_frame())
                        gcd.close()
                    writer.push(frame)
                    found = True
            f.close()

    if writer is not None:
        writer.close()

    if found:
        print(f"\nWrote event to: {output_path}")
    else:
        print("\nEvent NOT FOUND in any candidate run.")


if __name__ == "__main__":
    main()
