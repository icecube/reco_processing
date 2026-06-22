

### General

CONFIG_DIR=/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/configs/flavor_globalfit/
THIS_DIR=/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/datasets/flavor_globalfit/hese

dataset=IC86_pass2_SnowStorm_v2_FTP_Ensemble_hdf-v1_fluxlessweight
analysis_config=pse/hese/debug_bdt/FinalTopology_double_energy_length_binning/FinalTopology_double_energy_length_binning_combined.yaml

###
### Combined, needed for debugging unblinding
###

feature_names=(
    "11features_plus_rloglmilli_econf_evtgen"
    "11features"
    "11features_plus_rloglmilli"
    "11features_plus_econf"
    "11features_plus_evtgen"
)

for feature in "${feature_names[@]}"; do
    model=mcd-simpletopology_flux-hese_feat-${feature}
    outpath=${THIS_DIR}/combined_with_bdt/systematics/${dataset}/${model}
    cfg_name=${feature//_plus_/_}  # remove "_plus" → e.g. 11features_rloglmilli_evtgen

    mkdir -p ${outpath}
    calculate_SnowStorm_gradients.py \
        --gradient_config ${CONFIG_DIR}/GradientInputs/Crystal_HESEBestfit_SPL.yaml \
        --analysis_config ${CONFIG_DIR}/analysis_configs/${analysis_config} \
        --main_config ${CONFIG_DIR}/main.cfg \
        --config_dir ${CONFIG_DIR} \
        --override_configs ${CONFIG_DIR}/override/systematics/hese_combined/CreateSystematics_HESE_combined_${cfg_name}.cfg \
                           ${CONFIG_DIR}/override/systematics/NoSystematics_hese_combined.cfg \
                           ${CONFIG_DIR}/override/binning/hese/combined/bdt1_bdt2_10bins.cfg \
                           ${CONFIG_DIR}/override/livetime/hese_livetime_13yr_asr.cfg \
                           ${CONFIG_DIR}/override/binning/hese/combined/cut_energy.cfg \
        --override_components ${CONFIG_DIR}/override/components/astro_SPL_no_inel_no_flavor.yaml \
        --outfile ${outpath}/hese_combined_HESEBestfit_SPL_no_flavor_bdt1_bdt2.pickle \
        --calculate_cross_correlations

done
