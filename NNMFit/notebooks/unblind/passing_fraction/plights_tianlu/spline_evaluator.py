"""
Spline evaluator for depth-dependent HESE passing fractions.

Adapted from /data/user/nlad/PassingFractions/spline_evaluator.py.

Key differences:
  - No plight/E_thresh dimension: one spline per neutrino kind.
  - Splines live in plights_tianlu/splines/hese_plight_11dep_21cth_51ene/.
  - evaluate() accepts arrays directly (no pid-masking loop — caller owns that).
  - evaluate_vectorized() for fast per-event evaluation with bounds handling.
"""

import os
import pickle
import logging

import numpy as np
from photospline import SplineTable

logger = logging.getLogger(__name__)

SPLINES_DIR = (
    "/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/"
    "unblind/passing_fraction/plights_tianlu/splines/hese_plight_11dep_21cth_51ene"
)

ALL_KINDS = [
    "conv nu_mu", "conv nu_mubar",
    "conv nu_e",  "conv nu_ebar",
    "pr nu_mu",   "pr nu_mubar",
    "pr nu_e",    "pr nu_ebar",
]

_PID_TO_FLAVORTYPE = {
    12: "nu_e", -12: "nu_ebar",
    14: "nu_mu", -14: "nu_mubar",
}


class Spline_Evaluator:

    def __init__(self, splines_dir=SPLINES_DIR):
        self.splines_dir = splines_dir

        with open(os.path.join(splines_dir, "info.pickle"), "rb") as fh:
            self.grid_info = pickle.load(fh)

        self.min_cos_theta = float(self.grid_info["cos_theta_grid"].min())
        self.max_cos_theta = float(self.grid_info["cos_theta_grid"].max())
        self.min_log_e = float(np.log10(self.grid_info["energy_grid"].min()))
        self.max_log_e = float(np.log10(self.grid_info["energy_grid"].max()))

        self.splines = {}
        for kind in ALL_KINDS:
            fname = f"pf_spline_{kind.replace(' ', '_')}.fits"
            path = os.path.join(splines_dir, fname)
            self.splines[kind] = SplineTable(path)
            logger.debug(f"Loaded spline: {fname}")

        logger.info(f"Loaded {len(self.splines)} splines from {splines_dir}")

    @staticmethod
    def flavortype_to_pid(flavortype):
        return {"nu_e": 12, "nu_ebar": -12, "nu_mu": 14, "nu_mubar": -14}[flavortype]

    def get_flavortype_mask(self, flavortype, pid_array):
        return pid_array == self.flavortype_to_pid(flavortype)

    def get_min_cos_theta(self):
        return self.min_cos_theta

    @staticmethod
    def get_PF_default():
        """log10(PF) = 0 → PF = 1 for upgoing / below spline support."""
        return 0.0

    def evaluate(self, kind, pid, depth, zenith, energy):
        """
        Evaluate the passing-fraction spline.

        Parameters
        ----------
        kind    : str  e.g. "conv nu_mu"
        pid     : np.ndarray  PDG particle IDs
        depth   : np.ndarray  impact depths [m]
        zenith  : np.ndarray  true neutrino zenith angles [rad]
        energy  : np.ndarray  true neutrino energies [GeV]

        Returns
        -------
        np.ndarray of log10(passing_fraction), same length as pid.
        """
        comp, fltype = kind.split(" ")
        if comp not in ("conv", "pr"):
            raise NotImplementedError(f"Unknown component: {comp}")

        pf = np.zeros(len(depth), dtype=float)

        mask_type = self.get_flavortype_mask(fltype, pid)
        cos_theta = np.cos(zenith)

        # events below spline cos_theta support → PF = 1
        mask_upgoing = np.logical_and(mask_type,
                                      cos_theta < self.min_cos_theta)
        pf[mask_upgoing] = self.get_PF_default()

        mask_eval = np.logical_and(mask_type,
                                   cos_theta >= self.min_cos_theta)

        spline = self.splines[kind]
        for idx in np.where(mask_eval)[0]:
            d   = float(depth[idx])
            ct  = float(cos_theta[idx])
            lge = float(np.log10(energy[idx]))
            if np.isnan(d):
                pf[idx] = self.get_PF_default()
            else:
                pf[idx] = spline.evaluate_simple([d, ct, lge])

        return pf

    def evaluate_simple(self, kind, depth_m, cos_theta, energy_gev):
        """
        Scalar evaluation. Returns log10(PF).

        Parameters
        ----------
        kind       : str
        depth_m    : float  [m]
        cos_theta  : float
        energy_gev : float  [GeV]
        """
        if cos_theta < self.min_cos_theta:
            return self.get_PF_default()
        return float(self.splines[kind].evaluate_simple(
            [depth_m, cos_theta, np.log10(energy_gev)]
        ))

    def evaluate_all(self, pid, depth, zenith, energy, fluxtype="conv"):
        """
        Evaluate for all neutrino flavors and sum log10(PF) contributions.

        Parameters
        ----------
        pid      : np.ndarray  PDG particle IDs
        depth    : np.ndarray  impact depths [m]
        zenith   : np.ndarray  true neutrino zenith angles [rad]
        energy   : np.ndarray  true neutrino energies [GeV]
        fluxtype : str  "conv" or "pr"

        Returns
        -------
        np.ndarray of log10(passing_fraction)
        """
        pf_all = np.zeros(len(depth), dtype=float)
        for flavortype in ("nu_e", "nu_ebar", "nu_mu", "nu_mubar"):
            pf_all += self.evaluate(
                f"{fluxtype} {flavortype}", pid, depth, zenith, energy
            )
        logger.info("Tau passing fractions not available.")
        return pf_all
