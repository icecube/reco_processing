import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import math
import glob
import h5py
import simweights
from argparse import ArgumentParser
import pylab as p
import pickle
from NNMFit.kde_tools import kde_utilities as kde_tools

parser = ArgumentParser()

parser.add_argument("-d", "--dataset", dest="dataset",
                    default=None, type=str, required=False,
                    help="Dataset number")
parser.add_argument("-n", "--nfiles", dest="nfiles",
                    default=None, type=int, required=False,
                    help="Number of files")

args = parser.parse_args()
dataset = args.dataset
nfiles = args.nfiles

paths = glob.glob('/data/user/eyildizci/NT_reco_study/hdf_files/corsika/*.hdf5')

def read_path(df,path,nfiles):
    nt = pd.DataFrame()
    temp = pd.DataFrame()
    hf = h5py.File(path, 'r')
    simfile = pd.HDFStore(path, 'r')
    flux_model = simweights.GaisserH4a()
    weight_obj = simweights.CorsikaWeighter(simfile, nfiles=nfiles)
    weights = weight_obj.get_weights(flux_model)
    CascScore = pd.DataFrame(np.array(hf['CascScore']))
    CorsikaWeightMap = pd.DataFrame(np.array(hf['CorsikaWeightMap']))
    #print('Emin: ', CorsikaWeightMap['EnergyPrimaryMin'].values[0])
    #print('Emax: ', CorsikaWeightMap['EnergyPrimaryMax'].values[0])
    SplineMPEICTruncatedEnergySPICEMie_AllDOMS_Muongun = pd.DataFrame(np.array(hf['SplineMPEICTruncatedEnergySPICEMie_AllDOMS_Muon']))
    PolyplopiaPrimary = pd.DataFrame(np.array(hf['PolyplopiaPrimary']))
    nt['TruncatedEnergy_zenith'] = SplineMPEICTruncatedEnergySPICEMie_AllDOMS_Muongun['zenith']
    #nt['TruncatedEnergy_azimuth'] = SplineMPEICTruncatedEnergySPICEMie_AllDOMS_Muongun['azimuth']
    nt['Truncated'] = SplineMPEICTruncatedEnergySPICEMie_AllDOMS_Muongun['energy']
    TUM_dnn_energy_hive = pd.DataFrame(np.array(hf['TUM_dnn_energy_hive']))
    TUM_dnn_energy_dst = pd.DataFrame(np.array(hf['TUM_dnn_energy_dst']))
    nt['DNN'] = 10**TUM_dnn_energy_hive['mu_E_on_entry']
    nt['PrimaryEnergy'] = CorsikaWeightMap['PrimaryEnergy']
    nt['PolyplopiaPrimary'] = PolyplopiaPrimary['energy']
    nt['GaisserH4a'] = weights
    nt['CascScore'] = CascScore['value']
    nt = nt[nt['CascScore']>0.5]
    nt['Multiplicity'] = CorsikaWeightMap['Multiplicity']
    nt['Run'] = CorsikaWeightMap['Run']
    nt['Event'] = CorsikaWeightMap['Event']
    df = pd.concat([df,nt])
    hf.close()
    return df

def weight_corrector(df):
    #if df['PrimaryEnergy'] is below 2400 GeV, divide the df['GaisserH4a'] by 5, elif above 2400 GeV but below 30000 GeV divide by 6, elif above 30000 GeV but below 400000000 GeV divide by 2
    if df['PrimaryEnergy'] < 2400:
        df['GaisserH4a'] = df['GaisserH4a']/5
    elif df['PrimaryEnergy'] >= 2400 and df['PrimaryEnergy'] < 30000:
        df['GaisserH4a'] = df['GaisserH4a']/6
    elif df['PrimaryEnergy'] >= 30000 and df['PrimaryEnergy'] < 400000000:
        df['GaisserH4a'] = df['GaisserH4a']/2
    return df

nt = pd.DataFrame()
for path in paths:
    nfiles = 100000
    if path.split('/')[-1].split('.')[0] == '20904':
        nfiles = 769211
    elif path.split('/')[-1].split('.')[0] == '22542':
        nfiles = 199979
    elif path.split('/')[-1].split('.')[0] == '22674':
        nfiles = 97976
    elif path.split('/')[-1].split('.')[0] == '22524':
        nfiles = 99903
    elif path.split('/')[-1].split('.')[0] == '22539':
        nfiles = 99998
    elif path.split('/')[-1].split('.')[0] == '22545':
        nfiles = 99992
    nt = read_path(nt,path,nfiles=nfiles)
# if nt['Truncated']==0 make it equal to 1
nt['Truncated'] = nt['Truncated'].replace(0,1)
# remove the events with zenith angle equal to 0
nt = nt[nt['TruncatedEnergy_zenith']!=0]
print('Total number of raw events: ',len(nt))

#print('Max zenith value: ',np.cos(nt['TruncatedEnergy_zenith']).max())
#Run and Event values of maximum zenith value
#print('Run and Event values of maximum zenith value: ',nt[nt['TruncatedEnergy_zenith']==0])

