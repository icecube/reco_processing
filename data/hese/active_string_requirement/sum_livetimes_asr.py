"""
Sum GoodRunInfo livetimes with and without the active string requirement (ASR).

Inspired by sum_livetimes.py.

The full ASR (same as check_active_strings.py) requires:
  1. >= 83 active in-ice strings
  2. No inactive strings in the outer layer

For efficiency the GCD is only read for borderline runs where the GRL
ActiveStrings count is 83–85: those are the only cases where the outer-layer
check can actually change the verdict.  All other runs are decided from the
GRL column alone without touching icetray.

Run with:
    ./run.sh sum_livetimes_asr.py
"""

from icecube import dataio
import os
import glob
import argparse

RUNINFO_BASE = "/data/exp/IceCube"

DATASET_YEARS = [
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

OUTER_LAYER = frozenset([
    1, 2, 3, 4, 5, 6, 7, 13, 14, 21, 22, 30, 31,
    40, 41, 50, 51, 59, 60, 67, 68, 72, 73, 74, 75, 76, 77, 78,
])
ICETOP_OMS  = frozenset([61, 62, 63, 64, 65, 66])

def get_level(year):
    return "level2" if year >= 2017 else "level2pass2a"


def get_config(year):
    return "IC79" if year == 2010 else "IC86"


def parse_grl(path):
    """Parse a GoodRunInfo file.

    Returns list of dicts: run, good_i3, good_it, livetime, active_strings, out_dir.
    """
    runs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or not line[0].isdigit():
                continue
            parts = line.split()
            if len(parts) < 8:
                continue
            runs.append({
                "run":            int(parts[0]),
                "good_i3":        int(parts[1]),
                "good_it":        int(parts[2]),
                "livetime":       float(parts[3]),
                "active_strings": int(parts[4]),
                "out_dir":        parts[7],
            })
    return runs


def find_gcd(out_dir, run_number):
    matches = glob.glob(os.path.join(out_dir, "*%08d*_GCD.i3.*" % run_number))
    return matches[0] if matches else None


def outer_layer_check(gcd_path):
    """Return (n_active, n_inactive_outer) from a GCD file's BadDomsList."""
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
        raise RuntimeError("No BadDomsList in %s" % gcd_path)
    active = {s for s, doms in det.items() if doms - ICETOP_OMS}
    inactive = set(range(1, 87)) - active
    return len(active), len(OUTER_LAYER & inactive)


def passes_asr(run, gcd_cache):
    """Return True/False/None (None = could not determine)."""
    n_active = run["active_strings"]

    # IC79: full complement is 79 strings — treat same as IC86-86 case.
    # All 79 strings active means 86 are physically up (GCD shows 86);
    # the outer-layer check trivially passes.
    is_ic79 = run["run"] < 118175
    full_count = 79 if is_ic79 else 86

    # Fast paths that need no GCD read
    if n_active == full_count:
        return True   # all strings up → outer layer trivially passes
    if n_active < 83:
        return False  # count fails regardless of which strings are down

    # Borderline (83–85 active): need to read the GCD for the outer-layer check
    gcd_path = find_gcd(run["out_dir"], run["run"])
    if gcd_path is None:
        return None

    if gcd_path not in gcd_cache:
        try:
            gcd_cache[gcd_path] = outer_layer_check(gcd_path)
        except Exception as e:
            print("WARNING: run %d GCD error: %s" % (run["run"], e))
            gcd_cache[gcd_path] = None

    result = gcd_cache[gcd_path]
    if result is None:
        return None
    n_active_gcd, n_inactive_outer = result
    return n_active_gcd >= 83 and n_inactive_outer == 0


def process_dataset(ds_year, gcd_cache):
    year = int(ds_year.split("_")[1])
    level = get_level(year)
    config = get_config(year)
    path = os.path.join(
        RUNINFO_BASE, str(year), "filtered", level,
        "%s_%d_GoodRunInfo.txt" % (config, year),
    )
    if not os.path.exists(path):
        print("WARNING: GRL not found: %s" % path)
        return None

    runs = parse_grl(path)
    n_total = len(runs)
    print("Processing %s (%d runs) ..." % (ds_year, n_total), flush=True)
    lt_total = sum(r["livetime"] for r in runs)

    n_bad_i3 = n_bad_it = n_asr_fail = n_pass = n_unknown = 0
    lt_bad_i3 = lt_bad_it = lt_asr_fail = lt_pass = 0.0

    for r in runs:
        if r["good_i3"] != 1:
            n_bad_i3  += 1
            lt_bad_i3 += r["livetime"]
            continue
        if r["good_it"] != 1:
            n_bad_it  += 1
            lt_bad_it += r["livetime"]
            continue
        verdict = passes_asr(r, gcd_cache)
        if verdict is True:
            n_pass    += 1
            lt_pass   += r["livetime"]
        elif verdict is False:
            n_asr_fail  += 1
            lt_asr_fail += r["livetime"]
        else:
            n_unknown += 1

    if n_unknown:
        print("WARNING: %s — %d runs with unknown ASR status (GCD unreadable)"
              % (ds_year, n_unknown))

    return dict(
        n_total=n_total,
        n_bad_i3=n_bad_i3,   lt_bad_i3=lt_bad_i3,
        n_bad_it=n_bad_it,   lt_bad_it=lt_bad_it,
        n_asr_fail=n_asr_fail, lt_asr_fail=lt_asr_fail,
        n_pass=n_pass,       lt_pass=lt_pass,
        lt_total=lt_total,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--datasets", nargs="+", default=None, metavar="DATASET",
                        help="Datasets to process (default: all)")
    args = parser.parse_args()

    datasets = args.datasets or DATASET_YEARS
    gcd_cache = {}

    N = 7   # width for run counts
    W = 16  # width for livetime columns

    header = (
        f"{'Dataset':<15}"
        f"  {'GRL':>{N}}  {'Bad_i3':>{N}}  {'Bad_it':>{N}}  {'ASR_fail':>{N}}  {'Pass':>{N}}"
        f"  {'Total (s)':>{W}}  {'Bad_i3 (s)':>{W}}  {'Bad_it (s)':>{W}}"
        f"  {'ASR_fail (s)':>{W}}  {'Pass (s)':>{W}}  {'Kept (%)':>8}"
    )
    sep = "-" * len(header)
    print(header)
    print(sep)

    grand_keys = ["n_total", "n_bad_i3", "n_bad_it", "n_asr_fail", "n_pass",
                  "lt_total", "lt_bad_i3", "lt_bad_it", "lt_asr_fail", "lt_pass"]
    grand = {k: 0 for k in grand_keys}

    for ds_year in datasets:
        result = process_dataset(ds_year, gcd_cache)
        if result is None:
            continue

        kept_pct = 100.0 * result["lt_pass"] / result["lt_total"] if result["lt_total"] > 0 else 0.0

        print(
            f"{ds_year:<15}"
            f"  {result['n_total']:>{N}}"
            f"  {result['n_bad_i3']:>{N}}"
            f"  {result['n_bad_it']:>{N}}"
            f"  {result['n_asr_fail']:>{N}}"
            f"  {result['n_pass']:>{N}}"
            f"  {result['lt_total']:>{W}.2f}"
            f"  {result['lt_bad_i3']:>{W}.2f}"
            f"  {result['lt_bad_it']:>{W}.2f}"
            f"  {result['lt_asr_fail']:>{W}.2f}"
            f"  {result['lt_pass']:>{W}.2f}"
            f"  {kept_pct:>7.2f}%"
        )

        for key in grand_keys:
            grand[key] += result[key]

    grand_kept_pct = 100.0 * grand["lt_pass"] / grand["lt_total"] if grand["lt_total"] > 0 else 0.0

    print(sep)
    print(
        f"{'TOTAL':<15}"
        f"  {grand['n_total']:>{N}}"
        f"  {grand['n_bad_i3']:>{N}}"
        f"  {grand['n_bad_it']:>{N}}"
        f"  {grand['n_asr_fail']:>{N}}"
        f"  {grand['n_pass']:>{N}}"
        f"  {grand['lt_total']:>{W}.2f}"
        f"  {grand['lt_bad_i3']:>{W}.2f}"
        f"  {grand['lt_bad_it']:>{W}.2f}"
        f"  {grand['lt_asr_fail']:>{W}.2f}"
        f"  {grand['lt_pass']:>{W}.2f}"
        f"  {grand_kept_pct:>7.2f}%"
    )

    n_gcd_reads = sum(1 for v in gcd_cache.values() if v is not None)
    print("\n(GCD files read for borderline runs: %d)" % n_gcd_reads)


if __name__ == "__main__":
    main()
