import numpy as np

###
### FTP v3
###

plots_taupede = {

"HESETaupedeFit_deltaLength_trueLength" : 
{ "reco_key_y" : "HESETaupedeFit", "reco_var_key_y" : "length",
  "true_key_y" : "cc",             "true_var_key_y" : "length",
  "key_x" : "cc",                  "variable_key_x" : "length",
  "bins" : np.linspace(0,50,20), "xscale" : "linear", "ylim" : [-5,10], "normalize" : False,
  "xlabel" : r"$L_{\rm true}$ [m]",  "ylabel" : r"$L_{\rm reco} - L_{\rm true}$ [m]", 
  "name" : "HESETaupedeFit_deltaLength_trueLength"  },

"HESETaupedeFit_deltaLength_trueLength_normalised" : 
{ "reco_key_y" : "HESETaupedeFit", "reco_var_key_y" : "length",
  "true_key_y" : "cc",             "true_var_key_y" : "length",
  "key_x" : "cc",                  "variable_key_x" : "length",
  "bins" : np.linspace(0,50,20), "xscale" : "linear", "ylim" : [-0.2,0.6], "normalize" : True,
  "xlabel" : r"$L_{\rm true}$ [m]",  "ylabel" : r"($L_{\rm reco} - L_{\rm true})/L_{\rm true}$", 
  "name" : "HESETaupedeFit_deltaLength_trueLength_normalised"  },

"HESETaupedeFit_deltaEnergy_trueEnergy" : 
{ "reco_key_y" : "HESETaupedeFit", "reco_var_key_y" : "energy",
  "true_key_y" : "cc",                      "true_var_key_y" : "energy",
  "key_x" : "cc",                           "variable_key_x" : "energy",
  "bins" : np.geomspace(1e4,1e8,20), "xscale" : "log", "ylim" : [-0.15,0.20], "normalize" : True,
  "xlabel" : r"$E_{\rm deposited}$ [GeV]",  "ylabel" : r"$(E_{\rm reco} - E_{\rm true})/E_{\rm true}$", 
  "name" : "HESETaupedeFit_deltaEnergy_trueEnergy"  },

"HESETaupedeFit_deltaDir_trueEnergy" : 
{ "reco_key_y" : "HESETaupedeFit", "reco_var_key_y" : "direction",
  "true_key_y" : "cc",                      "true_var_key_y" : "direction",
  "key_x" : "cc",                           "variable_key_x" : "energy",
  "bins" : np.geomspace(1e4,1e8,20), "xscale" : "log", "ylim" : [0,15], "normalize" : False,
  "xlabel" : r"$E_{\rm deposited}$ [GeV]",  "ylabel" : r"$\Delta \psi$ [degrees]", 
  "name" : "HESETaupedeFit_deltaDir_trueEnergy"  },

"HESETaupedeFit_deltaDir_trueLength" :
{ "reco_key_y" : "HESETaupedeFit", "reco_var_key_y" : "direction",
  "true_key_y" : "cc",                      "true_var_key_y" : "direction",
  "key_x" : "cc",                           "variable_key_x" : "length",
  "bins" : np.linspace(0,50,20), "xscale" : "linear", "ylim" : [0,20], "normalize" : False,
  "xlabel" : r"$L_{\rm true}$ [m]",  "ylabel" : r"$\Delta \psi$ [degrees]", 
  "name" : "HESETaupedeFit_deltaDir_trueLength"  },

"HESETaupedeFit_deltaEasym_trueLength" :
{ "reco_key_y" : "HESETaupedeFit", "reco_var_key_y" : "easym",
  "true_key_y" : "cc_easymm",               "true_var_key_y" : "value",
  "key_x" : "cc",                           "variable_key_x" : "length",
  "bins" : np.linspace(0,50,20), "xscale" : "linear", "ylim" : [-0.25,1], "normalize" : False,
  "xlabel" : r"$L_{\rm true}$ [m]",  "ylabel" : r"$\Delta E_{\rm A}$", 
  "name" : "HESETaupedeFit_deltaEasym_trueLength"  },
}

plots_monopod = {

"HESEMonopodFit_deltaEnergy_trueEnergy" : 
{ "reco_key_y" : "HESEMonopodFit", "reco_var_key_y" : "energy",
  "true_key_y" : "cc",                      "true_var_key_y" : "energy",
  "key_x" : "cc",                           "variable_key_x" : "energy",
  "bins" : np.geomspace(1e4,1e8,20), "xscale" : "log", "ylim" : [-0.05,0.2], "normalize" : True,
  "xlabel" : r"$E_{\rm deposited}$ [GeV]",  "ylabel" : r"$(E_{\rm reco} - E_{\rm true})/E_{\rm true}$", 
  "name" : "HESEMonopodFit_deltaEnergy_trueEnergy"  },

"HESEMonopodFit_deltaDir_trueEnergy" : 
{ "reco_key_y" : "HESEMonopodFit", "reco_var_key_y" : "direction",
  "true_key_y" : "TrueAzimuth",                      "true_var_key_y" : "direction",
  "key_x" : "TrueETot",                           "variable_key_x" : "value",
  "bins" : np.geomspace(1e4,1e8,20), "xscale" : "log", "ylim" : [0,25], "normalize" : False,
  "xlabel" : r"$E_{\rm deposited}$ [GeV]",  "ylabel" : r"$\Delta \psi$ [degrees]", 
  "name" : "HESEMonopodFit_deltaDir_trueEnergy"  },

}
