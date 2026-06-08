"""Script to calculate Histograms for real data fits.

python pulls.py --precalculated_graph /data/user/pfuerst/DiffuseExtensions/fitdata/GP_globalfit/data/step0/TESTRUN_background_tracks_only_2D/Precalculated_Graph.pickle --fit_result /data/user/pfuerst/DiffuseExtensions/fitdata/GP_globalfit/data/step0/TESTRUN_background_tracks_only_2D/Freefit_01.pickle --output /data/user/pfuerst/DiffuseExtensions/fitdata/GP_globalfit/data/step0/TESTRUN_background_tracks_only_2D/pull_output.pickle
"""

# give it a fit_configuration (to calculate the real histogram from)

# and a fit file (to calculate the expectation from)

# alternatively give it two histograms, a data histogram and a MC histogram. The MC hist needs fluctuations,
# the data histogram may have fluctuations, otherwise just take sqrt()

# make the corresponding argparser
from NNMFit.utilities import load_pickle
from NNMFit import likelihoods
from NNMFit.utilities.readout_graphs import LLHmap
import numpy as np
from argparse import ArgumentParser, Namespace
from histogram_maker import make_histogram_from_fit
from freefit_parameter_config import FreefitParamConfig
import argparse
import sys
import os


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process either fit configuration files or histogram files."
    )
    parser.add_argument('scan_path', type=str, help='Path to scan path file')
    # optional fit result (otherwise, auto-detect from scan path)
    parser.add_argument(
        '--fit_result',
        type=str,
        help=
        'Path to fit result file to evaluate (optional, auto-detects the bestfit)',
        default=None,
    )
    parser.add_argument(
        '--sat_llh_save_dir',
        type=str,
        default=
        "/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/unblind/philipp/saturated",
    )
    parser.add_argument(
        '--not_force_read',
        action='store_false',
        help='Force reading the scan handler, even if it already exists.',
    )

    parsed_args = parser.parse_args()
    return parsed_args


# all of these are dicts with multiple entries, one for each det_config!
def generate_data_hist(scan_path):
    # Auto-generate a name for the (Data/injected) Histogram from the fit
    data_hist_filename = os.path.join(scan_path, "Data_Histogram.pickle")
    precalc_graph_path = os.path.join(scan_path, "Precalculated_Graph.pickle")

    # generate and save the data histogram if it does not exist
    if not os.path.exists(data_hist_filename):
        print(f"Generating Data Histogram: {data_hist_filename}")
        # generate and save the data histogram
        cmd = (
            f"make_histogram.py --precalculated_graph "
            f"{precalc_graph_path} --outfile {data_hist_filename}"
        )
        os.system(cmd)
    else:
        print(f"Data Histogram already exists: {data_hist_filename}")

    # load the data histogram
    print(f"Loading Data Histogram: {data_hist_filename}")
    return load_pickle(data_hist_filename)


def generate_mc_hist(scan_path, fit_file, fit_name, add_variables={}, name="MC_Histogram"):

    # get graph
    precalc_graph_path = os.path.join(scan_path, "Precalculated_Graph.pickle")

    mc_hist_filename = os.path.join(
        scan_path, f"{name}_{fit_name}.pickle"
    )

    # force rebuild once as these were buggy
    # if os.path.exists(mc_hist_filename):
    #     print(f"MC Histogram already exists: {mc_hist_filename}")

    # else:
    # build configuration
    nnnmfit_options_c = {
        "init_method": "from_precalculation",
        "precalculated_graph": precalc_graph_path,
    }

    # generate the histogram from the fit result & save
    make_histogram_from_fit(nnnmfit_options_c, fit_file, mc_hist_filename, add_variables=add_variables)
    return load_pickle(mc_hist_filename)


def generate_llh_map(scan_path, fit_file, fit_result_name):
    """
    Evaluate the bin-wise LLH values given the parameter values from the fit file.

    Parameters
    ----------

    scan_path: str
                the path where the scan files are.
    fit_file: str
                the path to the filename of the fit file from which to take the parameters
                values. Has to be a freefit (which has all parameters in the 
                fit-result).
    """
    # get llhmap name
    llh_map_filename = os.path.join(
        scan_path, f"LLH_Maps_{fit_result_name}.pickle"
    )

    if os.path.exists(llh_map_filename):
        print(f"LLH Map already exists: {llh_map_filename}")
        return
    # get graph
    precalc_graph_path = os.path.join(scan_path, "Precalculated_Graph.pickle")
    llh_hdl = LLHmap.from_precalculated_file(precalc_graph_path)
    llh_hdl.setup_llh()

    # get input variables: fit result from fit file
    # assert that this was a freefit file, otherwise this currently does not work
    if not "freefit" in fit_file.lower():
        raise ValueError(
            "Fit file must be a freefit file to generate the LLH map."
        )
    fit_result = load_pickle(fit_file)["fit-result"][1]

    out_dict = {}
    for det_config in llh_hdl.config_hdl.detector_configs:
        out_map = llh_hdl.eval_llh_func(
            det_config=det_config, input_variables=fit_result, reshape=True
        )
        out_dict[det_config] = out_map

    # save
    print(f"Saving LLH Map to: {llh_map_filename}")
    # dump pickle
    with open(llh_map_filename, 'wb') as f:
        import pickle
        pickle.dump(out_dict, f)



