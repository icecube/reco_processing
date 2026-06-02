features_list_dict = {}

# features_list_dict["13features"] = [
# 'TauMonoDiff_rlogl',
# 'Taupede_Asymmetry',
# 'Taupede_Distance',
# 'Taupede1_Particles_energy',
# 'Taupede2_Particles_energy',
# 'cscdSBU_MonopodFit4_noDC_zenith',
# 'MonopodFit_iMIGRAD_PPB0_Delay_ice',
# 'CVStatistics_q_max_doms',
# 'cscdSBU_VertexRecoDist_CscdLLh',
# 'MonopodFit_iMIGRAD_PPB0_energy',
# 'cscdSBU_Qtot_HLC_log',
# 'Taupede_ftpFitParams_rlogl', # bad data/mc
# 'cscdSBU_MonopodFit4_noDCFitParams_rlogl', # bad data/mc
# ]

# features_list_dict["11features"] = [
# 'TauMonoDiff_rlogl',
# 'Taupede_Asymmetry',
# 'Taupede_Distance',
# 'Taupede1_Particles_energy',
# 'Taupede2_Particles_energy',
# 'cscdSBU_MonopodFit4_noDC_zenith',
# 'MonopodFit_iMIGRAD_PPB0_Delay_ice',
# 'CVStatistics_q_max_doms',
# 'cscdSBU_VertexRecoDist_CscdLLh',
# 'MonopodFit_iMIGRAD_PPB0_energy',
# 'cscdSBU_Qtot_HLC_log',
# ]

# features_list_dict["simple"] = [
# 'TauMonoDiff_rlogl',
# 'Taupede_Asymmetry',
# 'Taupede_Distance',
# 'Taupede1_Particles_energy',
# 'Taupede2_Particles_energy',
# 'cscdSBU_MonopodFit4_noDC_zenith',
# 'MonopodFit_iMIGRAD_PPB0_energy',
# ]

# features_list_dict["11features_plus_evtgen"] = [
# 'TauMonoDiff_rlogl',
# 'Taupede_Asymmetry',
# 'Taupede_Distance',
# 'Taupede1_Particles_energy',
# 'Taupede2_Particles_energy',
# 'cscdSBU_MonopodFit4_noDC_zenith',
# 'MonopodFit_iMIGRAD_PPB0_Delay_ice',
# 'CVStatistics_q_max_doms',
# 'cscdSBU_VertexRecoDist_CscdLLh',
# 'MonopodFit_iMIGRAD_PPB0_energy',
# 'cscdSBU_Qtot_HLC_log',
# 'EventGeneratorDC_Thijs_length',
# 'RecoERatio_EventGeneratorDC_Max',
# ]

# features_list_dict["11features_plus_econf"] = [
# 'TauMonoDiff_rlogl',
# 'Taupede_Asymmetry',
# 'Taupede_Distance',
# 'Taupede1_Particles_energy',
# 'Taupede2_Particles_energy',
# 'cscdSBU_MonopodFit4_noDC_zenith',
# 'MonopodFit_iMIGRAD_PPB0_Delay_ice',
# 'CVStatistics_q_max_doms',
# 'cscdSBU_VertexRecoDist_CscdLLh',
# 'MonopodFit_iMIGRAD_PPB0_energy',
# 'cscdSBU_Qtot_HLC_log',
# 'econfinement',
# ]

# features_list_dict["11features_plus_millirlogl"] = [
# 'TauMonoDiff_rlogl',
# 'Taupede_Asymmetry',
# 'Taupede_Distance',
# 'Taupede1_Particles_energy',
# 'Taupede2_Particles_energy',
# 'cscdSBU_MonopodFit4_noDC_zenith',
# 'MonopodFit_iMIGRAD_PPB0_Delay_ice',
# 'CVStatistics_q_max_doms',
# 'cscdSBU_VertexRecoDist_CscdLLh',
# 'MonopodFit_iMIGRAD_PPB0_energy',
# 'cscdSBU_Qtot_HLC_log',
# 'MonopodFit_iMIGRAD_PPB0MillipedeFitFitParams_rlogl',
# 'SPEFit16_PPB0MillipedeFitFitParams_rlogl',
# 'TaupedeFit_iMIGRAD_PPB0MillipedeFitFitParams_rlogl',
# ]

# features_list_dict["11features_plus_milliE"] = [
# 'TauMonoDiff_rlogl',
# 'Taupede_Asymmetry',
# 'Taupede_Distance',
# 'Taupede1_Particles_energy',
# 'Taupede2_Particles_energy',
# 'cscdSBU_MonopodFit4_noDC_zenith',
# 'MonopodFit_iMIGRAD_PPB0_Delay_ice',
# 'CVStatistics_q_max_doms',
# 'cscdSBU_VertexRecoDist_CscdLLh',
# 'MonopodFit_iMIGRAD_PPB0_energy',
# 'cscdSBU_Qtot_HLC_log',
# 'MonopodFit_iMIGRAD_PPB0MillipedeFitTruncatedDepositedEnergy',
# 'SPEFit16_PPB0MillipedeFitTruncatedDepositedEnergy',
# 'TaupedeFit_iMIGRAD_PPB0MillipedeFitTruncatedDepositedEnergy',
# ]

