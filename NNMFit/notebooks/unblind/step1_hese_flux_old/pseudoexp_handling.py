import os

import numpy as np

from scipy.stats import chi2
from scipy.stats import ks_2samp

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import matplotlib.font_manager as font_manager
from NNMFit.utilities import PseudoexpHandler, HistogramGraph

from .plot_utils import savefig
from .plot_utils import plot_hist_errorbar, plot_hist_errorbar_T, make_hist_error
from .plot_utils import plot_energy_and_zenith_data_MC  #, plot_pulls
from .misc import get_central_range, get_bootstrapped_median_error
from .goodness_of_fit import binwise_saturated_llh, binwise_saturated_poisson_llh
from .goodness_of_fit import  calculate_marginalTS_double,calculate_marginalTS_nondouble

class PseudoexpPlotHandler(PseudoexpHandler):
    def __init__(self):
        self.pseudoexp_list = []
        self.__hdls = dict()
        self.__plot_settings = dict()

        self.all_params = []
        self.__injected = dict()

        self.__param_order = dict()

        self.__1d_hist_bins = dict()

        self.__graphs = dict()

    def add_pseudoexp(self, identifier, hdl, **plot_settings):
        """
        Add a pseudoexp to the plotting hdl

        Parameters
        ----------
        identifier : str
            Identifier for the pseudoexp
        hdl : NNMFit.PseudoexpHandler
            NNFit.PseudoexpHandler
        **plot_settings : 
            Any arguments/keywords to passed to the matplotlib plotting
            functions
        """
        # check for identifier already present
        if identifier in self.pseudoexp_list:
            raise KeyError(f"Pseudoexp {identifier} already added!")

        # add pseudoexp to list
        self.pseudoexp_list.append(identifier)

        # add handler to dict
        self.__hdls[identifier] = hdl

        # some default plot settings to use if non configured
        default_plot_settings = dict(
            label=identifier,  # use identifier as default label
            color=f"C{len(self.pseudoexp_list) - 1}"  # matplotlib colorcycle
        )
        # update default plot settings
        default_plot_settings.update(plot_settings)
        self.__plot_settings[identifier] = default_plot_settings

        # add parameters to list
        params = hdl.get_param_names()
        for p in params:
            if not p in self.all_params:
                self.all_params.append(p)

    def get_pseudoexp(self, identifier):
        return self.__hdls[identifier]

    def get_plot_settings(self, identifier):
        return self.__plot_settings[identifier]

    def _set_injected_value_from_seed(self, param, identifier):
        """
        Set injected parameter values from parameter seeds from pseudoexp
        `identifier`.

        Parameters
        ----------
        param : str
            parameter name
        identifier : str
            Pseudoexp identifier to get parameter seeds from
        """
        # get handler
        hdl = self.get_pseudoexp(identifier)

        # get dict with all seeds from handler
        d = hdl.get_injected_values()

        # check for param in dict
        if param in d:
            value = d[param]
        else:
            raise KeyError(f"No seed for {param} found, set manually!")

        # update class variable
        self.__injected[param] = value

    def update_injected(self, **kwargs):
        """
        Set injected parameter values
        """
        self.__injected.update(kwargs)

    def get_injected_value(self, param, pseudoexp_id=None):
        """
        get injected parameter value. If no value has been configured before,
        get value from the parameter seed from `pseudoexp_id`. Use first added
        pseudoexp if not specified

        Parameters
        ----------
        param : str
            parameter name
        identifier : str
            Pseudoexp identifier to get parameter seed from

        Returns
        -------
        injected_value : float
            injected paramter value
        """

        if param not in self.__injected:
            if pseudoexp_id is None:
                # use first configured pseudoexp
                self._set_injected_value_from_seed(
                    param, self.pseudoexp_list[0]
                )
            else:
                self._set_injected_value_from_seed(param, pseudoexp_id)

        return self.__injected[param]

    def set_param_order(self, order, allow_skip=False):
        """
        Set the order of parameters for the 1d plots, top left to bottom right

        Parameters
        ----------
        order : list
            List of ordered parameter names

        allow_skip : bool, optional
            Allow to skip a position by using an empty string
        """

        # check for invalid parameters
        for i, p in enumerate(order):
            if not p in self.all_params:
                if p == "" and allow_skip:
                    # assume the user intends to "skip" a position
                    continue
                else:
                    raise KeyError(f"Parameter {p} not found in any pseudoexp!")

            self.__param_order[p] = i

    def _set_default_param_order(self):
        """
        Set default parameter order for nrows=4 (hardcoded).
        """
        order = [
            'astro_norm', 'gamma_astro', 'conv_norm', 'prompt_norm' ,
            'barr_h'    , 'barr_w'     , 'barr_y'   , 'barr_z'      ,
            'CR_grad'   , 'delta_gamma', 'muon_norm', 'muongun_norm',
            'dom_eff'   , 'ice_abs'    , 'ice_scat' , 'ice_holep0'  ,
            'ice_holep1', 'ice_aniso'  , 'effective_veto'
        ]

        skip_counter = 0
        for i, p in enumerate(order):
            if not p in self.all_params:
                # skip if p not in any pseudoexp
                skip_counter += 1
                continue

            self.__param_order[p] = i - skip_counter

    def get_param_order(self):
        if not self.__param_order:
            self._set_default_param_order()

        return self.__param_order

    def set_1d_hist_bins(self, **kwargs):
        self.__1d_hist_bins.update(kwargs)

    def get_1d_hist_bins(self, param):
        if param in self.__1d_hist_bins:
            bins = self.__1d_hist_bins[param]
        else:
            bins = 10  # this is numpys default!
        return bins

    def _check_delta(self, delta):
        if not isinstance(delta, (list, tuple)) or len(delta) != 2:
            raise AssertionError(
                "Can only compare _two_ different pseudoexperiments! "
                "Provide a list or tuple of two identifiers!"
            )
        for identifier in delta:
            if not identifier in self.pseudoexp_list:
                raise KeyError(f"Pseudoeexp {identifier} not found!")

    def _get_param_deltas_df(self, pseudoexp0, pseudoexp1):
        # get dataframes of pseudoexp to compare
        hdl0 = self.get_pseudoexp(pseudoexp0)
        df0 = hdl0.get_pseudoexp_df()
        hdl1 = self.get_pseudoexp(pseudoexp1)
        df1 = hdl1.get_pseudoexp_df()

        # calculate delta
        df_deltas = df0 - df1

        # drop rows that contain at least one NaN, i.e. the pseudoexp were the
        # seeds differ
        df_deltas_cleaned = df_deltas.dropna()

        return df_deltas_cleaned

    def get_pseudoexp_graph(self, identifier):
        # get graph from dict (if present)
        graph = self.__graphs.get(identifier, None)

        # load graph if necessary
        if graph is None:
            # get pseudoexp handler
            pseudoexp_hdl = self.get_pseudoexp(identifier)

            # get graph file
            graph_file = os.path.join(
                pseudoexp_hdl.get_indir(), "Precalculated_Graph.pickle"
            )

            # load graph
            if os.path.isfile(graph_file):
                print("Reading precalculated graph...")
                graph = HistogramGraph.from_precalculated_file(graph_file)
                print("done!")
            else:
                raise FileNotFoundError("No precalculated graph found!")

            # add graph to dict
            self.__graphs[identifier] = graph

        return graph

    def plot_results_1d(
        self,
        delta=None,
        nrows=4,
        skip_pars=[],
        density_plots=False,
        add_legend=False,
        skip_injected=False,
        figsize=(8, 6),
        title=None,
        save=None,
        plot_dir=None,
    ):
        """
        Plot results of pseudo experiemnts: 1D distributions of all parameters.
        """

        if delta is not None:
            # check for plotting parameter delta
            self._check_delta(delta)

            # get df with parameter deltas
            df_deltas = self._get_param_deltas_df(delta[0], delta[1])

        # determine number of columns
        npars = len(self.all_params)
        npars -= len(skip_pars)
        ncols = npars//nrows
        if npars%nrows > 0:
            ncols += 1

        # create figure for 1d distributions
        fig, axs = plt.subplots(ncols, nrows, figsize=figsize)

        # check for figure title
        if title is not None:
            fig.suptitle(title)

        # loop all params
        for param in self.all_params:
            # skip parameters
            if param in skip_pars:
                continue

            # get ax for param
            pos = self.get_param_order()[param]
            if (ncols == 1) and (nrows == 1):
                ax = axs
            else:
                ax = axs[pos // nrows, pos % nrows]

            # plot either parameter results of the pseudoexp or
            # parameter deltas when comparing two pseudoexps
            if delta is None:
                # loop all pseudoexp
                for pseudoexp in self.pseudoexp_list:
                    # get pseudoexp hdl
                    pseudoexp_hdl = self.get_pseudoexp(pseudoexp)

                    # get parm hist and plot
                    hist, bins = pseudoexp_hdl.get_param_hist(
                        param,
                        density=density_plots,
                        bins=self.get_1d_hist_bins(param)
                    )

                    # get plot settings and plot
                    plot_settings = self.get_plot_settings(pseudoexp).copy()
                    ax.stairs(hist, edges=bins, **plot_settings)
            else:
                # get param delta values
                deltas = df_deltas[param].values

                # make hist of param delta
                hist, bins = np.histogram(
                    deltas,
                    density=density_plots,
                    bins=self.get_1d_hist_bins(param)
                )

                # plot hist of deltas
                ax.stairs(hist, edges=bins, color="k")

            # plot param injection value (only for not delta)
            if delta is None and not skip_injected:
                ax.axvline(
                    self.get_injected_value(param),
                    color='black',
                    linestyle='--',
                    label='injected'
                )

            # set xlabel
            ax.set_xlabel(param)

        # set ylabels
        if (ncols == 1) and (nrows == 1):
            if density_plots:
                plt.setp(axs, ylabel='pdf')
            else:
                plt.setp(axs, ylabel='N')
        else:
            if density_plots:
                plt.setp(axs[:, 0], ylabel='pdf')
            else:
                plt.setp(axs[:, 0], ylabel='N')

        if add_legend:
            # get legend handlers, labels from last axis and plot it once for the
            # figure
            if (ncols == 1) and (nrows == 1):
                ax_h = axs
            else:
                ax_h = axs[0, 0]
            handles, labels = ax_h.get_legend_handles_labels()
            fig.legend(
                handles,
                labels,
                loc='lower center',
                bbox_to_anchor=(0.5, 1.0),
                ncol=3
            )

        # plot and (optionally) save
        plt.tight_layout()
        if (save is not None) and (plot_dir is not None):
            savefig(fig, plot_dir, save)
        plt.show()

    @staticmethod
    def _plot_hist_x(ax, samples, bins, density=False, median_error=False, **plot_settings):
        # make hist and plot
        hist, error = make_hist_error(samples, bins=bins, normed=density)
        plot_hist_errorbar(ax, hist, bins, yerror=None, **plot_settings)

        # get color
        color = plot_settings["color"]

        if not median_error:
            # central 68%
            lower, upper = get_central_range(samples, q=0.68)
            label = "central 68%"
        else:
            lower, upper = get_bootstrapped_median_error(samples)
            label = "error on median"
        ax.axvspan(lower, upper, facecolor=color, alpha=0.2, label=label)
        # median
        ax.axvline(np.median(samples), color=color, ls="--",
                label="median")

    @staticmethod
    def _plot_hist_y(
        ax, samples, bins, density=False, median_error=False, **plot_settings
    ):
        # make hist and plot
        hist, error = make_hist_error(samples, bins=bins, normed=density)
        plot_hist_errorbar_T(ax, hist, bins, error=None, **plot_settings)

        # get color
        color = plot_settings["color"]

        if not median_error:
            # central 68%
            lower, upper = get_central_range(samples, q=0.68)
            label = "central 68%"
        else:
            lower, upper = get_bootstrapped_median_error(samples)
            label = "error on median"
        ax.axhspan(lower, upper, facecolor=color, alpha=0.2, label=label)

        # median
        ax.axhline(np.median(samples), color=color, ls="--", label="median")

    def plot_single_result_1d(
        self,
        param,
        delta=None,
        density_plot=False,
        add_legend=True,
        skip_injected=False,
        figsize=(8, 6),
        legend_loc=None,
        title=None,
        save=None,
        plot_dir=None,
    ):
        if delta is not None:
            # check for plotting parameter delta
            self._check_delta(delta)

            # get df with parameter deltas
            df_deltas = self._get_param_deltas_df(delta[0], delta[1])

        # create figure for 1d distributions
        fig, ax = plt.subplots(1, 1, figsize=figsize)

        # check for figure title
        if title is not None:
            fig.suptitle(title)

        # plot either parameter results of the pseudoexp or
        # parameter deltas when comparing two pseudoexps
        if delta is None:
            # loop all pseudoexp
            for pseudoexp in self.pseudoexp_list:
                # get pseudoexp hdl
                pseudoexp_hdl = self.get_pseudoexp(pseudoexp)

                # get parm hist and plot
                hist, bins = pseudoexp_hdl.get_param_hist(
                    param,
                    density=density_plot,
                    bins=self.get_1d_hist_bins(param)
                )

                # get plot settings and plot
                plot_settings = self.get_plot_settings(pseudoexp).copy()
                ax.stairs(hist, edges=bins, **plot_settings)
        else:
            # get param delta values
            deltas = df_deltas[param].values

            # make hist of param delta
            hist, bins = np.histogram(
                deltas,
                density=density_plot,
                bins=self.get_1d_hist_bins(param)
            )

            # plot hist of deltas
            ax.stairs(hist, edges=bins, color="k")

        # plot param injection value (only for not delta)
        if delta is None and not skip_injected:
            ax.axvline(
                self.get_injected_value(param),
                color='black',
                linestyle='--',
                label='injected'
            )

        # set xlabel
        ax.set_xlabel(param)

        # set ylabels
        ax.set_ylabel('pdf') if density_plot else ax.set_ylabel('N')

        if add_legend:
            ax.legend(loc=legend_loc)
            # handles, labels = ax.get_legend_handles_labels()
            # ax.legend(
            #     handles,
            #     labels,
            #     # loc='lower center',
            #     # bbox_to_anchor=(0.5, 1.0),
            #     # ncol=3
            # )

        # plot and (optionally) save
        plt.tight_layout()
        if (save is not None) and (plot_dir is not None):
            savefig(fig, plot_dir, save)
        plt.show()

    def plot_results_2d(
        self,
        param_x="gamma_astro",
        param_y="astro_norm",
        delta=None,
        figsize=(8, 6),
        xlim=(1.6, 2.8),
        ylim=(0.0, 2.2),
        include_1d_projections=True,
        median_error_in_1d=False,
        indicate_injected_values=True,
        legend_ncols=None,
        nbinsx=13,
        nbinsy=13,
        density_plots=False,
        title=None,
        save=None,
        plot_dir=None,
    ):
        # check for delta given
        if delta is not None:
            # check for plotting parameter delta
            self._check_delta(delta)

            # get df with parameter deltas
            df_deltas = self._get_param_deltas_df(delta[0], delta[1])


        # setup figure
        fig, (ax) = plt.subplots(1, 1, figsize=figsize)

        # check for figure title
        if title is not None:
            fig.suptitle(title)

        # setup axes for 1d projections
        if include_1d_projections:
            divider = make_axes_locatable(ax)
            axt = divider.append_axes("top",   size=2.0, pad=0.0, sharex=ax)
            axr = divider.append_axes("right", size=2.0, pad=0.0, sharey=ax)

        if indicate_injected_values:
            # get injected values
            x_injected = self.get_injected_value(param_x)
            y_injected = self.get_injected_value(param_y)

        def draw_data(x, y, xlim, ylim, plot_settings, incl_1d):
            # make optional 1d plots first
            if include_1d_projections:
                # param_x hist
                bins = np.linspace(xlim[0], xlim[1], nbinsx)
                self._plot_hist_x(
                    axt, x, bins, density=density_plots,
                    median_error=median_error_in_1d,
                    **plot_settings
                )

                # param_y hist
                bins = np.linspace(ylim[0], ylim[1], nbinsy)
                self._plot_hist_y(
                    axr, y, bins, density=density_plots,
                    median_error=median_error_in_1d,
                    **plot_settings
                )

            # update some plot settings before the scatter plot
            plot_settings.update(marker="o", alpha=0.5)

            # main scatter plot
            ax.scatter(x, y, **plot_settings)

        # plot either parameter results of the pseudoexp or
        # parameter deltas when comparing two pseudoexps
        if delta is None:
            # loop all pseudoexp
            for pseudoexp in self.pseudoexp_list:
                # get pseudoexp hdl and plot settings
                pseudoexp_hdl = self.get_pseudoexp(pseudoexp)
                plot_settings = self.get_plot_settings(pseudoexp).copy()

                # get x and y from pseudoexp dataframe
                df = pseudoexp_hdl.get_pseudoexp_df()
                x = df[param_x].values
                y = df[param_y].values

                # draw scatter points and (optional) 1d hists
                draw_data(
                    x, y, xlim, ylim, plot_settings, include_1d_projections
                )

        else:
            # get param_x and param_y delta values
            x = df_deltas[param_x].values
            y = df_deltas[param_y].values

            # set plot_settings
            plot_settings = dict(
                color="k",
                label=f"({self.get_plot_settings(delta[0])['label']}) - "
                      f"({self.get_plot_settings(delta[1])['label']})"
            )

            # draw scatter points and (optional) 1d hists
            draw_data(
                x, y, xlim, ylim, plot_settings, include_1d_projections
            )

        # main plot injections, labels, legend, limits
        if param_x == "gamma_astro":
            xlabel = r'$\gamma_{\rm{astro}}$'
        if param_y == "astro_norm":
            ylabel = r'$\Phi^{\mathrm{astro}}_{\mathrm{0}}$ $\rm{[10^{-18} GeV^{-1} cm^{-2} s^{-1} sr^{-1}]}$'
        if not delta and indicate_injected_values:
            # for delta plot, injected values cannot be used
            ax.axvline(
                x_injected, color="k", alpha=0.75, label="injected"
            )
            ax.axhline(y_injected, color="k", alpha=0.5)
        if delta:
            xlabel = r"$\Delta$ " + xlabel
            ylabel = r"$\Delta$ " + ylabel
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        if legend_ncols is None:
            legend_ncols = len(self.pseudoexp_list)+1
        ax.legend(ncols=legend_ncols)

        # 1d plot injections, labels, legend, limits
        if include_1d_projections:
            if not delta and indicate_injected_values:
                axt.axvline(x_injected, color="k", alpha=0.75)
                axr.axhline(y_injected, color="k", alpha=0.75)
            if density_plots:
                axt.set_ylabel(r"pdf")
                axr.set_xlabel(r"pdf")
            else:
                axt.set_ylabel(r"N")
                axr.set_xlabel(r"N")
            # make some labels invisible
            plt.setp(
                axt.get_xticklabels() + axr.get_yticklabels(), visible=False
            )
            # axt.legend()

        # plot and (optionally) save
        plt.tight_layout()
        if (save is not None) and (plot_dir is not None):
            savefig(fig, plot_dir, save)
        plt.show()

    def get_TS_values(
        self, identifier, llh_type=None, say_sat_llh_type="poisson",det_config=None,
        calculate_marginalTS = False,
        marginalTS_variable = None,
    ):
        """
        Get the test statistics values for the pseudoexperiments

        Parameters
        ----------
        llh_type : str, optional
            Likelihood used for fitting the pseudoexperiments. If None, will try
            to obtain the used LLH form the config if possible, by default None
        say_sat_llh_type : str, optional
            Saturated Likelihood type to assume when the SAY Likelihood was used
            during fitting. Choose from `poisson, say, say_simple`, defaults to
            "poisson"

        Returns
        -------
        ts : numpy.array
            array with the TS values
        """
        # get pseudoexp handler
        pseudoexp_hdl = self.get_pseudoexp(identifier)

        # get llh_type
        if llh_type is None:
            config_hdl = pseudoexp_hdl.get_pseudoexp_config()
            config_dict = config_hdl.to_dict()
            llh_type = config_dict["analysis"]["llh"][:-3].lower()

        # get llh values
        llh = pseudoexp_hdl.get_param_results("llh").astype(float)

        # "convert" llh to TS
        if llh_type.lower() == "poisson":
            # in NNMFit, the Poisson LLH has saturated term already
            # substracted by default. Only multiply by 2 to get TS
            ts = 2.0 * llh
        elif llh_type.lower() == "say":
            # substract saturated term if SAY LLH has beed used

            # start empty list for saturated Likelihood values
            sat_llh = []

            # get pseudoexp seeds for iterating
            seeds = pseudoexp_hdl.get_pseudoexp_seeds()

            # get df
            df = pseudoexp_hdl.get_pseudoexp_df()
            
                
            # First: check for saturated LLH type to use
            if say_sat_llh_type == 'poisson':
                # use the saturated LLH from the Poisson LLH log(Poisson(n,n))
                # i.e. choosing ssq=0

                # loop all pseudoexp
                
                for seed in seeds:
                    # get pseudo-datacounts dict (det_configs)
                    d = pseudoexp_hdl.get_datahist(seed)

                    # start with 0
                    temp = 0.0
                    
                    # loop all detector configs
                    
                    for det_conf, datahist in d.items():
                        if det_config is not None:
                            print(f'per detector config GOF requested,for {det_config}')
                            if det_conf==det_config:
                                
                                if calculate_marginalTS:
                                    print(f'1D marginal GOF requested, for {det_config} and for variable                                                                  {marginalTS_variable}')
                                    
                                    if det_conf=='IC86_pass2_SnowStorm_v2_Bfr_DoubleCascades':
                                            print(f'Calculating GOF for detcteor config {det_conf} for variable {marginalTS_variable}')
                                            k = calculate_marginalTS_double(variable = marginalTS_variable,
                                                                                      dataset=datahist)
                                            temp += np.sum(
                                                binwise_saturated_poisson_llh(np.array(k)))
                                    elif det_conf=='IC86_pass2_SnowStorm_v2_Bfr_Cascades':
                                            print(f'Calculating GOF for detcteor config {det_conf} for variable {marginalTS_variable}')
                                            k = calculate_marginalTS_nondouble(variable = marginalTS_variable,
                                                                                      dataset=datahist)
                                            temp += np.sum(
                                                binwise_saturated_poisson_llh(np.array(k)))
                                    elif det_conf=='IC86_pass2_SnowStorm_v2_Bfr_Tracks':
                                            print(f'Calculating GOF for detcteor config {det_conf} for variable {marginalTS_variable}')
                                            k = calculate_marginalTS_nondouble(variable = marginalTS_variable,
                                                                                      dataset=datahist)
                                            temp += np.sum(
                                                binwise_saturated_poisson_llh(np.array(k)))
                                    
                                        
                                else:
                                    print(f'---Calculating GOF for detcteor config {det_conf}---')
                                    temp += np.sum(binwise_saturated_poisson_llh(datahist))
                            else:
                                
                                continue
                        else:
                            print('Calculating overall GOF')
                            temp += np.sum(binwise_saturated_poisson_llh(datahist))

                    # append to sat_llh list
                    sat_llh.append(temp)
            elif say_sat_llh_type in ["say", "say_simple"]:
                # get graph
                graph = self.get_pseudoexp_graph(identifier)

                # loop all pseudoexp
                for seed in seeds:
                    print(f"working on seed {seed}...")

                    # get pseudo-datacounts dict (det_configs)
                    d = pseudoexp_hdl.get_datahist(seed)

                    # start with 0
                    temp = 0.0

                    # evaluate graph with best fit parameters for each det conf
                    for det_conf, datahist in d.items():
                        if det_config is not None:
                            if det_config==det_conf:
                                
                                # get pseudoexp result
                                bestfit_params = df.loc[seed].to_dict()

                                # get pseudoexp bestfit spectrum
                                res = graph.get_evaled_histogram(
                                    det_config=det_conf,
                                    input_variables=bestfit_params,
                                    reshape=False
                                )

                                print(f"got res for det_conf {det_conf}, ", end="")

                                for i, mu in enumerate(res['mu']):
                                    temp += binwise_saturated_llh(
                                        datahist[i], mu, res['ssq'][i], say_sat_llh_type
                                    )
                        else:
                            
                            bestfit_params = df.loc[seed].to_dict()

                            # get pseudoexp bestfit spectrum
                            res = graph.get_evaled_histogram(
                                det_config=det_conf,
                                input_variables=bestfit_params,
                                reshape=False
                            )

                            print(f"got res for det_conf {det_conf}, ", end="")

                            for i, mu in enumerate(res['mu']):
                                temp += binwise_saturated_llh(
                                    datahist[i], mu, res['ssq'][i], say_sat_llh_type
                                )

                    sat_llh.append(temp)
            else:
                raise NotImplementedError()

            # calculate TS, note that llh is already -Log(likelihood value)!
            ts = 2.0 * (llh + sat_llh)
        else:
            raise AssertionError(f"llh_type must be poisson or say!")

        return ts

    def plot_TS(
        self,
        llh_type='poisson',
        say_sat_llh_type='poisson',
        # override_injected={},
        # graph_name="Precalculated_Graph.pickle",
        fit_chi2=True,
        ax=None,
        title=None,
        save=None,
        plot_dir=None,
        data_TS=None,
        det_config=None,
        calculate_marginalTS = False,
        marginalTS_variable = None,
        subtitle = None
    ):
        # initialize figure
        #fig, ax = plt.subplots(figsize=figsize)
        
        font_axis_label = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 22,
        }
        font_title = {'family': 'serif',
                'color':  'black',
                'weight': 'bold',
                'size': 20,
                }
        font_legend = font_manager.FontProperties(family='serif',
                                           weight='normal',
                                           style='normal', size=15)
                # check for figure title
        if title is not None:
            plt.title(title,fontdict=font_title)

        # loop all pseudoexp
        for pseudoexp in self.pseudoexp_list:
            # get plot settings
            plot_settings = self.get_plot_settings(pseudoexp).copy()
            color = plot_settings["color"]

            # get TS
            ts = self.get_TS_values(
                pseudoexp, llh_type=llh_type, say_sat_llh_type=say_sat_llh_type,det_config=det_config,
                calculate_marginalTS = calculate_marginalTS,marginalTS_variable = marginalTS_variable,
            )

            # plot TS distribution
            hist, bins, _ = ax.hist(
                ts,
                bins=30,
                density=True,
                alpha=0.5,
                **plot_settings,
                # label=f"{len(ts)} pseudoexperiments",
            )

            # plot distribution error
            # TODO: make this more versatile for arbitrary binnings
            norm = (len(ts) * (bins[1] - bins[0]))
            bin_centers = bins[:-1] + 0.5 * (bins[1:] - bins[:-1])
            # error on normalized histogram count h^i:
            # d_h^i = sqrt(h^i) / sqrt(norm)
            ax.errorbar(
                bin_centers,
                hist,
                yerr=np.sqrt(hist) / np.sqrt(norm),
                linestyle='None',
                color=color
            )
            print('minimum of ts = {0} \nmaximum of ts = {1}'.format(min(ts),max(ts)))
            print('median of ts = {0}'.format(np.median(ts)))
            # optinal: fit chi2 (and plot)
            if fit_chi2:
                chi2_fit = chi2.fit(ts, floc=0.0, fscale=1.0)

                # plot chi2 fit
                rv = chi2(chi2_fit[0])
                x = np.linspace(min(ts),max(ts))

                ax.plot(
                    x,
                    rv.pdf(x),
                    color='orange',linewidth=2,
                    label=f"chi^2 (k={chi2_fit[0]:.2f}) pdf"
                )

            if data_TS is not None:
                # make label
                label = f"data_TS = {data_TS:.2f}"

                # calculate pvalue if chi2 fit
                if fit_chi2:
                    p = chi2.sf(x=data_TS, df=chi2_fit[0])
                    p = p*100
                    label += f" (p={p:.2f}%)"

                # plot as vline
                ax.axvline(data_TS, color="k", ls="--", label=label)

        # plot labels, legends, etc
        ax.set_xlabel(r'$-2 \mathrm{log}(\Lambda_\mathrm{sat})$',fontdict=font_axis_label)
        ax.set_ylabel('pdf',fontdict=font_axis_label)
        if subtitle is not None:
            ax.set_title(subtitle,fontdict=font_title)
        ax.legend(ncols=len(self.pseudoexp_list),prop=font_legend)
        ax.set_xlim(min(ts)-10,320)