nt = nt.apply(weight_corrector, axis=1)
total_rate = nt['GaisserH4a'].sum()
print('KDE total rate: ', total_rate)
livetime = 365 * 24 * 3600

def make_and_eval_kde(df, log_energy_key, weights_key):
    reco_log_energy = np.log10(df[log_energy_key].values)
    reco_cos_zenith = np.cos(df['TruncatedEnergy_zenith'].values)
    weights = df[weights_key].values
    #weights = np.ones_like(weights)
    xeval = [reco_log_energy,reco_cos_zenith]
    alpha = 0.3

    kernel = kde_tools.KDEKernel.make_new_kernel(df[log_energy_key].values,
                                                    df['TruncatedEnergy_zenith'].values,
                                                    weights,
                                                    bounds = (None, (-1, np.cos(np.radians(85)))),
                                                    thresholds = (None, (-1, 0.487)),
                                                    alpha = alpha,
                                                    adaptive = True,
                                                    weight_adaptive_bw = False)

    spline = kernel.make_spline(np.linspace(2, 8, 100),
                                            np.linspace(-1, 0.0872, 100), method='RectBivariateSpline')

    return kernel,spline

def energy_coszen_plotter(nt,reco):
    nx = 51
    ny = 34
    bins_x = np.linspace(2, 7, nx)
    bins_y = np.linspace(-1, 0.0872, ny)

    xmin = 1

    mask_x = bins_x[:-1] >= xmin
    CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']
    #nt['Multiplicity'] = nt['Multiplicity']-1
    color_map = {1: CB_color_cycle[7], 2: CB_color_cycle[4], 3: CB_color_cycle[1]}
    colors = nt['Multiplicity'].map(color_map)
    marker_map = {1: 'o', 2: 's', 3: '^'}
    marker = nt['Multiplicity'].map(marker_map)

    #!!!
    #nt['Multiplicity'] = 1

    fig, ax = plt.subplots(1, 1, figsize=(18, 6))
    for multiplicity in sorted(nt['Multiplicity'].unique()):
        mask = nt['Multiplicity'] == multiplicity
        ax.scatter(np.log10(nt[reco][mask]), np.cos(nt['TruncatedEnergy_zenith'][mask]),
               s=nt['GaisserH4a'][mask] * livetime * 40, c=colors[mask],
               #c=colors[mask],
               marker=marker_map[multiplicity], label=f'Multiplicity {multiplicity}')

    xx, yy = np.mgrid[bins_x[0]:bins_x[-1]:complex(nx-1), bins_y[0]:bins_y[-1]:complex(ny-1)]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    f = np.reshape(kernel(positions).T, xx.shape)

    # make the values below 1e-16 zero
    #f[f*total_rate<1e-16] = 0


    dx = (bins_x[-1]-bins_x[0])/(nx-1)  # Approximate grid spacing in x
    dy = (bins_y[-1]-bins_y[0])/(ny-1)  # Approximate grid spacing in y

    integral = np.sum(f * dx * dy)
    total_rate_new = integral*total_rate

    im1 = ax.imshow(np.rot90(f) * dx * dy *total_rate, extent=[bins_x[0], bins_x[-1], bins_y[0], bins_y[-1]],
                #aspect='auto', cmap='Blues', norm=matplotlib.colors.LogNorm(vmin=2e-12, vmax=5e-8))
                aspect='auto', cmap='Blues', norm=matplotlib.colors.LogNorm())
    cbar = fig.colorbar(im1)#, extend='min')
    cbar.set_label(label='GaisserH4a Rate (Hz)',size=25)
    cbar.ax.tick_params(labelsize=20)

    ax.set_xlabel(r'log$_{10}$(Reco energy (GeV))', fontsize=25)
    ax.set_ylabel(r'cos(zenith)', fontsize=25)
    ax.set_ylim(bins_y[0],bins_y[-1])
    #ax.set_title(reco+f' KDE\nTotal rate: {total_rate_new:.3g}', fontsize=25)
    # make ticks larger
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.grid()
    ax.legend(loc='upper right',fontsize=20)
    plt.tight_layout()
    #fig.suptitle(mc_type, fontsize=25, y=1.0)
    plt.savefig('temp.png')
    plt.clf()

