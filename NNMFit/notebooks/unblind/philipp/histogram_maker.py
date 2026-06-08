import os
import numpy as np

from NNMFit.utilities import load_pickle
from NNMFit import AnalysisConfig
from NNMFit.utilities import HistogramGraph
# from NNMFit.utilities import SkyMap
import pickle

# example configuration options
NNMFit_config_options_A = {
    "init_method": "from_configs",
    "main_config": None,
    "analysis_config": None,
    "config_dir": None,
    "override_configs": [],
    "override_parameters": [],
    "override_components": [],
}

NNMFit_config_options_B = {
    "init_method": "from_file",
    "config_infile": None,
}

NNMFit_config_options_C = {
    "init_method": "from_precalculation",
    "precalculated_graph": None,
}





def make_histogram_from_fit(NNMFit_config_options, fit_file, out_file, add_variables = {}):
    """
    Imitate NNMFits make_histogram.py while setting all parameters to values
    from a fit_file.

    Parameters
    ----------
    NNMFit_config_options : dict
        NNMFit config options, either type A,B, or C
    fit_file : str
        fit file with the parameter values to weight the histogram to.
    out_file : str
        file where the histogram is saved.
    add_variables : dict
        optional additional variables to add to or override the fit variables.
    """

    # create config handler
    config_hdl = AnalysisConfig.from_argparser(NNMFit_config_options)
    config_dict = config_hdl.to_dict()

    # histogramgraph
    hist_graph = HistogramGraph.from_configdict(config_dict)

    # load the fit file
    fit = load_pickle(fit_file)

    # extract best fit variables and set hist_graph to these
    variables = fit["fit-result"][1]

    # add any optional variables:
    for key in add_variables:
        variables[key] = add_variables[key]

    # make histograms, fluctuations
    histograms = {}
    fluctuations = {}

    # make for all det configs
    det_configs = config_dict["analysis"]["detector_configs"]

    # evaluate the histogram at the fit variable values
    for det_config in det_configs:
        out = hist_graph.get_evaled_histogram(
            input_variables=variables, det_config=det_config
        )
        histograms[det_config] = out["mu"]
        fluctuations[det_config] = out["ssq"]

    # overwrite the input params with the variables that were used
    config_dict['analysis']["input_params"] = variables

    # finally evaluate hist_graph:
    todump = {}
    todump["histograms"] = histograms
    # also store settings used for creating the histograms,
    # including the override variables from the fit file
    todump["settings"] = config_dict
    # optionally store fluctuations
    todump['fluctuations'] = fluctuations

    # save to pickle file
    with open(out_file, "wb") as outfile:
        pickle.dump(todump, outfile)


def make_histogram_from_variables(
    NNMFit_config_options, out_file, input_variables=None
):
    """
    Imitate NNMFits make_histogram.py while setting parameters to defaults
    or the values given in the analysis config.

    Parameters
    ----------
    NNMFit_config_options : dict
        NNMFit config options, either type A,B, or C
    fit_file : str
        fit file with the parameter values to weight the histogram to.
    out_file : str
        file where the histogram is saved.
    input_variables : dict or None
        optional input variables to evaluate the histogram at.
    """

    # create config handler
    config_hdl = AnalysisConfig.from_argparser(NNMFit_config_options)
    config_dict = config_hdl.to_dict()

    # histogramgraph
    hist_graph = HistogramGraph.from_configdict(config_dict)

    # make histograms, fluctuations
    histograms = {}
    fluctuations = {}

    # make for all det configs
    det_configs = config_dict["analysis"]["detector_configs"]

    # evaluate the histogram at the fit variable values
    for det_config in det_configs:
        out = hist_graph.get_evaled_histogram(
            det_config=det_config, input_variables=input_variables
        )
        histograms[det_config] = out["mu"]
        fluctuations[det_config] = out["ssq"]

    # finally evaluate hist_graph:
    todump = {}
    todump["histograms"] = histograms

    # also store settings used for creating the histograms,
    # including the override variables from the fit file
    todump["settings"] = config_dict

    # optionally store fluctuations
    todump['fluctuations'] = fluctuations

    # save to pickle file
    with open(out_file, "wb") as outfile:
        pickle.dump(todump, outfile)


