

### General

CONFIG_DIR=/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/configs/flavor_globalfit/
THIS_DIR=/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/datasets/flavor_globalfit/hese

dataset=IC86_pass2_SnowStorm_v2_FTP_Ensemble_hdf-v1_fluxlessweight
model=FinalTopology_double_energy_length_binning # mcd-simpletopology_flux-hese_feat-11features_plus_rloglmilli_econf_evtgen
outpath=${THIS_DIR}/combined_with_bdt/systematics/${dataset}/${model}
analysis_config=pse/hese/debug_bdt/FinalTopology_double_energy_length_binning/FinalTopology_double_energy_length_binning_combined.yaml

mkdir -p ${outpath}

###
### Combined, needed for debugging unblinding
###

# just energy zenith
mkdir -p ${outpath}
calculate_SnowStorm_gradients.py \
    --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
    --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
    --main_config ${CONFIG_DIR}/main.cfg \
    --config_dir ${CONFIG_DIR} \
    --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
                       ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                       ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
    --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
    --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_energy_zenith.pickle \
    --calculate_cross_correlations \


# bdt1 bdt2
mkdir -p ${outpath}
calculate_SnowStorm_gradients.py \
    --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
    --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
    --main_config ${CONFIG_DIR}/main.cfg \
    --config_dir ${CONFIG_DIR} \
    --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
                       ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/bdt1_bdt2_10bins.cfg \
                       ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
    --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
    --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_bdt1_bdt2.pickle \
    --calculate_cross_correlations \

# # 8 pairs of 16 bdt var

mkdir -p ${outpath}
calculate_SnowStorm_gradients.py \
    --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
    --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
    --main_config ${CONFIG_DIR}/main.cfg \
    --config_dir ${CONFIG_DIR} \
    --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
                       ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/Taupede_Distance_Taupede_Asymmetry_10bins.cfg \
                       ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
    --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
    --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_len_easym.pickle \
    --calculate_cross_correlations \

mkdir -p ${outpath}
calculate_SnowStorm_gradients.py \
    --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
    --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
    --main_config ${CONFIG_DIR}/main.cfg \
    --config_dir ${CONFIG_DIR} \
    --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
                       ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/Taupede1_Particles_energy_Taupede2_Particles_energy_10bins.cfg \
                       ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
    --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
    --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_e1_e2.pickle \
    --calculate_cross_correlations \

mkdir -p ${outpath}
calculate_SnowStorm_gradients.py \
    --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
    --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
    --main_config ${CONFIG_DIR}/main.cfg \
    --config_dir ${CONFIG_DIR} \
    --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
                       ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/Taupede1_Particles_energy_Taupede2_Particles_energy_10bins_zoom.cfg \
                       ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
    --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
    --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_e1_e2_zoom.pickle \
    --calculate_cross_correlations \


mkdir -p ${outpath}
calculate_SnowStorm_gradients.py \
    --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
    --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
    --main_config ${CONFIG_DIR}/main.cfg \
    --config_dir ${CONFIG_DIR} \
    --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
                       ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/MonopodFit_iMIGRAD_PPB0_energy_cscdSBU_MonopodFit4_noDC_zenith_10bins.cfg \
                       ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
    --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
    --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_mono_energy_zenith.pickle \
    --calculate_cross_correlations \

mkdir -p ${outpath}
calculate_SnowStorm_gradients.py \
    --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
    --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
    --main_config ${CONFIG_DIR}/main.cfg \
    --config_dir ${CONFIG_DIR} \
    --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
                       ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/MonopodFit_iMIGRAD_PPB0_Delay_ice_CVStatistics_q_max_doms_10bins.cfg \
                       ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
    --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
    --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_mono_delay_qmax.pickle \
    --calculate_cross_correlations \

mkdir -p ${outpath}
calculate_SnowStorm_gradients.py \
    --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
    --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
    --main_config ${CONFIG_DIR}/main.cfg \
    --config_dir ${CONFIG_DIR} \
    --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
                       ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/MonopodFit_iMIGRAD_PPB0_Delay_ice_CVStatistics_q_max_doms_10bins_zoom.cfg \
                       ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
    --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
    --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_mono_delay_qmax_zoom.pickle \
    --calculate_cross_correlations \

mkdir -p ${outpath}
calculate_SnowStorm_gradients.py \
    --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
    --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
    --main_config ${CONFIG_DIR}/main.cfg \
    --config_dir ${CONFIG_DIR} \
    --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
                       ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cscdSBU_VertexRecoDist_CscdLLh_cscdSBU_Qtot_HLC_log_10bins.cfg \
                       ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
    --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
    --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_vtxdist_qtot.pickle \
    --calculate_cross_correlations \

mkdir -p ${outpath}
calculate_SnowStorm_gradients.py \
    --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
    --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
    --main_config ${CONFIG_DIR}/main.cfg \
    --config_dir ${CONFIG_DIR} \
    --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
                       ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cscdSBU_VertexRecoDist_CscdLLh_cscdSBU_Qtot_HLC_log_10bins_zoom.cfg \
                       ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
    --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
    --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_vtxdist_qtot_zoom.pickle \
    --calculate_cross_correlations \

