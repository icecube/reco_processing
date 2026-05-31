#!/usr/bin/env python3
"""Sum livetimes for HESE dataset runs from GoodRunInfo files."""

import os
import re

HESE_BASE = "/data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/HESE"
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
]


def get_level(year):
    return "level2" if year >= 2017 else "level2pass2a"


def get_config(year_int):
    return "IC79" if year_int == 2010 else "IC86"


def parse_runlist(path):
    """Return dict mapping run_number (int) -> livetime (float) from a GoodRunInfo file."""
    livetimes = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or not line[0].isdigit():
                continue
            parts = line.split()
            if len(parts) < 4:
                continue
            run = int(parts[0])
            livetime = float(parts[3])
            livetimes[run] = livetime
    return livetimes


def load_runlists(ds_year, versioned=False):
    year_int = int(ds_year.split("_")[1])
    level = get_level(year_int)
    config = get_config(year_int)
    suffix = "_Versioned" if versioned else ""
    path = os.path.join(
        RUNINFO_BASE,
        str(year_int),
        "filtered",
        level,
        f"{config}_{year_int}_GoodRunInfo{suffix}.txt",
    )
    if not os.path.exists(path):
        return None, path
    return parse_runlist(path), path


def extract_run_number(filename):
    """Extract integer run number from filenames like Run00118175.i3.zst"""
    m = re.match(r"Run(\d+)", filename)
    if m:
        return int(m.group(1))
    return None


def hese_livetime(hese_dir, runinfo):
    """Return (n_runs, livetime_s) for i3 files in hese_dir looked up in runinfo."""
    total = 0.0
    n = 0
    missing = []
    for fname in sorted(os.listdir(hese_dir)):
        if ".i3" not in fname:
            continue
        run = extract_run_number(fname)
        if run is None:
            continue
        n += 1
        if run in runinfo:
            total += runinfo[run]
        else:
            missing.append(run)
    return n, total, missing


def main():
    col = 20
    header = (
        f"{'Dataset':<15}  {'Runs':>5}"
        f"  {'HESE (s)':>{col}}  {'GRL (s)':>{col}}"
        f"  {'HESE versioned (s)':>{col}}  {'GRL versioned (s)':>{col}}"
    )
    sep = "-" * len(header)
    print(header)
    print(sep)

    total_hese = total_grl = total_hese_v = total_grl_v = 0.0

    for ds_year in DATASET_YEARS:
        hese_dir = os.path.join(HESE_BASE, ds_year)
        if not os.path.isdir(hese_dir):
            print(f"WARNING: directory not found: {hese_dir}")
            continue

        runinfo, path = load_runlists(ds_year)
        if runinfo is None:
            print(f"WARNING: runlist not found: {path}")
            runinfo = {}

        runinfo_v, path_v = load_runlists(ds_year, versioned=True)
        if runinfo_v is None:
            runinfo_v = {}

        grl_lt = sum(runinfo.values())
        grl_lt_v = sum(runinfo_v.values())

        n_runs, hese_lt, missing = hese_livetime(hese_dir, runinfo)
        _, hese_lt_v, _ = hese_livetime(hese_dir, runinfo_v)

        if missing:
            print(f"WARNING: {ds_year} - {len(missing)} runs not in runlist: {missing[:5]}{'...' if len(missing) > 5 else ''}")

        total_hese += hese_lt
        total_grl += grl_lt
        total_hese_v += hese_lt_v
        total_grl_v += grl_lt_v

        hese_v_str = f"{hese_lt_v:>{col}.2f}" if runinfo_v else f"{'N/A':>{col}}"
        grl_v_str  = f"{grl_lt_v:>{col}.2f}"  if runinfo_v else f"{'N/A':>{col}}"

        print(
            f"{ds_year:<15}  {n_runs:>5}"
            f"  {hese_lt:>{col}.2f}  {grl_lt:>{col}.2f}"
            f"  {hese_v_str}  {grl_v_str}"
        )

    # 2022: GRL only, no HESE files
    def load_2022(versioned=False):
        suffix = "_Versioned" if versioned else ""
        path = os.path.join(RUNINFO_BASE, "2022", "filtered", "level2", f"IC86_2022_GoodRunInfo{suffix}.txt")
        if not os.path.exists(path):
            print(f"WARNING: not found: {path}")
            return 0.0
        return sum(parse_runlist(path).values())

    lt_2022   = load_2022(versioned=False)
    lt_2022_v = load_2022(versioned=True)
    total_grl   += lt_2022
    total_grl_v += lt_2022_v

    print(
        f"{'IC86_2022':<15}  {'N/A':>5}"
        f"  {'N/A':>{col}}  {lt_2022:>{col}.2f}"
        f"  {'N/A':>{col}}  {lt_2022_v:>{col}.2f}"
    )

    print(sep)
    print(
        f"{'TOTAL':<15}  {'':>5}"
        f"  {total_hese:>{col}.2f}  {total_grl:>{col}.2f}"
        f"  {total_hese_v:>{col}.2f}  {total_grl_v:>{col}.2f}"
    )


if __name__ == "__main__":
    main()
