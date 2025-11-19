import numpy as np
import matplotlib.pyplot as plt
from common import calculator # tianlu
import tables, os

slc = np.s_[:]
colors = ["C0","C3","C2","C1"]

def plot_median_quartiles( hdf_file_paths, plot_dicts, plotting_main_path = "", plot_quartiles = True ):

    plt.figure(figsize=(6, 4))

    if plotting_main_path != "": os.system(f"mkdir -p {plotting_main_path}")

    for i, (hdf_file_path, plot_dict) in enumerate(zip(hdf_file_paths, plot_dicts)):

        hdf_file = tables.open_file( hdf_file_path )

        reco_table_y = hdf_file.get_node(f'/{plot_dict["reco_key_y"]}')
        true_table_y = hdf_file.get_node(f'/{plot_dict["true_key_y"]}')
        table_x = hdf_file.get_node(f'/{plot_dict["key_x"]}')

        if plot_dict["reco_var_key_y"] == "direction":
            azi_reco = reco_table_y.read(field="azimuth")   
            zen_reco = reco_table_y.read(field="zenith")
            if plot_dict["true_key_y"] == "TrueAzimuth":
                azi_true = hdf_file.root.TrueAzimuth[slc]['value']
                zen_true = hdf_file.root.TrueZenith[slc]['value']
            else:   
                azi_true = true_table_y.read(field="azimuth")   
                zen_true = true_table_y.read(field="zenith")   
            deltas = np.degrees(calculator.center_angle( zen_true, azi_true, zen_reco, azi_reco))
        elif plot_dict["reco_var_key_y"] == "easym":
            if "EventGenerator" not in plot_dict["reco_key_y"]:
                easym_reco = get_easym( hdf_file.get_node(f'/{plot_dict["reco_key_y"]}Particles') )
            else:
                easym_reco = get_easymm_evtgen( hdf_file.get_node(f'/{plot_dict["reco_key_y"]}') )
            easym_true = true_table_y.read(field=plot_dict["true_var_key_y"])   
            deltas = easym_reco - easym_true
        else:
            y_reco = reco_table_y.read(field=plot_dict["reco_var_key_y"]) if plot_dict["reco_var_key_y"] != "cascade_cascade_00001_distance" else abs(reco_table_y.read(field=plot_dict["reco_var_key_y"])) 
            y_true = true_table_y.read(field=plot_dict["true_var_key_y"]) 
            deltas = (y_reco-y_true)/y_true if plot_dict["normalize"] else y_reco-y_true

        x = table_x.read(field=plot_dict["variable_key_x"])

        bins = plot_dict["bins"]
        label = plot_dict["label"] if "label" in plot_dict else ""
        color = colors[i]

        plot_quartiles_vs_x( deltas, x, bins, label, color, plot_quartiles = plot_quartiles )
        hdf_file.close()

    if len(hdf_file_paths) > 1: plt.legend(loc="best")
    plt.xscale( plot_dicts[0]["xscale"] )
    plt.ylim( plot_dicts[0]["ylim"] )
    plt.xlabel( plot_dicts[0]["xlabel"] )
    plt.ylabel( plot_dicts[0]["ylabel"] )
    plt.axhline(y=0.0, color='gray', linestyle='--', linewidth=1)
    plt.savefig(f'{plotting_main_path}/{plot_dicts[0]["name"]}.png', bbox_inches='tight')


def get_easym(node):
    _es = node.cols.energy[:]
    _vs = node.cols.vector_index[:]
    _e1 = _es[_vs==0]
    _e2 = _es[_vs==1]
    return (_e1 - _e2) / (_e1 + _e2)

def get_easymm_evtgen(node):
    _e1 = node.cols.cascade_energy[:]
    _e2 = node.cols.cascade_cascade_00001_energy[:]
    return (_e1 - _e2) / (_e1 + _e2)

def plot_quartiles_vs_x(deltas, lge_tru, lge_bins, label, color, plot_quartiles = True):
    if np.any(np.isnan(deltas)):
        print(
            f'WARN: {len(deltas[np.isnan(deltas)])} nan events. Ignored in quartiles.')
    lge_i = np.digitize(lge_tru, lge_bins)
    digitized_deltas = [deltas[lge_i == ei] for ei in range(1, lge_bins.size)]

    per50 = [np.nanmedian(ca) for ca in digitized_deltas]
    per25 = [np.nanpercentile(ca, 25) if len(
        ca) > 0 else np.nan for ca in digitized_deltas]
    per75 = [np.nanpercentile(ca, 75) if len(
        ca) > 0 else np.nan for ca in digitized_deltas]
    if plot_quartiles:
        plt.plot(calculator.centers(lge_bins), per50, label=label+' quartiles', color=color)
        plt.fill_between(calculator.centers(lge_bins), per25, per75, alpha=0.5, color=color)
    else:
        plt.plot(calculator.centers(lge_bins), per50, label=label+' median', color=color)
        # plt.plot(calculator.centers(lge_bins), (np.array(per75)-np.array(per25))/2, "--",label=label+' (q75-q25)/2', color=color)
    return per25, per50, per75