#         for item in (ax.get_xticklabels() + ax.get_yticklabels()):
#             item.set_subfontsize(14)
# #             item.set_family('serif')
#         ax.tick_params(axis='both',which='major',width=3,length=15,direction='in')
#         ax.tick_params(axis='both',which='minor',width=1,length=8,direction='in')
        # plot and (optionally) save
#         plt.tight_layout()
#         if (save is not None) and (plot_dir is not None):
#             savefig(fig, plot_dir, save)
#         plt.show()

    def twosample_ks_test(self, pseudoexp_list, param):
        """
        Run scipy's two-sample KS test for the 1D distribution
        of a parameter, comparing two pseudoexps

        Parameters
        ----------
        pseudoexp_list : list
            conatining the name of the two pseudoexps to be compared
        param : str
            name of the parameter for which to run the KS test

        Returns
        -------
        KstestResult
            result of scipy's two-sample KS test
        """

        assert len(pseudoexp_list) == 2, 'can only compare two pseudoexp'

        hists = []

        for pseudoexp in pseudoexp_list:
            hist, _ = self.get_pseudoexp(pseudoexp).get_param_hist(
                param, density=True, bins=self.get_1d_hist_bins(param)
            )
            hists.append(hist)

        res = ks_2samp(hists[0], hists[1])

        return res


