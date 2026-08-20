#!/usr/bin/env python3
"""
Test that Spline_Evaluator.evaluate_all equals the sum of per-flavor
evaluate calls.

evaluate_all loops over ["nu_e","nu_ebar","nu_mu","nu_mubar"] and adds each
evaluate result. Because evaluate masks by PID, only the matching flavor
contributes; the rest are zero. So for any array of events the two approaches
must be numerically identical.

Run with:
  /mnt/ceph1-npx/user/tvaneede/software/py_venvs/py3-v4.4.2_reco-v1.2.3_icetray-v1.16.0/bin/python \
      test_spline_evaluate_vs_evaluate_all.py
"""

import sys
import numpy as np

sys.path.insert(0, "/data/user/nlad/PassingFractions/")
from spline_evaluator import Spline_Evaluator

hdl = Spline_Evaluator()

FLAVORS   = ["nu_e", "nu_ebar", "nu_mu", "nu_mubar"]
PID_MAP   = {"nu_e": 12, "nu_ebar": -12, "nu_mu": 14, "nu_mubar": -14}
FLUX_TYPE = "conv"

# ── Test events ───────────────────────────────────────────────────────────────
# One representative event per flavor at a mid-range (depth, zenith, energy).
# Zenith chosen so cos(zenith) is comfortably inside the spline grid (0.05–1).
N = len(FLAVORS)
depth  = np.full(N, 1950.0)              # m
zenith = np.arccos(np.array([0.5, 0.5, 0.7, 0.7]))  # radians
energy = np.array([1e3, 1e4, 1e3, 1e4])  # GeV
pid    = np.array([PID_MAP[f] for f in FLAVORS])

print("Test events:")
print(f"  pid    = {pid}")
print(f"  depth  = {depth} m")
print(f"  zenith = {np.degrees(zenith).round(1)} deg  (cos = {np.cos(zenith).round(3)})")
print(f"  energy = {energy} GeV")
print()

# ── evaluate_all ──────────────────────────────────────────────────────────────
result_all = hdl.evaluate_all(pid, depth, zenith, energy, fluxtype=FLUX_TYPE)

# ── sum of per-flavor evaluate calls ─────────────────────────────────────────
result_sum = np.zeros(N)
for flavor in FLAVORS:
    kind = f"{FLUX_TYPE} {flavor}"
    contrib = hdl.evaluate(kind, pid, depth, zenith, energy)
    print(f"  evaluate('{kind}') = {contrib}")
    result_sum += contrib

print()
print(f"evaluate_all result : {result_all}")
print(f"sum of evaluate     : {result_sum}")
print()

# ── Check ─────────────────────────────────────────────────────────────────────
diff = np.abs(result_all - result_sum)
tol  = 1e-12
passed = np.all(diff < tol)

print(f"Max absolute difference: {diff.max():.2e}  (tolerance {tol:.0e})")
if passed:
    print("PASS: evaluate_all == sum of evaluate for all events.")
else:
    print("FAIL: results differ!")
    for k in range(N):
        print(f"  event {k} (pid={pid[k]}, flavor={FLAVORS[k]}): "
              f"all={result_all[k]:.8f}  sum={result_sum[k]:.8f}  "
              f"diff={diff[k]:.2e}")
