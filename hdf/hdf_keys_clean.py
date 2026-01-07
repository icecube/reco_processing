
hdfkeys = []


hdfkeys += ['cc', 'cc_easymm', 'cc_tauvis'] # true information tianlu
hdfkeys += ['I3MCWeightDict','I3EventHeader'] # general info
hdfkeys += ['LineFit','SPEFit2','l2_online_SplineMPE','OnlineL2_SplineMPE'] # l2 track reco
hdfkeys += ["L3_MonopodFit4_AmptFit"] # l3 cascade
hdfkeys += ["BestTrack"] # l3 track

# tau reco
for key in ["TaupedeFit_iMIGRAD_PPB0", "TaupedeFit_iMIGRAD_PPB0_ibr", "TaupedeFit_iMIGRAD_PPB0_ibr_idc"]: 
    hdfkeys += [f"{key}", f"{key}FitParams", "Particles"]
    hdfkeys += [f"{key}MillipedeFitDepositedEnergy",f"{key}MillipedeFitTruncatedDepositedEnergy",f"{key}MillipedeFitFitParams"]
    hdfkeys += [f"{key}_1", f"{key}_2"]        
    for coord in ["x","y","z"]:
        hdfkeys += [f"{key}_1_{coord}"]
        hdfkeys += [f"{key}_2_{coord}"]

# monopod and SPEFit
for key in ["MonopodFit_iMIGRAD_PPB0", "MonopodFit_iMIGRAD_PPB0_ibr", "MonopodFit_iMIGRAD_PPB0_ibr_idc", "SPEFit16_PPB0"]: 
    hdfkeys += [f"{key}", f"{key}FitParams"]
    hdfkeys += [f"{key}MillipedeFitDepositedEnergy",f"{key}MillipedeFitTruncatedDepositedEnergy",f"{key}MillipedeFitFitParams"]
    if "Monopod" in key:
        for coord in ["x","y","z"]:
            hdfkeys += [f"{key}_{coord}"]

# millipede, best of 3 hypotheses
for key in ["HESEMillipedeFit_PPB0", "HESEMillipedeFit_PPB0_ibr", "HESEMillipedeFit_PPB0_ibr_idc"]: 
    hdfkeys += [f"{key}", f"{key}FitParams", f"{key}DepositedEnergy", f"{key}TruncatedDepositedEnergy"]

# reco var from RecoObservables
for sfx in ["", "_ibr", "_ibr_idc"]:
    hdfkeys += [f'RecoContainedSingle{sfx}', f'RecoContained1{sfx}', f'RecoContained2{sfx}']
    hdfkeys += [f'RecoL{sfx}', f'RecoERatio{sfx}',f'RecoEConfinement{sfx}', f'RecoETot{sfx}', f'RecoLogE1{sfx}', f'RecoLogE2{sfx}']
    hdfkeys += [f'RecoZenith{sfx}', f'RecoAzimuth{sfx}', f'RecoLbyE{sfx}']
    hdfkeys += [f'FinalTopology{sfx}', f"FinalEventClass{sfx}"]
    hdfkeys += [f"TaupedeFit_iMIGRAD_PPB0{sfx}HESEEventclass"]


hdfkeys += [
    'MCInteractionEventclass',
    'TauDecayLength','TauEnergy','TauNeutrinoEnergy','MCInteractionDoubleBang', 'MCReconstructionEventclass', 

    'ConventionalAtmosphericPassingFractions', 'PromptAtmosphericPassingFractions',

    # neha true variables
    'TrueAzimuth', 'TrueETot', 'TrueL', 'TrueZenith', 'TrueERatio', 'TrueEConfinement', 'TrueE1', 'TrueE2',

    # event generator
    'EventGeneratorDC_Max', 'EventGeneratorDC_Thijs', 'EventGeneratorDC_Combined',
    'RecoERatio_EventGeneratorDC_Max', 'RecoERatio_EventGeneratorDC_Thijs',

    # bdt
    'TauMonoDiff_rlogl', 'Taupede_Asymmetry', 'Taupede_Distance',
    'Taupede1_Particles_energy', 'Taupede2_Particles_energy',
    'cscdSBU_MonopodFit4_noDC_zenith', 'MonopodFit_iMIGRAD_PPB0_Delay_ice',
    'CVStatistics_q_max_doms', 'cscdSBU_VertexRecoDist_CscdLLh',
    'cscdSBU_Qtot_HLC_log', 'Taupede_ftpFitParams_rlogl',
    'cscdSBU_MonopodFit4_noDCFitParams_rlogl',

    'TauMonoMilliDiff_rlogl', 'TauSPEMilliDiff_rlogl',

    # HESE
    'HESE_VHESelfVeto', 'HESE_CausalQTot', 'HESE_HomogenizedQTot',
    'VHESelfVeto', 'CausalQTot', 'HomogenizedQTot',
    'QFilterMask', 'QFilterMask_HESEFilter_15_condition_passed',

    # AddOutgoingParticles
    'VertexOutgoingHadron', 'VertexOutgoingLepton',
    'VertexOutgoingHadronOne', 'VertexOutgoingHadronTwo',

    # AddMCInfo
    'MostEnergeticPrimary', 'MostEnergeticNeutrino', 'MostEnergeticInIce',
    'MostEnergeticMuon', 'MostEnergeticCascade', 'MCTrack',
    'MCInteractionType', 'MCInteractionDepth',
    'MCTrueDepositedEnergy', 'MCTrueTruncatedDepositedEnergy',
    'MCInteractionDoubleBang1', 'MCInteractionDoubleBang2',

    # more Neha stuff
    'Filenum', 'TaupedeFitManualFitStatus', 'issingle', 'isdouble', 'istrack',

    # add extra variables for Kevin
    'TrueContainedSingle', 'TrueContained1', 'TrueContained2',

    # weight, polarization, more
    'TotalWeight', 'TotalWeightPol', 'TotalWeight_Original',
    'y_lep', 'y_had','SnowstormParameterDict',
    'DNNC_I3Particle',

    # muon stuff
    'MuonWeightConv','MuonWeightPrompt','MuonWeightScaled',

    # cascade keys from /home/pfuerst/software/processing/cascades-processing/i3_to_summary_hdf_cascades_rnaab.py
    'cscdSBU_MonopodFit4','cscdSBU_LE_bdt_input','cscdSBU_LE_bdt_cascade','cscdSBU_LE_bdt_hybrid','cscdSBU_LE_bdt_track', 
    'cscdSBU_L4StartingTrackHLC_cscdSBU_MonopodFit4_OfflinePulsesHLC_noDCVetoCharge',
    'cscdSBU_MonopodFit4_Delay_ice', 'cscdSBU_Qtot_HLC_IC', 'CascadeLlhVertexFit_L2Params',
    'cscdSBU_VetoMaxDomChargeOM', 'cscdSBU_VetoDepthFirstHit',
    'cscdSBU_MCPrimary','PolyplopiaPrimary',
    'penetrating_depth','penetrating_depth_old', 'penetrating_depth_v1_gcd','penetrating_depth_v1_gcd_old',
]