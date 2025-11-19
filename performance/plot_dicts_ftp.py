import numpy as np

###
### FTP v3
###

plots_taupede = {

"TaupedeFit_iMIGRAD_PPB0_deltaLength_trueLength" :
{ "reco_key_y" : "TaupedeFit_iMIGRAD_PPB0", "reco_var_key_y" : "length",
  "true_key_y" : "cc",                      "true_var_key_y" : "length",
  "key_x" : "cc",                           "variable_key_x" : "length",
  "bins" : np.linspace(0,50,20), "xscale" : "linear", "ylim" : [-5,10], "normalize" : False,
  "xlabel" : r"$L_{\rm true}$ [m]",  "ylabel" : r"$L_{\rm reco} - L_{\rm true}$ [m]", 
  "name" : "TaupedeFit_iMIGRAD_PPB0_deltaLength_trueLength"  },

"TaupedeFit_iMIGRAD_PPB0_deltaLength_trueLength_normalised" :
{ "reco_key_y" : "TaupedeFit_iMIGRAD_PPB0", "reco_var_key_y" : "length",
  "true_key_y" : "cc",                      "true_var_key_y" : "length",
  "key_x" : "cc",                           "variable_key_x" : "length",
  "bins" : np.linspace(0,50,20), "xscale" : "linear", "ylim" : [-0.5,0.5], "normalize" : True,
  "xlabel" : r"$L_{\rm true}$ [m]",  "ylabel" : r"$(L_{\rm reco} - L_{\rm true})/L_{\rm true}$ [m]", 
  "name" : "TaupedeFit_iMIGRAD_PPB0_deltaLength_trueLength_normalised"  },

"TaupedeFit_iMIGRAD_PPB0_deltaEnergy_trueEnergy" :
{ "reco_key_y" : "TaupedeFit_iMIGRAD_PPB0", "reco_var_key_y" : "energy",
  "true_key_y" : "cc",                      "true_var_key_y" : "energy",
  "key_x" : "cc",                           "variable_key_x" : "energy",
  "bins" : np.geomspace(1e4,1e8,20), "xscale" : "log", "ylim" : [-0.15,0.15], "normalize" : True,
  "xlabel" : r"$E_{\rm deposited}$ [GeV]",  "ylabel" : r"$(E_{\rm reco} - E_{\rm true})/E_{\rm true}$", 
  "name" : "TaupedeFit_iMIGRAD_PPB0_deltaEnergy_trueEnergy"  },

"TaupedeFit_iMIGRAD_PPB0_deltaDir_trueEnergy" :
{ "reco_key_y" : "TaupedeFit_iMIGRAD_PPB0", "reco_var_key_y" : "direction",
  "true_key_y" : "cc",                      "true_var_key_y" : "direction",
  "key_x" : "cc",                           "variable_key_x" : "energy",
  "bins" : np.geomspace(1e4,1e8,20), "xscale" : "log", "ylim" : [0,10], "normalize" : False,
  "xlabel" : r"$E_{\rm deposited}$ [GeV]",  "ylabel" : r"$\Delta \psi$ [degrees]", 
  "name" : "TaupedeFit_iMIGRAD_PPB0_deltaDir_trueEnergy"  },

"TaupedeFit_iMIGRAD_PPB0_deltaDir_trueLength" :
{ "reco_key_y" : "TaupedeFit_iMIGRAD_PPB0", "reco_var_key_y" : "direction",
  "true_key_y" : "cc",                      "true_var_key_y" : "direction",
  "key_x" : "cc",                           "variable_key_x" : "length",
  "bins" : np.linspace(0,50,20), "xscale" : "linear", "ylim" : [0,10], "normalize" : False,
  "xlabel" : r"$L_{\rm true}$ [m]",  "ylabel" : r"$\Delta \psi$ [degrees]", 
  "name" : "TaupedeFit_iMIGRAD_PPB0_deltaDir_trueLength"  },

"TaupedeFit_iMIGRAD_PPB0_deltaEasym_trueLength" :
{ "reco_key_y" : "TaupedeFit_iMIGRAD_PPB0", "reco_var_key_y" : "easym",
  "true_key_y" : "cc_easymm",               "true_var_key_y" : "value",
  "key_x" : "cc",                           "variable_key_x" : "length",
  "bins" : np.linspace(0,50,20), "xscale" : "linear", "ylim" : [-1,1], "normalize" : False,
  "xlabel" : r"$L_{\rm true}$ [m]",  "ylabel" : r"$\Delta E_{\rm A}$", 
  "name" : "TaupedeFit_iMIGRAD_PPB0_deltaEasym_trueLength"  },

}

