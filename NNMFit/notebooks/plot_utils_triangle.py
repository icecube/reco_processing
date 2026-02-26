
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as font_manager

rcParams = {"axes.titlesize": 16,"axes.labelsize": 14,"xtick.labelsize": 14,"ytick.labelsize": 14}
mpl.rcParams.update(rcParams)
font_axis_label = {'family': 'serif','color':  'black','weight': 'normal','size': 22}
font_title = {'family': 'serif','color':  'black','weight': 'bold','size': 20}
font_legend = font_manager.FontProperties(family='serif',weight='normal',style='normal', size=13)

# triangle plotting settings
from Ternary import flavor_triangle
plt.rcParams["figure.figsize"] = (6,6)
plt.rcParams.update({'font.family':'serif'})

ts_dict = {
    '68%' : 2.37,
    '90%' : 4.605,
    '95%' : 5.99,
}

colours = ["black","C0","C3","C2", "C1", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11"]
linestyles = ["-","--",":"]

def compare_contours( data, names, labels, levels = ['68%'], title = r"HESE: $\phi_0 = 2.12,\gamma=2.87$", savepath = None ):

    # helper functions
    C = {} # needed for area comparison!

    fig = plt.figure()
    tax = flavor_triangle()

    lh, ll = [], []

    asimov = tax.ca.scatter([1.0/3], [1.0/3], marker='*', facecolor='black',
                    edgecolor='k', lw=0.5, s=80)
    lh.append(asimov)
    ll.append('Asimov: 1:1:1')

    fmt={} # set labels to the contours

    ts_values = [ts_dict[i] for i in levels]

    for i,name in enumerate(names):
        C[name] = tax.ca.contour(data[name]["ft_grid_asimov_poisson"],
                                data[name]["fe_grid_asimov_poisson"],
                                data[name]["ts_grid_asimov_poisson"], 
                                ts_values,
                                linestyles=linestyles[:len(levels)],
                                linewidths=1.5,
                                colors=colours[i])
        
        h, _ = C[name].legend_elements()
        lh.append(h[0]) # legend elements
        ll.append(labels[i])

        # add ts levels in plot
        if i == len(names) - 1:
            for l, s in zip(C[name].levels, levels):
                fmt[l] = s
            plt.clabel(C[name],ts_values,inline=True,fontsize=12.,
                    fmt=fmt,colors='black')

    l = fig.legend(lh,ll,
                    bbox_to_anchor=(0.7, 0.05),prop=font_legend,
                    ncols=1 if len(names) < 5 else 2,frameon=True,fancybox=True,shadow=True)
    if title: plt.title(title,y=1.1,fontdict=font_title)    

    if savepath: plt.savefig(savepath,bbox_inches='tight')

    return C

def likelihood_contour( data, name, labels, levels = ['68%','90%'], title = r"HESE: $\phi_0 = 2.12,\gamma=2.87$", savepath = None ):

    fig = plt.figure()
    tax = flavor_triangle()

    lh, ll = [], []

    ts_values = [ts_dict[i] for i in levels]


    C2 = tax.ca.contour(data[name]["ft_grid_asimov_poisson"],
                        data[name]["fe_grid_asimov_poisson"],
                        data[name]["ts_grid_asimov_poisson"],  
                        ts_values,
                        linestyles=["-",'--'],
                        linewidths=3,
                        colors='black')


    levs_vals = np.linspace(0,10,num=45)

    # heatmap
    X = tax.ca.contourf(data[name]["ft_grid_asimov_poisson"],
                        data[name]["fe_grid_asimov_poisson"],
                        data[name]["ts_grid_asimov_poisson"], 
                        levs_vals,
                        cmap= plt.colormaps['Blues_r'])

    # create colourbar
    cax = plt.axes([1., 0.2, 0.045, 0.65])
    cbar = plt.colorbar(X,
                        cax=cax, # axes where to make the colourbar
                        spacing='proportional',
                        ticks=[2.37,5.99,9.21])
    cbar.set_label(label=r'$-2\Delta\mathrm{log}\mathcal{L}$',size=16,fontfamily='serif')
    cbar.ax.set_yticklabels(['2.37','5.99','9.21'])  # vertically oriented colorbar

    if savepath: plt.savefig(savepath,bbox_inches='tight')

def polygon_area(x, y):
    # Close path if not already closed
    if x[0] != x[-1] or y[0] != y[-1]:
        x = np.append(x, x[0])
        y = np.append(y, y[0])
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

def compare_area( C, alt_key, base_key, levels ):
    areas = {}

    ts_values = [ts_dict[i] for i in levels]

    for name in [alt_key,base_key]: 
        # print(f"Processing {name}")
        contour_obj = C[name]
        area_list = []
        for i, level in enumerate(levels):  # 68%, 90%
            paths = contour_obj.collections[i].get_paths()
            level_area = 0.0
            for p in paths:
                v = p.vertices
                x, y = v[:, 0], v[:, 1]
                level_area += polygon_area(x, y)
            area_list.append(level_area)
            # print(f"Area for level {ts_values[i]} ({level}): {level_area:.4f}")
        areas[name] = area_list

    # Now calculate and print ratio of areas at 68% CL (index 0) and 90% CL (index 1)
    for i, level in enumerate(levels):
        ratio = areas[alt_key][i] / areas[base_key][i]
        print(f"Area ratio ({alt_key} / {base_key}) at {level}: {ratio:.4f}")