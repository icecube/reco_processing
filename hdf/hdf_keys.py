
hdfkeys = []

# true information tianlu
hdfkeys += ['cc', 'cc_2surf', 'cc_zshift', 'cc_b400_notilt', 'cc_b400_tilted', 'cc_aDust400_notilt', 'cc_aDust400_tilted','cc_easymm', 'cc_tauvis']
hdfkeys += ['tau','cascade','track'] # not sure if these are working

# general info
hdfkeys += ['I3MCWeightDict','I3EventHeader']

# tianlu reco
hdfkeys += ['CombinedCascadeSeed_L3','PreferredFit','MonopodFit_iMIGRAD', 'MonopodFit_iMIGRADFitParams','TaupedeFit_iMIGRAD', 'TaupedeFit_iMIGRADParticles', 'TaupedeFit_iMIGRADFitParams']
hdfkeys += ['MillipedeFit_iMIGRAD','MillipedeFit_iMIGRADParticles', 'MillipedeFit_iMIGRADFitParams', 'seed_iMIGRAD_BestMonopod','seed_iMIGRAD_BestAltnFit']
                                               
# track reco
hdfkeys += ['LineFit','SPEFit2','l2_online_SplineMPE','OnlineL2_SplineMPE']     
                            
# evtgen tianlu
hdfkeys += ['EventGeneratorFit_I3Particle', 'EventGeneratorSelectedReco_I3Particle', 'EventGeneratorSelectedRecoNN_I3Particle','EventGeneratorSelectedRecoNNCircularUncertainty']
                            
hdfkeys += [
    # thijs
    'TaupedeFit_iMIGRAD_PPB0', 'TaupedeFit_iMIGRAD_PPB0FitParams', 'TaupedeFit_iMIGRAD_PPB0Particles',
    'MonopodFit_iMIGRAD_PPB0', 'MonopodFit_iMIGRAD_PPB0FitParams',
    'CscdL3_SPEFit16', 'CscdL3_SPEFit16FitParams',

    # christopher
    'TaupedeFit_iMIGRAD_PPB0_bright', 'TaupedeFit_iMIGRAD_PPB0_brightFitParams',
    'TaupedeFit_iMIGRAD_PPB0_brightParticles',

    # neha reco var
    'HESETaupedeFit', 'HESETaupedeFitFitParams', 'HESETaupedeFitParticles',
    'HESEMonopodFit', 'HESEMonopodFitFitParams', 'HESEMonopodFitParticles',
    'SPEFit16', 'SPEFit16FitParams',
    'HESEMillipedeFit', 'HESEMillipedeFitParticles',

    'HESEEventclass', 'FinalTopology', 'FinalEventClass', 'MCInteractionEventclass',
    'TauDecayLength','TauEnergy','TauNeutrinoEnergy','MCInteractionDoubleBang', 'MCReconstructionEventclass', 

    'ConventionalAtmosphericPassingFractions', 'PromptAtmosphericPassingFractions',

    'RecoL', 'RecoEConfinement', 'RecoERatio', 'RecoETot', 'RecoLogE1', 'RecoLogE2',
    'RecoAzimuth', 'RecoZenith',

    # neha true variables
    'TrueAzimuth', 'TrueETot', 'TrueL', 'TrueZenith', 'TrueERatio', 'TrueEConfinement', 'TrueE1', 'TrueE2',

    # event generator
    'EventGeneratorDC_Max', 'EventGeneratorDC_Thijs',

    # bdt
    'TauMonoDiff_rlogl', 'Taupede_Asymmetry', 'Taupede_Distance',
    'Taupede1_Particles_energy', 'Taupede2_Particles_energy',
    'cscdSBU_MonopodFit4_noDC_zenith', 'MonopodFit_iMIGRAD_PPB0_Delay_ice',
    'CVStatistics_q_max_doms', 'cscdSBU_VertexRecoDist_CscdLLh',
    'cscdSBU_Qtot_HLC_log', 'Taupede_ftpFitParams_rlogl',
    'cscdSBU_MonopodFit4_noDCFitParams_rlogl',

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
    'Filenum', 'HESEMillipedeFitTruncatedDepositedEnergy',
    'HESEMillipedeFitDepositedEnergy', 'TaupedeFitManualFitStatus',
    'HESEMillipedeFitFitParams', 'issingle', 'isdouble', 'istrack',
    'RecoE1', 'RecoE2', 'RecoLbyE', 'TaupedeFitParticles',
    'TaupedeFit', 'TaupedeFitFitParams',

    # weight, polarization, more
    'TotalWeight', 'TotalWeightPol',
    'y_lep', 'y_had','SnowstormParameterDict',
    'DNNC_I3Particle'
]