plots_evtgen = {

# thijs
"EventGeneratorDC_Thijs_deltaLength_trueLength" :
{ "reco_key_y" : "EventGeneratorDC_Thijs", "reco_var_key_y" : "cascade_cascade_00001_distance",
  "true_key_y" : "cc",                      "true_var_key_y" : "length",
  "key_x" : "cc",                           "variable_key_x" : "length",
  "bins" : np.linspace(0,50,20), "xscale" : "linear", "ylim" : [-5,10], "normalize" : False,
  "xlabel" : r"$L_{\rm true}$ [m]",  "ylabel" : r"$L_{\rm reco} - L_{\rm true}$ [m]", 
  "name" : "EventGeneratorDC_Thijs_deltaLength_trueLength"  },

"EventGeneratorDC_Thijs_deltaLength_trueLength_normalised" :
{ "reco_key_y" : "EventGeneratorDC_Thijs", "reco_var_key_y" : "cascade_cascade_00001_distance",
  "true_key_y" : "cc",                      "true_var_key_y" : "length",
  "key_x" : "cc",                           "variable_key_x" : "length",
  "bins" : np.linspace(0,50,20), "xscale" : "linear", "ylim" : [-0.5,0.5], "normalize" : True,
  "xlabel" : r"$L_{\rm true}$ [m]",  "ylabel" : r"$(L_{\rm reco} - L_{\rm true})/L_{\rm true}$", 
  "name" : "EventGeneratorDC_Thijs_deltaLength_trueLength_normalised"  },

"EventGeneratorDC_Thijs_deltaEasym_trueLength" :
{ "reco_key_y" : "EventGeneratorDC_Thijs", "reco_var_key_y" : "easym",
  "true_key_y" : "cc_easymm",               "true_var_key_y" : "value",
  "key_x" : "cc",                           "variable_key_x" : "length",
  "bins" : np.linspace(0,50,20), "xscale" : "linear", "ylim" : [-1,1], "normalize" : False,
  "xlabel" : r"$L_{\rm true}$ [m]",  "ylabel" : r"$\Delta E_{\rm A}$", 
  "name" : "EventGeneratorDC_Thijs_deltaEasym_trueLength"  },

# max
"EventGeneratorDC_Max_deltaLength_trueLength" :
{ "reco_key_y" : "EventGeneratorDC_Max", "reco_var_key_y" : "cascade_cascade_00001_distance",
  "true_key_y" : "cc",                      "true_var_key_y" : "length",
  "key_x" : "cc",                           "variable_key_x" : "length",
  "bins" : np.linspace(0,100,20), "xscale" : "linear", "ylim" : [-5,10], "normalize" : False,
  "xlabel" : r"$L_{\rm true}$ [m]",  "ylabel" : r"$L_{\rm reco} - L_{\rm true}$ [m]", 
  "name" : "EventGeneratorDC_Max_deltaLength_trueLength"  },

"EventGeneratorDC_Max_deltaLength_trueLength_normalised" :
{ "reco_key_y" : "EventGeneratorDC_Max", "reco_var_key_y" : "cascade_cascade_00001_distance",
  "true_key_y" : "cc",                      "true_var_key_y" : "length",
  "key_x" : "cc",                           "variable_key_x" : "length",
  "bins" : np.linspace(0,100,20), "xscale" : "linear", "ylim" : [-0.5,0.5], "normalize" : True,
  "xlabel" : r"$L_{\rm true}$ [m]",  "ylabel" : r"$(L_{\rm reco} - L_{\rm true})/L_{\rm true}$", 
  "name" : "EventGeneratorDC_Max_deltaLength_trueLength_normalised"  },

"EventGeneratorDC_Max_deltaEasym_trueLength" :
{ "reco_key_y" : "EventGeneratorDC_Max", "reco_var_key_y" : "easym",
  "true_key_y" : "cc_easymm",               "true_var_key_y" : "value",
  "key_x" : "cc",                           "variable_key_x" : "length",
  "bins" : np.linspace(0,50,20), "xscale" : "linear", "ylim" : [-1,1], "normalize" : False,
  "xlabel" : r"$L_{\rm true}$ [m]",  "ylabel" : r"$\Delta E_{\rm A}$", 
  "name" : "EventGeneratorDC_Max_deltaEasym_trueLength"  },

}

plots_monopod = {

"MonopodFit_iMIGRAD_PPB0_deltaEnergy_trueEnergy" : 
{ "reco_key_y" : "MonopodFit_iMIGRAD_PPB0", "reco_var_key_y" : "energy",
  "true_key_y" : "cc",                      "true_var_key_y" : "energy",
  "key_x" : "cc",                           "variable_key_x" : "energy",
  "bins" : np.geomspace(1e4,1e8,20), "xscale" : "log", "ylim" : [-0.05,0.1], "normalize" : True,
  "xlabel" : r"$E_{\rm deposited}$ [GeV]",  "ylabel" : r"$(E_{\rm reco} - E_{\rm true})/E_{\rm true}$", 
  "name" : "MonopodFit_iMIGRAD_PPB0_deltaEnergy_trueEnergy"  },

"MonopodFit_iMIGRAD_PPB0_deltaDir_trueEnergy" : 
{ "reco_key_y" : "MonopodFit_iMIGRAD_PPB0", "reco_var_key_y" : "direction",
  "true_key_y" : "cc",                      "true_var_key_y" : "direction",
  "key_x" : "cc",                           "variable_key_x" : "energy",
  "bins" : np.geomspace(1e4,1e8,20), "xscale" : "log", "ylim" : [0,15], "normalize" : False,
  "xlabel" : r"$E_{\rm deposited}$ [GeV]",  "ylabel" : r"$\Delta \psi$ [degrees]", 
  "name" : "MonopodFit_iMIGRAD_PPB0_deltaDir_trueEnergy"  },

}