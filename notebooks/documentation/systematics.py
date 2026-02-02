
systematics = {}

systematics["half_range"] = [
    {"syst_param"  : "CrystalDensityParameterScaling", "syst_upper" : 0.9, "syst_lower" : 1.1},
    {"syst_param"  : "DOMEfficiency", "syst_upper" : 0.95, "syst_lower" : 1.05},
    {"syst_param"  : "Absorption", "syst_upper" : 0.95, "syst_lower" : 1.05},
    {"syst_param"  : "MieScattering", "syst_upper" : 0.95, "syst_lower" : 1.05},
    {"syst_param"  : "HoleIceForward_Unified_p0", "syst_upper" : 0.075, "syst_lower" : 0.425},
    {"syst_param"  : "HoleIceForward_Unified_p1", "syst_upper" : -0.09, "syst_lower" : -0.03},
]