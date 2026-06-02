from scipy.interpolate import RectBivariateSpline
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# spline = pickle.load(open("/data/user/eyildizci/NNMFit_combined_fit_for_pev/combined_fit_configs_and_scripts/scripts_2/new_muon_template/combined_DNN_spline.pickle", "rb"))
# outfile = '/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/muon_template_northern/templates/reproduce_new_muon_template.pickle' 
# energy_bins_out = np.logspace(2.5, 7, 46)

# spline = pickle.load(open("/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/muon_template_northern/combined_DNN_spline.pickle", "rb"))
# outfile = '/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/muon_template_northern/templates/reproduce_new_muon_template_own_spline.pickle' 
# energy_bins_out = np.logspace(2.5, 7, 46)

spline = pickle.load(open("/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/muon_template_northern/combined_Truncated_spline.pickle", "rb"))
outfile = '/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/notebooks/muon_template_northern/templates/truncated_loge2.5_v0.pickle' 
energy_bins_out = np.logspace(2.5, 7, 46)


energy_bins = np.logspace(2, 7, 51)
energy_bin_centers = np.log10(energy_bins[:-1] + np.diff(energy_bins) / 2) # centers of the bins in logspace

cos_zen_bins = np.linspace(-1,0.0872,34)
cos_zen_bin_centers = (cos_zen_bins[:-1] + np.diff(cos_zen_bins) / 2)


muon_template = spline(
    energy_bin_centers,
    cos_zen_bin_centers,
    grid=True
)

total_rate = spline.integral(2,7,cos_zen_bins.min(),cos_zen_bins.max())
print('spline total rate',total_rate)


#muon_template = muon_template * 3.1458995230232768e-06 / np.sum(muon_template) #that nummber is the total rate of the kde used to construct the spline

total_rate_correction_ratio = 3.1458995230232768e-06 / np.sum(muon_template)

energy_bins = energy_bins_out
energy_bin_centers = np.log10(energy_bins[:-1] + np.diff(energy_bins) / 2) # centers of the bins in logspace

cos_zen_bins = np.linspace(-1,0.0872,34)
cos_zen_bin_centers = (cos_zen_bins[:-1] + np.diff(cos_zen_bins) / 2)


muon_template_correct_binning = spline(
    energy_bin_centers,
    cos_zen_bin_centers,
    grid=True
)

muon_template_correct_binning *= total_rate_correction_ratio

#make values of muon_template_correct_binning below some threshold zero
threshold = 1e-11
muon_template_correct_binning[muon_template_correct_binning < threshold] = 0

new_template_2d_scipy = muon_template_correct_binning
new_template_2d = np.fliplr(muon_template_correct_binning)
new_template = new_template_2d.flatten()

muon_template_correct_binning = np.fliplr(muon_template_correct_binning)

print('new muon template rate',np.sum(muon_template))
print('new muon template rate with correct binning',np.sum(muon_template_correct_binning))
print(muon_template_correct_binning.shape)

def replace_template(path):
    """
    Replace the template in the original file with the new template.
    """
    # Load the original file
    with open(path, 'rb') as f:
        data = pickle.load(f)

    print(data['template'])
    print(data['total_rate'])

    # Replace the template
    data['template'] = new_template
    data['template_2d'] = new_template_2d
    data['template_2d_scipy'] = new_template_2d_scipy
    # data['total_rate'] = 2.1056402918260832e-06
    data['total_rate'] = 0.0
    data['energy_bins'] = energy_bins
    data['energy_bins_centers'] = 10**energy_bin_centers
    data['cos_zen_bins'] = cos_zen_bins
    data['zenith_bins'] = cos_zen_bins
    data['zenith_bins_centers'] = cos_zen_bin_centers
    print(data['template'])
    print(data['total_rate'])
    # Save the modified file
    with open(path, 'wb') as f:
        pickle.dump(data, f)

replace_template(outfile)