def make_histogram_from_fit_per_flux(
    NNMFit_config_options, fit_file, out_file, flux_norm, all_flux_norms
):
    # similar to plot_reco_fluxes.ipynb in  GP_globalfit/reco_space
    # then auto-run on the freefits just like the others.
    # histograms get the name norm_parameter_histogram.-.-. etc

    # do the same as make_histogram_from_fit, but set all flux norms except the one we have here to zero
    # also set the snowstorm gradients to baseline values since they act additively on the full histogram.

    # then plot these.
    # do not run this for: muon templates, galactic plane templates. These can be inserted manually and do 
    # not need to be recalculated.
    pass


if __name__ == "__main__":
    config_dir = "/home/pfuerst/software/analysis/DiffuseNuMu_12a/NNMConfigs/GP_globalfit"
    analysis_configs_path = f"{config_dir}/analysis_configs/asimov/astro_bestfits/poisson/cringe_1/"

    ana_configs_astromodels = [
        "Asimov_Poisson_Powerlaw.yaml",
        "Asimov_Poisson_BrokenPowerlaw.yaml",
        "Asimov_Poisson_LogParabola.yaml",
        "Asimov_Poisson_Piecewise.yaml",
    ]

    override_configs_astromodels = [
        "SPL.cfg",
        "BPL.cfg",
        "LogParabola.cfg",
        "Piecewise.cfg",
    ]

    #######################################################
    # Block to create histograms for discovery scans      #
    #######################################################

    # inject bestfit piecewise
    # piecewise_config = ana_configs_astromodels[3]
    spl_config = ana_configs_astromodels[0]

    # do 3D fits
    # config_3D = "override/astro_and_gp_model/cringe_3d/Piecewise.cfg"
    config_3D = "override/astro_and_gp_model/cringe_3d/Powerlaw.cfg"

    # make muontemplate 3D:
    override_components_list = [
        "override/components/Tracks_defaultbins_3D_muontemplate.yaml"
    ]

    options = {
        "init_method":
            "from_configs",
        "main_config":
            os.path.join(config_dir, "main.cfg"),
        "analysis_config":
            os.path.join(analysis_configs_path, spl_config),
        "config_dir":
            config_dir,
        "override_configs": [os.path.join(config_dir, config_3D)],
        "override_components":
            override_components_list,
        "override_parameters":
            None
    }

    # out path
    # out_base_dir = "/data/user/pfuerst/DiffuseExtensions/asimov_datasets/globalfit/discovery_scan_inject_piecewise"
    out_base_dir = "/data/user/pfuerst/DiffuseExtensions/asimov_datasets/globalfit/discovery_scan_inject_powerlaw"

    for x in np.linspace(0.0, 6.0, 121):
        current_input_variables = {"cringefits_norm": x}
        name = spl_config.replace("Asimov_Poisson_",
                                        "").replace(".yaml", "")
        name = f"{name}_cringefits_norm_{x:.3f}"
        print(name)
        make_histogram_from_variables(
            options,
            # out_file=f"{out_base_dir}/Piecewise+cringefits{x}.pickle",
            out_file=f"{out_base_dir}/Powerlaw+cringefits{x}.pickle",
            input_variables=current_input_variables
        )

    #######################################################
    # Block to create histograms from globalfit bestfits  #
    #######################################################
    # override_components = "override/components/muon_fullrange_3D.yaml"

    # for idx, analysis_config in enumerate(ana_configs_astromodels):
    #     override_config = override_configs_astromodels[idx]
    #     options = {
    #         "init_method": "from_configs",
    #         "main_config": os.path.join(config_dir, "main.cfg"),
    #         "analysis_config": os.path.join(analysis_configs_path, analysis_config),
    #         "config_dir": config_dir,
    #         "override_configs":
    #             [os.path.join(override_configs_path, override_config)],
    #         "override_components":
    #             ["override/components/Tracks_defaultbins_3D_muontemplate.yaml"],
    #         "override_parameters": None
    #     }
    #     name = analysis_config.replace("Asimov_Poisson_", "").replace(".yaml", "")
    #     print(idx, name)
    #     make_histogram_from_variables(
    #         options,
    #         out_file=
    #         f"/data/user/pfuerst/DiffuseExtensions/asimov_datasets/globalfit/Jakob_bestfit_astro_1Cringe/Bestfit_{name}_plusCringe.pickle"
    #     )
