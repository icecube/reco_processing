from icecube import icetray,dataclasses
import joblib

@icetray.traysegment
def apply_bdt(tray, name):

    model1 = joblib.load( "/data/user/zchen/bdt_training/models/ftp/ftp_13features/bdt1_model.pkl" )
    model2 = joblib.load( "/data/user/zchen/bdt_training/models/ftp/ftp_13features/bdt2_model.pkl" )

    def append_bdt(frame):

        # taken from /data/user/zchen/bdt_training/models/ftp/ftp_13features/features_ftp_13features.txt
        features = [ frame['TauMonoDiff_rlogl'].value, 
                     frame['Taupede_Asymmetry'].value,
                     frame["Taupede_Distance"].value,
                     frame["Taupede1_Particles_energy"].value,
                     frame["Taupede2_Particles_energy"].value,
                     frame["cscdSBU_MonopodFit4_noDC_zenith"].value,
                     frame["MonopodFit_iMIGRAD_PPB0_Delay_ice"].value,
                     frame["CVStatistics_q_max_doms"].value,
                     frame["cscdSBU_VertexRecoDist_CscdLLh"].value,
                     frame["MonopodFit_iMIGRAD_PPB0"].energy,
                     frame['cscdSBU_Qtot_HLC_log'].value,
                     frame["Taupede_ftpFitParams_rlogl"].value,
                     frame["cscdSBU_MonopodFit4_noDCFitParams_rlogl"].value ]

        print("features", features)

        bdt1_score = model1.predict_proba([features])
        bdt2_score = model2.predict_proba([features])

        print("bdt1_score", bdt1_score)
        print("bdt2_score", bdt2_score)

    tray.Add(append_bdt)