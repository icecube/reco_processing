
import joblib
import numpy as np

model1 = joblib.load( "/data/user/zchen/bdt_training/models/ftp/ftp_13features/bdt1_model.pkl" )
model2 = joblib.load( "/data/user/zchen/bdt_training/models/ftp/ftp_13features/bdt2_model.pkl" )

def Append_BDT(file):

    var_names = [
        'TauMonoDiff_rlogl',
        'Taupede_Asymmetry',
        'Taupede_Distance',
        'Taupede1_Particles_energy',
        'Taupede2_Particles_energy',
        'cscdSBU_MonopodFit4_noDC_zenith',
        'MonopodFit_iMIGRAD_PPB0_Delay_ice',
        'CVStatistics_q_max_doms',
        'cscdSBU_VertexRecoDist_CscdLLh',
        'MonopodFit_iMIGRAD_PPB0_energy',
        'cscdSBU_Qtot_HLC_log',
        'Taupede_ftpFitParams_rlogl',
        'cscdSBU_MonopodFit4_noDCFitParams_rlogl',
    ]

    # Build feature array: shape (num_events, 13)
    features = np.column_stack([file['variables'][var] for var in var_names])

    # Predict BDT scores
    file['variables']['BDT_score1'] = model1.predict_proba(features)[:, 1]  # assuming binary classifier
    file['variables']['BDT_score2'] = model2.predict_proba(features)[:, 1]  # assuming second model

    return file