def energy_coszen_plotter_template():
    nx = 51
    ny = 34
    bins_x = np.linspace(2, 7, nx)
    bins_y = np.linspace(-1, 0.0872, ny)

    fig, ax = plt.subplots(1, 1, figsize=(18, 6))

    #print('Integral of the template: ', np.sum(muon_template['template_2d_scipy']))
    total_rate_new = np.sum(muon_template['template_2d_scipy'])

    im2 = ax.imshow(np.rot90(muon_template['template_2d_scipy']),
        extent=[bins_x[0], bins_x[-1], bins_y[0], bins_y[-1]], aspect='auto', cmap='Blues',
        #norm=matplotlib.colors.LogNorm(vmin=1e-20, vmax=1e-7))
        norm=matplotlib.colors.LogNorm())
    cbar = fig.colorbar(im2)
    cbar.set_label(label='GaisserH4a Rate (Hz)',size=25)
    cbar.ax.tick_params(labelsize=20)

    ax.set_xlabel(r'log$_{10}$(Reco energy (GeV))', fontsize=25)
    ax.set_ylabel(r'cos(zenith)', fontsize=25)
    ax.set_ylim(-1,0.0872)
    ax.set_title(f'GlobalFit Template\nTotal rate: {total_rate_new:.3g} Hz', fontsize=25)
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.grid()
    plt.tight_layout()
    #plt.savefig('./plots/Template_energy_cosZen.png')
    plt.clf()

def energy_coszen_plotter_ratio(nt,reco,reco2,limit=2):
    nx = 51
    ny = 34
    bins_x = np.linspace(2, 7, nx)
    bins_y = np.linspace(-1, 0.0872, ny)

    fig, ax = plt.subplots(1, 1, figsize=(18, 6))

    xx, yy = np.mgrid[bins_x[0]:bins_x[-1]:complex(nx-1), bins_y[0]:bins_y[-1]:complex(ny-1)]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    f = np.reshape(kernel(positions).T, xx.shape)

    dx = (bins_x[-1]-bins_x[0])/(nx-1)  # Approximate grid spacing in x
    dy = (bins_y[-1]-bins_y[0])/(ny-1)  # Approximate grid spacing in y

    integral = np.sum(f * dx * dy)

    print('Integral of the KDE: ', integral*total_rate)

    total_ratio = np.sum(muon_template['template_2d_scipy'])/(integral*total_rate)
    print('Total ratio: ', total_ratio)
    
    # make the values zero 1e-20
    #muon_template['template_2d_scipy'][muon_template['template_2d_scipy']==0] = 1e-22
    im3 = ax.imshow(np.rot90(f)*dx*dy*total_rate/np.rot90(muon_template['template_2d_scipy']),
            extent=[bins_x[0], bins_x[-1], bins_y[0], bins_y[-1]], aspect='auto', cmap='viridis',
            #vmin = 0,vmax=2)
            norm=matplotlib.colors.LogNorm(vmin=1e-1, vmax=1e1))
            #norm=matplotlib.colors.LogNorm())
    cbar = fig.colorbar(im3, extend='both')
    cbar.set_label(label=fr'$\frac{{New \ ({reco}) \ KDE}}{{GlobalFit \ Muon \ Template}}$',size=25)
    cbar.ax.tick_params(labelsize=20)

    ax.set_xlabel(r'log$_{10}$(Reco energy (GeV))', fontsize=25)
    ax.set_ylabel(r'cos(zenith)', fontsize=25)
    ax.set_ylim(bins_y[0],bins_y[-1])
    ax.set_title(f'Total rate ratio: {total_ratio:.3g}',fontsize=25)
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.grid()
    plt.tight_layout()
    #plt.savefig('./plots/combined_'+reco+'_energy_cosZen_ratio.png')
    plt.clf()


reco = 'DNN'
kernel,spline = make_and_eval_kde(nt, reco, 'GaisserH4a')
energy_coszen_plotter(nt,reco)

pickle.dump(kernel, open('combined_DNN_kernel.pickle', 'wb'))
pickle.dump(spline, open('combined_DNN_spline.pickle', 'wb'))


# reco = 'Truncated'
# kernel, spline = make_and_eval_kde(nt, reco, 'GaisserH4a')
# pickle.dump(kernel, open('combined_Truncated_kernel.pickle', 'wb'))
# pickle.dump(spline, open('combined_Truncated_spline.pickle', 'wb'))

'''



#muon_template = pd.read_pickle('/data/ana/Diffuse/GlobalFit/NNMFit/templates/Tracks_CorsikaMuon_Fullrange_drop_5lowEbins.pickle')
muon_template = pd.read_pickle('/data/ana/Diffuse/GlobalFit/NNMFit/templates/Tracks_CorsikaMuon.pickle')
print('Template total rate: ',muon_template['total_rate'])
#print('Template total rate2',np.sum(muon_template['template_2d_scipy']))
energy_coszen_plotter_template()

#print(min(muon_template['template_2d_scipy'].flatten()))
# print the lowest non-zero value
#print(np.min(muon_template['template_2d_scipy'][muon_template['template_2d_scipy']>0]))

#print(muon_template['template_2d_scipy'])
#print(muon_template['template_2d'])

for reco in ['DNN']:
    kernel = pd.read_pickle('combined_'+reco+'_kernel.pickle')
    # the other reco is reco2
    reco2 = 'DNN' if reco == 'Truncated' else 'Truncated'
    energy_coszen_plotter(nt,reco,reco2,limit=2)
    energy_coszen_plotter_ratio(nt,reco,reco2,limit=2)


#print(muon_template['template_2d'])

'''