# features_list_dict["11features_plus_rloglmilli"] = [
# 'TauMonoDiff_rlogl',
# 'Taupede_Asymmetry',
# 'Taupede_Distance',
# 'Taupede1_Particles_energy',
# 'Taupede2_Particles_energy',
# 'cscdSBU_MonopodFit4_noDC_zenith',
# 'MonopodFit_iMIGRAD_PPB0_Delay_ice',
# 'CVStatistics_q_max_doms',
# 'cscdSBU_VertexRecoDist_CscdLLh',
# 'MonopodFit_iMIGRAD_PPB0_energy',
# 'cscdSBU_Qtot_HLC_log',
# 'TauMonoMilliDiff_rlogl',
# 'TauSPEMilliDiff_rlogl',
# ]

# features_list_dict["11features_ibr"] = [
# 'TaupedeFit_iMIGRAD_PPB0_ibr_MonopodFit_iMIGRAD_PPB0_ibr_Diff_rlogl',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_Asymmetry',
# 'RecoL_ibr',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_1_energy',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_2_energy',
# 'MonopodFit_iMIGRAD_PPB0_ibr_zenith',
# 'MonopodFit_iMIGRAD_PPB0_Delay_ice',
# 'CVStatistics_q_max_doms',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_VertexRecoDist_CscdLLh',
# 'MonopodFit_iMIGRAD_PPB0_ibr_energy',
# 'cscdSBU_Qtot_HLC_log',
# ]

# features_list_dict["11features_ibr_idc"] = [
# 'TaupedeFit_iMIGRAD_PPB0_ibr_idc_MonopodFit_iMIGRAD_PPB0_ibr_idc_Diff_rlogl',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_idc_Asymmetry',
# 'RecoL_ibr_idc',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_idc_1_energy',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_idc_2_energy',
# 'MonopodFit_iMIGRAD_PPB0_ibr_idc_zenith',
# 'MonopodFit_iMIGRAD_PPB0_Delay_ice',
# 'CVStatistics_q_max_doms',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_idc_VertexRecoDist_CscdLLh',
# 'MonopodFit_iMIGRAD_PPB0_ibr_idc_energy',
# 'cscdSBU_Qtot_HLC_log',
# ]

features_list_dict["11features_plus_rloglmilli_econf_evtgen"] = [
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
'TauMonoMilliDiff_rlogl',
'TauSPEMilliDiff_rlogl',
'econfinement',
'EventGeneratorDC_Thijs_length',
'RecoERatio_EventGeneratorDC_Max',
]

# features_list_dict["11features_ibr_plus_rloglmilli_econf_evtgen"] = [
# 'TaupedeFit_iMIGRAD_PPB0_ibr_MonopodFit_iMIGRAD_PPB0_ibr_Diff_rlogl',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_Asymmetry',
# 'RecoL_ibr',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_1_energy',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_2_energy',
# 'MonopodFit_iMIGRAD_PPB0_ibr_zenith',
# 'MonopodFit_iMIGRAD_PPB0_Delay_ice',
# 'CVStatistics_q_max_doms',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_VertexRecoDist_CscdLLh',
# 'MonopodFit_iMIGRAD_PPB0_ibr_energy',
# 'cscdSBU_Qtot_HLC_log',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_MonopodFit_iMIGRAD_PPB0_ibr_MilliDiff_rlogl',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_SPEFit16_PPB0_ibr_MilliDiff_rlogl',
# 'econfinement',
# 'EventGeneratorDC_Thijs_length',
# 'RecoERatio_EventGeneratorDC_Max',
# ]

# features_list_dict["11features_ibr_idc_plus_rloglmilli_econf_evtgen"] = [
# 'TaupedeFit_iMIGRAD_PPB0_ibr_idc_MonopodFit_iMIGRAD_PPB0_ibr_idc_Diff_rlogl',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_idc_Asymmetry',
# 'RecoL_ibr_idc',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_idc_1_energy',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_idc_2_energy',
# 'MonopodFit_iMIGRAD_PPB0_ibr_idc_zenith',
# 'MonopodFit_iMIGRAD_PPB0_Delay_ice',
# 'CVStatistics_q_max_doms',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_idc_VertexRecoDist_CscdLLh',
# 'MonopodFit_iMIGRAD_PPB0_ibr_idc_energy',
# 'cscdSBU_Qtot_HLC_log',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_idc_MonopodFit_iMIGRAD_PPB0_ibr_idc_MilliDiff_rlogl',
# 'TaupedeFit_iMIGRAD_PPB0_ibr_idc_SPEFit16_PPB0_ibr_idc_MilliDiff_rlogl',
# 'econfinement',
# 'EventGeneratorDC_Thijs_length',
# 'RecoERatio_EventGeneratorDC_Max',
# ]

# features_list_dict["11features_plus_rloglmilli_econf"] = [
# 'TauMonoDiff_rlogl',
# 'Taupede_Asymmetry',
# 'Taupede_Distance',
# 'Taupede1_Particles_energy',
# 'Taupede2_Particles_energy',
# 'cscdSBU_MonopodFit4_noDC_zenith',
# 'MonopodFit_iMIGRAD_PPB0_Delay_ice',
# 'CVStatistics_q_max_doms',
# 'cscdSBU_VertexRecoDist_CscdLLh',
# 'MonopodFit_iMIGRAD_PPB0_energy',
# 'cscdSBU_Qtot_HLC_log',
# 'TauMonoMilliDiff_rlogl',
# 'TauSPEMilliDiff_rlogl',
# 'econfinement',
# ]