# # TODO:
# def plot_pull_map(
#     pseudoexp_hdl,
#     graph,
#     det_conf=None,
#     square_pull=False,
#     include_mc_sigma=False,
#     cmap_name="coolwarm",
#     vmax=None,
#     plot_1d=False,
#     nBins_1d=21,
#     acceptance_range={},
#     unused_pars=['muongun_norm', 'effective_veto'],
#     plot_title=None,
#     save=None,
#     plot_dir=None,
# ):

#     # read pseudoexp results if necessary
#     if isinstance(pseudoexp_result, str):
#         pseudoexp_result = read_pseudoexp(
#             pseudoexp_result, acceptance_range, unused_pars
#         )

#     # get binning
#     temp = graph.get_binning()
#     bins_energy = temp["reco_energy"]
#     bins_zenith = temp["reco_zenith"]
#     shape = (len(bins_energy) - 1, len(bins_zenith) - 1)

#     # get det_conf
#     if det_conf is None:
#         det_conf = graph.get_detconfig()

#     # get (pseude)data and reshape
#     data = pseudoexp_result["datahists"][0][det_conf].reshape(shape)

#     # pseudoexp bestfit
#     res = graph.get_evaled_histogram(
#         det_config=det_conf,
#         input_variables=pseudoexp_result["fit_result_single"],
#         reshape=True
#     )
#     mc = res["mu"]
#     mc_yerror = np.sqrt(res["ssq"])

