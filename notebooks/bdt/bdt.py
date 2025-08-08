
import joblib
import numpy as np

model1 = joblib.load( "/data/user/zchen/bdt_training/models/ftp/ftp_13features/bdt1_model.pkl" )
model2 = joblib.load( "/data/user/zchen/bdt_training/models/ftp/ftp_13features/bdt2_model.pkl" )

def Append_BDT(weighter):

    var_names = [
        ['TauMonoDiff_rlogl','value'],
        ['Taupede_Asymmetry','value'],
        ['Taupede_Distance','value'],
        ['Taupede1_Particles_energy','value'],
        ['Taupede2_Particles_energy','value'],
        ['cscdSBU_MonopodFit4_noDC_zenith','value'],
        ['MonopodFit_iMIGRAD_PPB0_Delay_ice','value'],
        ['CVStatistics_q_max_doms','value'],
        ['cscdSBU_VertexRecoDist_CscdLLh','value'],
        # ['MonopodFit_iMIGRAD_PPB0_energy','value'],
        ['MonopodFit_iMIGRAD_PPB0','energy'],
        ['cscdSBU_Qtot_HLC_log','value'],
        ['Taupede_ftpFitParams_rlogl','value'],
        ['cscdSBU_MonopodFit4_noDCFitParams_rlogl','value'],
    ]

    # Build feature array: shape (num_events, 13)
    variables = [weighter.get_column(var[0], var[1]) for var in var_names]    
    features = np.column_stack(variables)

    # Predict BDT scores
    bdt_score1 = model1.predict_proba(features)[:, 1]  # assuming binary classifier
    bdt_score2 = model2.predict_proba(features)[:, 1]  # assuming second model

    return bdt_score1, bdt_score2
