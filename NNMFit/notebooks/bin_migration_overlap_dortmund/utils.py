import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

x_labels = {
    "reco_energy" : r"Reco $E_{\rm dep}$ [GeV]",
    "reco_length" : r"Reco $L_{\tau}$ [m]",
    "reco_zenith" : r"Reco $\theta$ [rad]",
    "reco_dir" : r"Reco $\theta$ [rad]",
    "bdt_product" : "BDT score 1 x BDT score 2",
    "bdt_scores1" : "BDT score 1",
    "bdt_scores2" : "BDT score 2",
}

def get_event_rates(hist_graph_hdl, det_config, input_variables):
    results = {}

    for input_name, input_variable in input_variables.items():

        res = hist_graph_hdl.get_evaled_histogram(
            input_variables=input_variable,
            det_config=det_config,
            reshape=True,
        )

        rate = np.sum(res["mu"])
        error = np.sqrt(np.sum(res["ssq"]))

        results[input_name] = {
            "rate": rate,
            "error": error,
        }

    return results


def plot_histogram_annotate_selection(
    hist_graph_hdl,
    det_config,
    input_variables,
    cuts=None,
    ylog=None,
    title=None,
    savepath=None,
):

    import numpy as np
    import matplotlib.pyplot as plt

    print(det_config)

    binnings = hist_graph_hdl.get_binning(det_config=det_config)

    fig, axes = plt.subplots(
        1,
        len(binnings),
        figsize=(len(binnings) * 5, 4)
    )

    if len(binnings) == 1:
        axes = [axes]

    variable_names = list(binnings.keys())

    for input_name, input_variable in input_variables.items():

        # ============================================================
        # Full model evaluation
        # ============================================================

        res = hist_graph_hdl.get_evaled_histogram(
            input_variables=input_variable,
            det_config=det_config,
            reshape=True
        )

        # ============================================================
        # NuTau-only evaluation
        # ============================================================
        input_variable_nutau = input_variable.copy()
        input_variable_nutau["a"] = 0.0
        input_variable_nutau["b"] = 0.0
        input_variable_nutau["total_astro_norm"] = input_variable["total_astro_norm"] / 3.0
        input_variable_nutau["conv_norm"] = 0
        input_variable_nutau["prompt_norm"] = 0

        res_nutau = hist_graph_hdl.get_evaled_histogram(
            input_variables=input_variable_nutau,
            det_config=det_config,
            reshape=True
        )

        # ============================================================
        # Selection mask + yields
        # ============================================================
        selected_mu = None
        selected_err = None
        selected_mu_nutau = None

        if cuts is not None:

            mask = np.ones(res["mu"].shape, dtype=bool)

            for axis, variable_name in enumerate(variable_names):

                if variable_name not in cuts:
                    continue

                low, high = cuts[variable_name]

                binning = binnings[variable_name]
                centers = 0.5 * (binning[:-1] + binning[1:])

                axis_mask = (centers >= low) & (centers < high)

                reshape_dims = [1] * res["mu"].ndim
                reshape_dims[axis] = len(axis_mask)

                mask &= axis_mask.reshape(reshape_dims)

            selected_mu = res["mu"][mask].sum()
            selected_err = np.sqrt(res["ssq"][mask].sum())

            selected_mu_nutau = res_nutau["mu"][mask].sum()

        # ============================================================
        # Plot projections
        # ============================================================
        for i, (variable_name, binning) in enumerate(binnings.items()):

            sum_axes = tuple(
                ax for ax in range(res["mu"].ndim)
                if ax != i
            )

            hist = res["mu"].sum(axis=sum_axes)
            yerror = np.sqrt(res["ssq"].sum(axis=sum_axes))

            # ========================================================
            # Legend logic per panel
            # ========================================================
            if i == 0:
                # total events
                label = f"{input_name} : {hist.sum():.2f} ± {yerror.sum():.2f}"

            elif i == 1 and cuts is not None:
                # selected events
                label = f"{selected_mu:.2f} ± {selected_err:.2f}"

            elif i == 2 and cuts is not None:
                # NuTau yield + purity
                if selected_mu > 0:
                    nutau_fraction = selected_mu_nutau / selected_mu
                else:
                    nutau_fraction = 0.0

                label = (
                    f"NuTau: {selected_mu_nutau:.2f}\n"
                    f"Purity: {100.0 * nutau_fraction:.1f}%"
                )

            else:
                label = None

            axes[i].stairs(
                hist,
                binning,
                label=label
            )

            axes[i].fill_between(
                binning,
                np.r_[hist - yerror, (hist - yerror)[-1]],
                np.r_[hist + yerror, (hist + yerror)[-1]],
                step="post",
                alpha=0.4
            )

            axes[i].set_xlabel(x_labels[variable_name])

            axes[i].set_ylabel(
                f"Rate / "
                f"{hist_graph_hdl.get_livetime(det_config)/(3600*24*365.25):.2f} yr"
            )

            axes[i].set_xlim(min(binning), max(binning))

            if ylog:
                axes[i].set_yscale("log")

            if "energy" in variable_name or "length" in variable_name:
                axes[i].set_xscale("log")

    # ================================================================
    # Legends
    # ================================================================
    axes[0].legend(title="All events")

    if "reco_length" in cuts:
        low, high = cuts["reco_length"]
        axes[0].axvline(low, color="red")

    if "bdt_scores1" in cuts and len(axes) > 1:
        low, high = cuts["bdt_scores1"]
        axes[1].axvline(low, color="red")
        axes[1].legend(title="Selected double\ncascade events")

    if "bdt_scores2" in cuts and len(axes) > 2:
        low, high = cuts["bdt_scores2"]
        axes[2].axvline(low, color="red")
        # axes[2].legend(title="NuTau composition")

    # ================================================================
    # Final layout
    # ================================================================
    plt.suptitle(det_config if title is None else title)

    plt.tight_layout()

    if savepath:
        plt.savefig(savepath)

    plt.show()


