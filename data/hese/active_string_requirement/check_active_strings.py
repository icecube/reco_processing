"""
Check the active string requirement for HESE reco runs.

Inspired by the checkRuns() function in makedag.py (tyuan).

For each reco run file the script:
  1. Extracts the run number from the filename.
  2. Looks up the run in the GoodRunInfo file to find the GCD file path.
  3. Reads the GCD file (BadDomsList) and checks:
       a. At least 83 active strings (DOMs not flagged bad, outside IceTop positions 61-66).
       b. No inactive strings in the outer layer.
  4. Prints a per-run table and a per-dataset summary.

Run with:
    ./run.sh [--version v2] [--reco-type Taupede] [--datasets IC86_2016 IC86_2017 ...]
"""

from icecube import dataio
import os
import re
import glob
import argparse

RECO_BASE = "/data/user/tvaneede/GlobalFit/reco_processing/data/hese/output"
RUNINFO_BASE = "/data/exp/IceCube"

DATASETS = [
    "IC79_2010",
    "IC86_2011",
    "IC86_2012",
    "IC86_2013",
    "IC86_2014",
    "IC86_2015",
    "IC86_2016",
    "IC86_2017",
    "IC86_2018",
    "IC86_2019",
    "IC86_2020",
    "IC86_2021",
    "IC86_2022",
]

# Outer-layer strings as defined in makedag.py (tyuan)
OUTER_LAYER = frozenset([
    1, 2, 3, 4, 5, 6, 7, 13, 14, 21, 22, 30, 31,
    40, 41, 50, 51, 59, 60, 67, 68, 72, 73, 74, 75, 76, 77, 78,
])

# IceTop DOMs (excluded from in-ice active string count)
ICETOP_OMS = frozenset([61, 62, 63, 64, 65, 66])


def get_level(year):
    return "level2" if year >= 2017 else "level2pass2a"


def get_config(year):
    return "IC79" if year == 2010 else "IC86"


def parse_runlist(path):
    """Parse a GoodRunInfo file.

    Returns dict: run_number (int) -> {good_i3, good_it, active_strings, out_dir, livetime}.
    """
    runs = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or not line[0].isdigit():
                continue
            parts = line.split()
            if len(parts) < 8:
                continue
            run = int(parts[0])
            runs[run] = {
                "good_i3":        int(parts[1]),
                "good_it":        int(parts[2]),
                "livetime":       float(parts[3]),
                "active_strings": int(parts[4]),
                "out_dir":        parts[7],
            }
    return runs


def find_gcd(out_dir, run_number):
    """Return the GCD file path for *run_number* found inside *out_dir*, or None."""
    matches = glob.glob(os.path.join(out_dir, "*%08d*_GCD.i3.*" % run_number))
    return matches[0] if matches else None


def check_run(gcd_path):
    """Read a GCD file and evaluate the active string requirement.

    Returns (n_active, n_inactive_outer, passes) where:
      n_active         — number of strings with ≥1 working in-ice DOM
      n_inactive_outer — number of outer-layer strings that are inactive
      passes           — True if n_active >= 83 and n_inactive_outer == 0
    """
    # Start with all DOMs present; remove bad ones.
    # We consume the BadDomsList inline while the frame is still alive to
    # avoid C++ object lifetime issues after the I3File is garbage-collected
    # (matching the pattern in makedag.py which never stores bdl separately).
    det = {s: set(range(1, 67)) for s in range(1, 87)}
    found = False
    f = dataio.I3File(gcd_path)
    while f.more():
        frame = f.pop_frame()
        if frame.Has("BadDomsList"):
            for bad in frame["BadDomsList"]:
                if 1 <= bad.string <= 86:
                    det[bad.string].discard(bad.om)
            found = True
            break

    if not found:
        raise RuntimeError("No BadDomsList found in %s" % gcd_path)

    # A string is active if it has at least one working in-ice DOM
    active = {s for s, doms in det.items() if doms - ICETOP_OMS}
    inactive = set(range(1, 87)) - active
    n_inactive_outer = len(OUTER_LAYER & inactive)

    passes = len(active) >= 83 and n_inactive_outer == 0
    return len(active), n_inactive_outer, passes


def extract_run_number(filename):
    m = re.match(r"Run0*(\d+)", os.path.basename(filename))
    return int(m.group(1)) if m else None


def process_dataset(ds, version, reco_type):
    """Check all reco runs for one dataset.

    Returns list of dicts with keys:
      run, grl_active, n_active, n_inactive_outer, passes, error
    """
    year = int(ds.split("_")[1])
    level = get_level(year)
    config = get_config(year)

    grl_path = os.path.join(
        RUNINFO_BASE, str(year), "filtered", level,
        "%s_%d_GoodRunInfo.txt" % (config, year),
    )
    reco_dir = os.path.join(RECO_BASE, version, ds, reco_type)

    if not os.path.isdir(reco_dir):
        print("WARNING: reco directory not found: %s" % reco_dir)
        return []

    if not os.path.exists(grl_path):
        print("WARNING: GoodRunInfo not found: %s" % grl_path)
        return []

    runlist = parse_runlist(grl_path)
    reco_files = sorted(glob.glob(os.path.join(reco_dir, "Run*.i3.zst")))

    rows = []
    for reco_file in reco_files:
        run = extract_run_number(reco_file)
        if run is None:
            continue

        row = {"run": run, "good_i3": None, "good_it": None,
               "grl_active": None, "n_active": None,
               "n_inactive_outer": None, "passes": None, "error": None}

        if run not in runlist:
            row["error"] = "not in GRL"
            rows.append(row)
            continue

        run_info = runlist[run]
        row["good_i3"]    = run_info["good_i3"]
        row["good_it"]    = run_info["good_it"]
        row["grl_active"] = run_info["active_strings"]

        gcd = find_gcd(run_info["out_dir"], run)
        if gcd is None:
            row["error"] = "GCD not found in %s" % run_info["out_dir"]
            rows.append(row)
            continue

        try:
            n_active, n_inactive_outer, passes = check_run(gcd)
            row["n_active"] = n_active
            row["n_inactive_outer"] = n_inactive_outer
            row["passes"] = passes
        except Exception as e:
            row["error"] = str(e)

        rows.append(row)

    return rows


