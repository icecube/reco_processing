"""Script holding a class that can build input param configs from bestfit results"""
# TODO: Generalize for any fit result, not just freefits

import numpy as np
import os
import yaml
import socket
import glob

from NNMFit.utilities import ScanHandler


class FreefitParamConfig():
    def __init__(
        self,
        scan_path,
        cobalt_base_config_dir="/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/configs/flavor_globalfit/",
        ac_base_config_dir="/home/home2/institut_3b/pfuerst/software/NNMConfigs/Globalfit_lx3b/",
        config_subdir="analysis_configs/input_pars_only",
        force_read=True,
    ):
        # check the server:
        if "icecube.wisc.edu" in socket.gethostname():
            self.full_config_dir = os.path.join(cobalt_base_config_dir, config_subdir)
        elif "physik.rwth-aachen.de" in socket.gethostname():
            self.full_config_dir = os.path.join(
                ac_base_config_dir, config_subdir
            )
        print(f"Initializing on server {socket.gethostname()}. ")
        print(f"Using config directory: {self.full_config_dir}")
        self.scan_path = scan_path.rstrip(os.sep)  # Ensure no trailing slash

        # get the name of the directory holding the scan:
        self.scan_name = os.path.basename(self.scan_path)

        # get the name of the directory one level above (for example "stepX")
        self.scan_dirname = os.path.basename(os.path.dirname(self.scan_path))

        # get the scanhandler object of the scan:
        self.scan_hdl = ScanHandler(self.scan_path, force_read=force_read)

        # extract the relevant info
        _, self.min_llh_index, self.min_llh_row = self.get_min_llh_freefit(
            self.scan_hdl
        )
        self.freefit_filename = self.get_freefit_filename_from_index(
            self.min_llh_index
        )

        # generate the name of the input param config:
        self.name = self.generate_name(self.full_config_dir)

    @staticmethod
    def get_freefit_df(scan_hdl):
        """Get the freefit dataframe from the scan handler."""
        return scan_hdl.get_raw_df().loc["freefit"]

    @staticmethod
    def check_columns_close(df, tol=1e-3):
        """Check if all columns in the dataframe are close to the first value.
        """
        cols = df.columns
        not_close_columns = []
        for col in cols:
            if not np.allclose(
                df[col].values, df[col].values[0], rtol=tol, atol=tol
            ):
                not_close_columns.append(col)
        if not_close_columns:
            # print the amount of columns that are not close
            print(
                f"{len(not_close_columns)} of {len(df)} "
                f"total columns are not close: {not_close_columns}"
            )

    def get_min_llh_freefit(self, scan_hdl):
        """Get the minimum log-likelihood and its index from the 
        freefit dataframe."""
        # get the dataframe part with the freefits
        freefit_df = FreefitParamConfig.get_freefit_df(scan_hdl)

        # get the minimum llh values
        min_llh = freefit_df['llh'].min()

        # find all fits which found this minimum
        min_llh_rows = freefit_df[freefit_df['llh'] == min_llh]

        # if there are multiple rows, we take the first one
        min_llh_row = min_llh_rows.iloc[0]

        min_llh_index = freefit_df['llh'].idxmin()
        print("found the minimum llh value: ", min_llh)

        return min_llh, min_llh_index, min_llh_row

    def get_freefit_filename_from_index(self, min_llh_index):
        """Get the filename (with number) of the freefit,
        i.e. 'Freefit' or 'Freefit_03' but omit the .pickle ending
        """
        # find all files with "Freefit" in the name
        all_freefit_names = [
            name for name in sorted(glob.glob(self.scan_path+"/Freefit*"))
        ]
        print(f"Found {len(all_freefit_names)} freefit files in {self.scan_path}")
        name = all_freefit_names[min_llh_index]
        print(f"This is the index of the best fit: {min_llh_index}, the name is {name}")
        # get only the filename without the path and without the .pickle ending
        name = os.path.basename(name).replace('.pickle', '')
        # if min_llh_index == 0:
        #     name = "Freefit"
        # elif min_llh_index > 0 and min_llh_index < 10:
        #     name = f"Freefit_0{min_llh_index}"
        # else:
        #     name = f"Freefit_{min_llh_index}"
        return name

    def generate_name(self, config_dir):
        # input param config filename
        name = (
            f"Input_params_{self.scan_dirname}_{self.scan_name}"
            f"_{self.freefit_filename}.yaml"
        )
        name = os.path.join(config_dir, name)
        return name

    def write(self, custom_name=None):
        """Write the input parameter configuration belonging to the bestfit
        from the scan handler.

        If custom_name is provided, it will be used instead of the default
        """

        # extract only the relevant values to a dictionary
        values = self.min_llh_row.drop(['fit_success', 'llh']).to_dict()

        # add the "input_params" level to values
        to_dump = {
            "input_params": values,
        }
        if custom_name is not None:
            name_dump = custom_name
        else:
            name_dump = self.name

        # write to file.
        with open(name_dump, 'w', encoding='utf-8') as f:
            yaml.dump(to_dump, f, default_flow_style=False)

        # add a commented line to the yaml file in line 1:
        with open(name_dump, 'r') as f:
            lines = f.readlines()
        lines.insert(
            0, f"# Params from {self.scan_path}/{self.freefit_filename}\n"
        )
        # close again:
        with open(name_dump, 'w') as f:
            f.writelines(lines)

        print(f"Writing input params to {name_dump}")

    def get_name(self):
        """Get the name of the input parameter configuration file."""
        return self.name

    def read(self, generate=True):
        """Read the input parameter configuration from the file."""
        if not os.path.exists(self.name):
            print(
                f"Input parameter config {self.name} "
                f"does not exist. Generating it now."
            )
            if generate:
                print(
                    f"Generating input parameter config "
                    f"{self.name} from bestfit "
                    f"{self.scan_path}/{self.freefit_filename}."
                )
                self.write()

        with open(self.name, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        return data.get("input_params", {})