def plot_histogram_annotate_selection_flavor(
    hist_graph_hdl,
    det_config,
    input_variables,
    cuts=None,
    ylog=None,
    title=None,
    savepath=None,
):

    import numpy as np
    import matplotlib.pyplot as plt

    print(det_config)

    binnings = hist_graph_hdl.get_binning(det_config=det_config)
    variable_names = list(binnings.keys())

    fig, axes = plt.subplots(
        3,  # flavors
        len(binnings),
        figsize=(len(binnings) * 5, 12)
    )

    if len(binnings) == 1:
        axes = axes.reshape(3, 1)

    flavor_names = ["NuE", "NuMu", "NuTau"]

    # ================================================================
    # LOOP OVER FLAVORS (ROWS)
    # ================================================================
    for row, flavor in enumerate(flavor_names):

        for input_name, input_variable in input_variables.items():

            # ------------------------------------------------------------
            # Build flavor hypothesis
            # ------------------------------------------------------------
            input_var_flavor = input_variable.copy()

            # kill atmospheric components (as before)
            input_var_flavor["conv_norm"] = 0.0
            input_var_flavor["prompt_norm"] = 0.0

            input_var_flavor["total_astro_norm"] = (
                input_variable["total_astro_norm"] / 3.0
            )

            # ------------------------------------------------------------
            # NEW FLAVOR MAPPING
            # ------------------------------------------------------------
            if flavor == "NuE":
                input_var_flavor["a"] = 1.0
                input_var_flavor["b"] = 1.0

            elif flavor == "NuMu":
                input_var_flavor["a"] = 1.0
                input_var_flavor["b"] = -1.0

            elif flavor == "NuTau":
                input_var_flavor["a"] = 0.0
                input_var_flavor["b"] = 0.0

            # ------------------------------------------------------------
            # Evaluate histogram
            # ------------------------------------------------------------
            res = hist_graph_hdl.get_evaled_histogram(
                input_variables=input_var_flavor,
                det_config=det_config,
                reshape=True
            )

            # ------------------------------------------------------------
            # Selection mask
            # ------------------------------------------------------------
            selected_mu = None
            selected_err = None

            if cuts is not None:

                mask = np.ones(res["mu"].shape, dtype=bool)

                for axis, variable_name in enumerate(variable_names):

                    if variable_name not in cuts:
                        continue

                    low, high = cuts[variable_name]

                    binning = binnings[variable_name]
                    centers = 0.5 * (binning[:-1] + binning[1:])

                    axis_mask = (centers >= low) & (centers < high)

                    reshape_dims = [1] * res["mu"].ndim
                    reshape_dims[axis] = len(axis_mask)

                    mask &= axis_mask.reshape(reshape_dims)

                selected_mu = res["mu"][mask].sum()
                selected_err = np.sqrt(res["ssq"][mask].sum())

            # ------------------------------------------------------------
            # LOOP OVER COLUMNS
            # ------------------------------------------------------------
            for i, (variable_name, binning) in enumerate(binnings.items()):

                sum_axes = tuple(
                    ax for ax in range(res["mu"].ndim)
                    if ax != i
                )

                hist = res["mu"].sum(axis=sum_axes)
                yerror = np.sqrt(res["ssq"].sum(axis=sum_axes))

                # --------------------------------------------------------
                # LABELS
                # --------------------------------------------------------
                if i == 0:
                    label = f"{input_name} : {hist.sum():.2f} ± {yerror.sum():.2f}"
                else:
                    label = None  # ONLY LEFT COLUMN HAS LEGENDS

                axes[row, i].stairs(
                    hist,
                    binning,
                    label=label
                )

                axes[row, i].fill_between(
                    binning,
                    np.r_[hist - yerror, (hist - yerror)[-1]],
                    np.r_[hist + yerror, (hist + yerror)[-1]],
                    step="post",
                    alpha=0.4
                )

                axes[row, i].set_xlim(min(binning), max(binning))

                if ylog:
                    axes[row, i].set_yscale("log")

                if "energy" in variable_name or "length" in variable_name:
                    axes[row, i].set_xscale("log")

                # column titles only once
                if row == 0:
                    axes[row, i].set_title(x_labels[variable_name])

        # end input loop

    # ================================================================
    # ROW LABELS (FLAVORS)
    # ================================================================
    for r, flavor in enumerate(flavor_names):
        axes[r, 0].set_ylabel(
                f"Astro {flavor} Rate / "
                f"{hist_graph_hdl.get_livetime(det_config)/(3600*24*365.25):.2f} yr"
            )


    # ================================================================
    # LEGENDS (ONLY LEFT COLUMN)
    # ================================================================
    for r in range(3):
        axes[r, 0].legend(title="Total events")

    # ================================================================
    # FINAL FORMATTING
    # ================================================================
    plt.suptitle(det_config if title is None else title)

    plt.tight_layout()

    if savepath:
        plt.savefig(savepath)

    plt.show()