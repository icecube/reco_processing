import numpy as np

###
### FTP v3
###

plots_spice = {

"HESETaupedeFit_deltaLength_trueAzimuth" : 
{ "reco_key_y" : "HESETaupedeFit", "reco_var_key_y" : "length",
  "true_key_y" : "cc",             "true_var_key_y" : "length",
  "key_x" : "cc",                  "variable_key_x" : "azimuth",
  "bins" : np.linspace(0,6.28318530718,20), "xscale" : "linear", "ylim" : [-5,60], "normalize" : False,
  "xlabel" : r"Azimuth [rad]",  "ylabel" : r"$L_{\rm reco} - L_{\rm true}$ [m]", 
  "name" : "HESETaupedeFit_deltaLength_trueAzimuth"  },

"HESETaupedeFit_deltaLength_trueAzimuth_zoom" : 
{ "reco_key_y" : "HESETaupedeFit", "reco_var_key_y" : "length",
  "true_key_y" : "cc",             "true_var_key_y" : "length",
  "key_x" : "cc",                  "variable_key_x" : "azimuth",
  "bins" : np.linspace(0,6.28318530718,20), "xscale" : "linear", "ylim" : [-5,10], "normalize" : False,
  "xlabel" : r"Azimuth [rad]",  "ylabel" : r"$L_{\rm reco} - L_{\rm true}$ [m]", 
  "name" : "HESETaupedeFit_deltaLength_trueAzimuth_zoom"  },

"HESETaupedeFit_deltaLength_trueAzimuth_normalised" : 
{ "reco_key_y" : "HESETaupedeFit", "reco_var_key_y" : "length",
  "true_key_y" : "cc",             "true_var_key_y" : "length",
  "key_x" : "cc",                  "variable_key_x" : "azimuth",
  "bins" : np.linspace(0,6.28318530718,20), "xscale" : "linear", "ylim" : [-1,6], "normalize" : True,
  "xlabel" : r"Azimuth [rad]",  "ylabel" : r"($L_{\rm reco} - L_{\rm true})/L_{\rm true}$", 
  "name" : "HESETaupedeFit_deltaLength_trueAzimuth_normalised"  },

}



plots_ftp = {

"TaupedeFit_iMIGRAD_PPB0_deltaLength_trueAzimuth" : 
{ "reco_key_y" : "TaupedeFit_iMIGRAD_PPB0", "reco_var_key_y" : "length",
  "true_key_y" : "cc",             "true_var_key_y" : "length",
  "key_x" : "cc",                  "variable_key_x" : "azimuth",
  "bins" : np.linspace(0,6.28318530718,20), "xscale" : "linear", "ylim" : [-5,20], "normalize" : False,
  "xlabel" : r"Azimuth [rad]",  "ylabel" : r"$L_{\rm reco} - L_{\rm true}$ [m]", 
  "name" : "TaupedeFit_iMIGRAD_PPB0_deltaLength_trueAzimuth"  },

"TaupedeFit_iMIGRAD_PPB0_deltaLength_trueAzimuth_zoom" : 
{ "reco_key_y" : "TaupedeFit_iMIGRAD_PPB0", "reco_var_key_y" : "length",
  "true_key_y" : "cc",             "true_var_key_y" : "length",
  "key_x" : "cc",                  "variable_key_x" : "azimuth",
  "bins" : np.linspace(0,6.28318530718,20), "xscale" : "linear", "ylim" : [-5,10], "normalize" : False,
  "xlabel" : r"Azimuth [rad]",  "ylabel" : r"$L_{\rm reco} - L_{\rm true}$ [m]", 
  "name" : "TaupedeFit_iMIGRAD_PPB0_deltaLength_trueAzimuth_zoom"  },

"TaupedeFit_iMIGRAD_PPB0_deltaLength_trueAzimuth_normalised" : 
{ "reco_key_y" : "TaupedeFit_iMIGRAD_PPB0", "reco_var_key_y" : "length",
  "true_key_y" : "cc",             "true_var_key_y" : "length",
  "key_x" : "cc",                  "variable_key_x" : "azimuth",
  "bins" : np.linspace(0,6.28318530718,20), "xscale" : "linear", "ylim" : [-2,10], "normalize" : True,
  "xlabel" : r"Azimuth [rad]",  "ylabel" : r"($L_{\rm reco} - L_{\rm true})/L_{\rm true}$", 
  "name" : "TaupedeFit_iMIGRAD_PPB0_deltaLength_trueAzimuth_normalised"  },

}