def calc_sat_llh(data_hist, calculation_type="poisson"):
    if calculation_type != "poisson":
        raise NotImplementedError(
            f"Calculation type {calculation_type} not implemented."
        )
    det_configs = list(data_hist.keys())
    sat_llh = 0
    for det_config in det_configs:
        k = data_hist[det_config]
        sat_llh += np.sum(likelihoods.PoissonLLH.compute_log_L_non_graph(k, k))
    return -1 * sat_llh  # we save -llh in all cases


if __name__ == "__main__":
    # get args
    args = parse_arguments()

    # get fit result file
    if args.fit_result is None:
        print(
            "Auto-Detecting the best fit from among the freefits in the scan path."
        )
        freefit_param_config = FreefitParamConfig(
            args.scan_path, force_read=args.not_force_read
        )

        # get the minimum log-likelihood and its index
        min_llh, min_llh_index, min_llh_row = freefit_param_config.get_min_llh_freefit(
            freefit_param_config.scan_hdl
        )
        fit_result_name = freefit_param_config.get_freefit_filename_from_index(
            min_llh_index
        )
        fit_result_file = os.path.join(
            args.scan_path, f"{fit_result_name}.pickle"
        )
    else:
        fit_result_file = args.fit_result

        # load the fit result and get the llh value:
        fit_result = load_pickle(fit_result_file)
        min_llh = fit_result['fit-result'][0]
        fit_result_name = os.path.basename(fit_result_file).replace(
            '.pickle', ''
        )

    # generate and save mc hist (or just load it if already exists)
    mc_hist = generate_mc_hist(args.scan_path, fit_result_file, fit_result_name)

    # generate the mc hist again but force the gp parameter(s) to be zero
    # we can set them all to zero, the ones that do not appear in any configured
    # fluxes will just be ignored
    all_gp0_dict = {
        "fermi_norm": 0.0,
        "cringefits_and_unresolved_norm": 0.0,
        "cringefits_norm": 0.0,
        "fmconst_norm": 0.0,
        "fmsnr_norm": 0.0,
        "kra50_norm": 0.0,
        "kra5_norm": 0.0,
    }
    mc_hist_bestfit_gp0 = generate_mc_hist(args.scan_path, fit_result_file, fit_result_name + "_set_gp0", add_variables=all_gp0_dict)

    # generate and save data hist (or just load it if already exists)
    data_hist = generate_data_hist(args.scan_path)

    # generate and save the llh maps
    generate_llh_map(args.scan_path, fit_result_file, fit_result_name)

    # calculate and save sat llh
    sat_llh = calc_sat_llh(data_hist["histograms"], calculation_type="poisson")
    print(f"Saturated LLH: {sat_llh}")
    # save as mini-txt. name is the last part of the scan path
    # Normalize the path (optional but good practice)
    path = os.path.normpath(args.scan_path)

    # Split the path into parts
    parts = path.split(os.sep)

    # Get the last and second-to-last directories
    last_dir = parts[-1]
    second_last_dir = parts[-2]

    os.system(f"mkdir -p {args.sat_llh_save_dir}/{second_last_dir}")

    # for now, save these in the unblinding dir so we can transfer between
    # servers
    sat_llh_filename = os.path.join(
        args.sat_llh_save_dir,
        second_last_dir,
        f"SatLLH_{last_dir}.txt"
    )

    # write the full scan path and sat_llh in the txt file
    with open(sat_llh_filename, 'w') as f:
        f.write(f"Scan Path: {args.scan_path}\n")
        f.write(f"min LLH: {min_llh}\n")
        f.write(f"Saturated LLH: {sat_llh}\n")
    print(f"Min LLH: {min_llh}, sat. LLH: {sat_llh}")
    print(f"LLH info saved to: {sat_llh_filename}")