mkdir -p ${outpath}
calculate_SnowStorm_gradients.py \
    --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
    --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
    --main_config ${CONFIG_DIR}/main.cfg \
    --config_dir ${CONFIG_DIR} \
    --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
                       ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/TauMonoDiff_rlogl_econfinement_10bins.cfg \
                       ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
    --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
    --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_taumono_econf.pickle \
    --calculate_cross_correlations \

mkdir -p ${outpath}
calculate_SnowStorm_gradients.py \
    --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
    --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
    --main_config ${CONFIG_DIR}/main.cfg \
    --config_dir ${CONFIG_DIR} \
    --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
                       ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/TauMonoDiff_rlogl_econfinement_10bins_zoom.cfg \
                       ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
    --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
    --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_taumono_econf_zoom.pickle \
    --calculate_cross_correlations \




mkdir -p ${outpath}
calculate_SnowStorm_gradients.py \
    --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
    --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
    --main_config ${CONFIG_DIR}/main.cfg \
    --config_dir ${CONFIG_DIR} \
    --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
                       ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/TauSPEMilliDiff_rlogl_TauMonoMilliDiff_rlogl_10bins.cfg \
                       ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
    --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
    --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_tauspe_taumilli.pickle \
    --calculate_cross_correlations \

mkdir -p ${outpath}
calculate_SnowStorm_gradients.py \
    --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
    --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
    --main_config ${CONFIG_DIR}/main.cfg \
    --config_dir ${CONFIG_DIR} \
    --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
                       ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/TauSPEMilliDiff_rlogl_TauMonoMilliDiff_rlogl_10bins_zoom.cfg \
                       ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
    --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
    --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_tauspe_taumilli_zoom.pickle \
    --calculate_cross_correlations \



mkdir -p ${outpath}
calculate_SnowStorm_gradients.py \
    --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
    --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
    --main_config ${CONFIG_DIR}/main.cfg \
    --config_dir ${CONFIG_DIR} \
    --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
                       ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/EventGeneratorDC_Thijs_length_RecoERatio_EventGeneratorDC_Max_10bins.cfg \
                       ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
    --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
    --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_evtgen_recoeratio.pickle \
    --calculate_cross_correlations \

mkdir -p ${outpath}
calculate_SnowStorm_gradients.py \
    --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
    --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
    --main_config ${CONFIG_DIR}/main.cfg \
    --config_dir ${CONFIG_DIR} \
    --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
                       ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/EventGeneratorDC_Thijs_length_RecoERatio_EventGeneratorDC_Max_10bins_zoom.cfg \
                       ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
    --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
    --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_evtgen_recoeratio_zoom.pickle \
    --calculate_cross_correlations \

# some extra with energy and length, like in the double signal region

mkdir -p ${outpath}
calculate_SnowStorm_gradients.py \
    --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
    --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
    --main_config ${CONFIG_DIR}/main.cfg \
    --config_dir ${CONFIG_DIR} \
    --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
                       ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/energy_length_analysis.cfg \
                       ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                       ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
    --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
    --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_energy_length_analysis.pickle \
    --calculate_cross_correlations \

# ###
# ### extra zheyang hists
# ###

# mkdir -p ${outpath}
# calculate_SnowStorm_gradients.py \
#     --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
#     --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
#     --main_config ${CONFIG_DIR}/main.cfg \
#     --config_dir ${CONFIG_DIR} \
#     --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
#                        ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
#                        ${CONFIG_DIR}/override/binning/hese/combined/EventGeneratorDC_Thijs_length_RecoERatio_EventGeneratorDC_Max_20bins_zheyang.cfg \
#                        ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
#                        ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
#     --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
#     --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_evtgen_recoeratio_zheyang.pickle \
#     --calculate_cross_correlations \

# mkdir -p ${outpath}
# calculate_SnowStorm_gradients.py \
#     --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
#     --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
#     --main_config ${CONFIG_DIR}/main.cfg \
#     --config_dir ${CONFIG_DIR} \
#     --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
#                        ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
#                        ${CONFIG_DIR}/override/binning/hese/combined/TauSPEMilliDiff_rlogl_TauMonoMilliDiff_rlogl_20bins_zheyang.cfg \
#                        ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
#                        ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
#     --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
#     --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_tauspe_taumilli_zheyang.pickle \
#     --calculate_cross_correlations \

# mkdir -p ${outpath}
# calculate_SnowStorm_gradients.py \
#     --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
#     --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
#     --main_config ${CONFIG_DIR}/main.cfg \
#     --config_dir ${CONFIG_DIR} \
#     --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
#                        ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
#                        ${CONFIG_DIR}/override/binning/hese/combined/TauMonoDiff_rlogl_econfinement_20bins_zheyang.cfg \
#                        ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
#                        ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
#     --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
#     --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_taumono_econf_zheyang.pickle \
#     --calculate_cross_correlations \

# mkdir -p ${outpath}
# calculate_SnowStorm_gradients.py \
#     --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
#     --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
#     --main_config ${CONFIG_DIR}/main.cfg \
#     --config_dir ${CONFIG_DIR} \
#     --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_11features_rloglmilli_econf_evtgen.cfg \
#                        ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
#                        ${CONFIG_DIR}/override/binning/hese/combined/Taupede_Distance_Taupede_Asymmetry_20bins_zheyang.cfg \
#                        ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
#                        ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
#     --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
#     --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_len_easym_zheyang.pickle \
#     --calculate_cross_correlations \