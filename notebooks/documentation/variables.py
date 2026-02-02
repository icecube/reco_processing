import numpy as np
from copy import deepcopy

nbins = 12

variables = {}

variables["level6_cascade"] = {
    # true parameters
    "PrimaryNeutrinoEnergy" : {"base_var_key1" : "I3MCWeightDict", "base_var_key2" : "PrimaryNeutrinoEnergy", "variable_name" : "PrimaryNeutrinoEnergy [GeV]","bins" : np.geomspace(1e2, 1e8, nbins), "xscale" : "log", "yscale" : "log"},
    "PrimaryNeutrinoAzimuth" : {"base_var_key1" : "I3MCWeightDict", "base_var_key2" : "PrimaryNeutrinoAzimuth", "variable_name" : "PrimaryNeutrinoAzimuth [rad]","bins" : np.linspace(0, 2*np.pi, nbins), "xscale" : "linear", "yscale" : "log"},
    "PrimaryNeutrinoZenith" : {"base_var_key1" : "I3MCWeightDict", "base_var_key2" : "PrimaryNeutrinoZenith", "variable_name" : "PrimaryNeutrinoZenith [rad]","bins" : np.linspace(0, 1*np.pi, nbins), "xscale" : "linear", "yscale" : "log"},

    # cscdSBU_MonopodFit4
    "cscdSBU_MonopodFit4_energy" : {"base_var_key1" : "cscdSBU_MonopodFit4", "base_var_key2" : "energy", "variable_name" : "cscdSBU_MonopodFit4 energy [GeV]","bins" : np.geomspace(1e2, 1e8, nbins), "xscale" : "log", "yscale" : "log"},
    "cscdSBU_MonopodFit4_azimuth" : {"base_var_key1" : "cscdSBU_MonopodFit4", "base_var_key2" : "azimuth", "variable_name" : "cscdSBU_MonopodFit4 azimuth [rad]","bins" : np.linspace(0, 2*np.pi, nbins), "xscale" : "linear", "yscale" : "log"},
    "cscdSBU_MonopodFit4_zenith" : {"base_var_key1" : "cscdSBU_MonopodFit4", "base_var_key2" : "zenith", "variable_name" : "cscdSBU_MonopodFit4 zenith [rad]","bins" : np.linspace(0, 1*np.pi, nbins), "xscale" : "linear", "yscale" : "log"},
}
variables["level6_hybrid"] = deepcopy(variables["level6_cascade"])
variables["level6_muon"] = deepcopy(variables["level6_cascade"])

variables["HESE"] = {
    # true parameters
    "PrimaryNeutrinoEnergy" : {"base_var_key1" : "I3MCWeightDict", "base_var_key2" : "PrimaryNeutrinoEnergy", "variable_name" : "PrimaryNeutrinoEnergy [GeV]","bins" : np.geomspace(1e3, 1e8, nbins - 2), "xscale" : "log", "yscale" : "log"},
    "PrimaryNeutrinoAzimuth" : {"base_var_key1" : "I3MCWeightDict", "base_var_key2" : "PrimaryNeutrinoAzimuth", "variable_name" : "PrimaryNeutrinoAzimuth [rad]","bins" : np.linspace(0, 2*np.pi, nbins), "xscale" : "linear", "yscale" : "log"},
    "PrimaryNeutrinoZenith" : {"base_var_key1" : "I3MCWeightDict", "base_var_key2" : "PrimaryNeutrinoZenith", "variable_name" : "PrimaryNeutrinoZenith [rad]","bins" : np.linspace(0, 1*np.pi, nbins), "xscale" : "linear", "yscale" : "log"},

    # cscdSBU_MonopodFit4
    "MonopodFit_iMIGRAD_PPB0_energy" : {"base_var_key1" : "MonopodFit_iMIGRAD_PPB0", "base_var_key2" : "energy", "variable_name" : "MonopodFit_iMIGRAD_PPB0 energy [GeV]","bins" : np.geomspace(1e3, 1e8, nbins - 2), "xscale" : "log", "yscale" : "log"},
    "MonopodFit_iMIGRAD_PPB0_azimuth" : {"base_var_key1" : "MonopodFit_iMIGRAD_PPB0", "base_var_key2" : "azimuth", "variable_name" : "MonopodFit_iMIGRAD_PPB0 azimuth [rad]","bins" : np.linspace(0, 2*np.pi, nbins), "xscale" : "linear", "yscale" : "log"},
    "MonopodFit_iMIGRAD_PPB0_zenith" : {"base_var_key1" : "MonopodFit_iMIGRAD_PPB0", "base_var_key2" : "zenith", "variable_name" : "MonopodFit_iMIGRAD_PPB0 zenith [rad]","bins" : np.linspace(0, 1*np.pi, nbins), "xscale" : "linear", "yscale" : "log"},

    # taupede
    "TaupedeFit_iMIGRAD_PPB0_energy" : {"base_var_key1" : "TaupedeFit_iMIGRAD_PPB0", "base_var_key2" : "energy", "variable_name" : "TaupedeFit_iMIGRAD_PPB0 energy [GeV]","bins" : np.geomspace(1e3, 1e8, nbins - 2), "xscale" : "log", "yscale" : "log"},
    "TaupedeFit_iMIGRAD_PPB0_azimuth" : {"base_var_key1" : "TaupedeFit_iMIGRAD_PPB0", "base_var_key2" : "azimuth", "variable_name" : "TaupedeFit_iMIGRAD_PPB0 azimuth [rad]","bins" : np.linspace(0, 2*np.pi, nbins), "xscale" : "linear", "yscale" : "log"},
    "TaupedeFit_iMIGRAD_PPB0_zenith" : {"base_var_key1" : "TaupedeFit_iMIGRAD_PPB0", "base_var_key2" : "zenith", "variable_name" : "TaupedeFit_iMIGRAD_PPB0 zenith [rad]","bins" : np.linspace(0, 1*np.pi, nbins), "xscale" : "linear", "yscale" : "log"},
    "TaupedeFit_iMIGRAD_PPB0_length" : {"base_var_key1" : "TaupedeFit_iMIGRAD_PPB0", "base_var_key2" : "length", "variable_name" : "TaupedeFit_iMIGRAD_PPB0 length [m]","bins" : np.linspace(0, 50, nbins), "xscale" : "linear", "yscale" : "log"},
    "TaupedeFit_iMIGRAD_PPB0_loglength" : {"base_var_key1" : "TaupedeFit_iMIGRAD_PPB0", "base_var_key2" : "length", "variable_name" : "TaupedeFit_iMIGRAD_PPB0 length [m]","bins" : np.geomspace(1e-2, 1e2, nbins), "xscale" : "log", "yscale" : "log"},
}
variables["HESE_evtgen"]           = deepcopy(variables["HESE"])
variables["level7_cascade_evtgen"] = deepcopy(variables["HESE"])