def print_dataset_table(ds, rows):
    hdr = "  %10s  %7s  %7s  %10s  %10s  %12s  %6s  %s" % (
        "Run", "Good_i3", "Good_it", "GRL_Active", "GCD_Active", "Inactive_OL", "Pass", "Error")
    sep = "  " + "-" * (len(hdr) - 2)

    print("\n--- %s (%d runs) ---" % (ds, len(rows)))
    print(hdr)
    print(sep)

    for r in rows:
        i3   = str(r["good_i3"])           if r["good_i3"]           is not None else "N/A"
        it   = str(r["good_it"])           if r["good_it"]           is not None else "N/A"
        grl  = str(r["grl_active"])        if r["grl_active"]        is not None else "N/A"
        gcd  = str(r["n_active"])          if r["n_active"]          is not None else "N/A"
        ol   = str(r["n_inactive_outer"])  if r["n_inactive_outer"]  is not None else "N/A"
        pstr = ("PASS" if r["passes"] else "FAIL") if r["passes"] is not None else "N/A"
        err  = r["error"] or ""
        print("  %10d  %7s  %7s  %10s  %10s  %12s  %6s  %s" % (
            r["run"], i3, it, grl, gcd, ol, pstr, err))


def print_summary(all_results):
    hdr = "  %-15s  %6s  %7s  %7s  %6s  %6s  %7s  %s" % (
        "Dataset", "Total", "Bad_i3", "Bad_it", "Pass", "Fail", "Missing", "Errors")
    sep = "  " + "-" * (len(hdr) - 2)

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(hdr)
    print(sep)

    grand = {"total": 0, "bad_i3": 0, "bad_it": 0, "pass": 0, "fail": 0, "missing": 0}

    for ds, rows in all_results:
        total    = len(rows)
        n_bad_i3 = sum(1 for r in rows if r["good_i3"] == 0)
        n_bad_it = sum(1 for r in rows if r["good_it"] == 0)
        n_pass   = sum(1 for r in rows if r["passes"] is True)
        n_fail   = sum(1 for r in rows if r["passes"] is False)
        n_miss   = sum(1 for r in rows if r["passes"] is None)
        errors   = sorted({r["error"] for r in rows if r["error"]})
        err_str  = "; ".join(errors[:2]) + ("..." if len(errors) > 2 else "")
        print("  %-15s  %6d  %7d  %7d  %6d  %6d  %7d  %s" % (
            ds, total, n_bad_i3, n_bad_it, n_pass, n_fail, n_miss, err_str))
        grand["total"]   += total
        grand["bad_i3"]  += n_bad_i3
        grand["bad_it"]  += n_bad_it
        grand["pass"]    += n_pass
        grand["fail"]    += n_fail
        grand["missing"] += n_miss

    print(sep)
    print("  %-15s  %6d  %7d  %7d  %6d  %6d  %7d" % (
        "TOTAL", grand["total"], grand["bad_i3"], grand["bad_it"],
        grand["pass"], grand["fail"], grand["missing"]))
    print("=" * 80)


def print_rm_commands(all_results, version, reco_types):
    """Print rm commands for every run that fails the active string requirement.

    Only runs with passes=False are listed (not N/A / missing GCD).
    Files are not deleted — copy-paste the output to act on it.
    """
    lines = []
    for ds, rows in all_results:
        for r in rows:
            if r["passes"] is not True:
                run = r["run"]
                for reco_type in reco_types:
                    path = os.path.join(
                        RECO_BASE, version, ds, reco_type,
                        "Run%08d.i3.zst" % run,
                    )
                    if os.path.exists(path):
                        lines.append("rm %s" % path)

    if not lines:
        print("\n# No failing runs found — nothing to remove.")
        return

    print("\n# rm commands for runs that fail the active string requirement")
    print("# (%d files). Review before executing.\n" % len(lines))
    for line in lines:
        print(line)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version",   default="v2",
                        help="Reco version subdirectory (default: v2)")
    parser.add_argument("--reco-type", nargs="+", default=["Taupede"],
                        metavar="TYPE",
                        help="Reco type subdirectory/ies (default: Taupede)")
    parser.add_argument("--datasets",  nargs="+", default=None,
                        metavar="DATASET",
                        help="Datasets to check (default: all)")
    parser.add_argument("--print-rm",  action="store_true",
                        help="After the summary, print rm commands for failing runs")
    args = parser.parse_args()

    datasets = args.datasets or DATASETS

    # The active-string check is the same regardless of reco type, so we run
    # the GCD check once per run using the first reco type and reuse the result.
    primary_type = args.reco_type[0]

    all_results = []
    for ds in datasets:
        print("Processing %s ..." % ds, flush=True)
        rows = process_dataset(ds, args.version, primary_type)
        if rows:
            print_dataset_table(ds, rows)
        all_results.append((ds, rows))

    print_summary(all_results)

    if args.print_rm:
        print_rm_commands(all_results, args.version, args.reco_type)


if __name__ == "__main__":
    main()