#     plot_pulls(data, mc, mc_yerror, bins_energy, bins_zenith,
#                square_pull=square_pull, include_mc_sigma=include_mc_sigma, cmap_name=cmap_name,
#                vmax=vmax, plot_1d=plot_1d, nBins_1d=nBins_1d, plot_title=plot_title,
#                save=save, plot_dir=plot_dir)

# # TODO:
# def plot_1D_projected_data_MC(
#     pseudoexp_result,
#     graph,
#     det_conf=None,
#     acceptance_range={},
#     unused_pars=['muongun_norm', 'effective_veto'],
#     save=None,
#     plot_dir=None,):

#     # read pseudoexp results if necessary
#     if isinstance(pseudoexp_result, str):
#         pseudoexp_result = read_pseudoexp(
#             pseudoexp_result, acceptance_range, unused_pars
#         )

#     # get binning
#     temp = graph.get_binning()
#     bins_energy = temp["reco_energy"]
#     bins_zenith = temp["reco_zenith"]
#     shape = (len(bins_energy) - 1, len(bins_zenith) - 1)

#     # get det_conf
#     if det_conf is None:
#         det_conf = graph.get_detconfig()

#     # get (pseude)data and reshape
#     data = pseudoexp_result["datahists"][0][det_conf].reshape(shape)

#     # pseudoexp bestfit
#     res = graph.get_evaled_histogram(
#         det_config=det_conf,
#         input_variables=pseudoexp_result["fit_result_single"],
#         reshape=True
#     )

#     plot_energy_and_zenith_data_MC(
#         res["mu"],
#         res["ssq"],
#         data,
#         bins_energy,
#         bins_zenith,
#         plot_dir=plot_dir,
#         save=save
#     )
