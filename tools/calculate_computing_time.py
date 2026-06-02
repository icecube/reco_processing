import re
from datetime import datetime, timedelta
import os, sys
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


logfile = "job.log"

import re
from datetime import datetime, timedelta

def extract_time_mem(logfile, print_output=True):
    start_time = None
    end_time = None
    cpu_time = timedelta(0)
    mem_mb = None

    with open(logfile) as f:
        for line in f:
            # Detect start time
            if "Job executing on host" in line:
                # Timestamp is in columns 2 and 3
                ts = " ".join(line.split()[2:4])
                start_time = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")

            # Detect end time: exact Condor termination line (ignore other messages)
            if re.match(r"^\d+\s+\(\d+\.\d+\.\d+\)\s+\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} Job terminated\.", line):
                ts = " ".join(line.split()[2:4])
                end_time = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")

            # Detect CPU usage line (Usr/Sys times)
            if "Usr" in line and "Sys" in line and "Remote Usage" in line:
                usr_match = re.search(r"Usr\s+\d+\s+(\d+):(\d+):(\d+)", line)
                sys_match = re.search(r"Sys\s+\d+\s+(\d+):(\d+):(\d+)", line)
                if usr_match and sys_match:
                    usr_time = timedelta(
                        hours=int(usr_match.group(1)),
                        minutes=int(usr_match.group(2)),
                        seconds=int(usr_match.group(3)),
                    )
                    sys_time = timedelta(
                        hours=int(sys_match.group(1)),
                        minutes=int(sys_match.group(2)),
                        seconds=int(sys_match.group(3)),
                    )
                    cpu_time = usr_time + sys_time


            # Memory usage
            if "MemoryUsage of job" in line:
                mem_match = re.search(r"(\d+)\s+-\s+MemoryUsage of job \(MB\)", line)
                if mem_match:
                    mem_mb = int(mem_match.group(1))

    # Report results
    if print_output:
        if start_time and end_time:
            wall_time = end_time - start_time
            print(f"Start time: {start_time}")
            print(f"End time:   {end_time}")
            print(f"Wall time:  {wall_time}")
            print(f"CPU time:   {cpu_time}")
        else:
            print("Could not find start or end in log.")

    return (end_time - start_time if start_time and end_time else None), cpu_time, mem_mb


def count_frames(logfile, print_output=False):
    frame_numbers = []

    pattern = re.compile(r"Currently processing frame (\d+)")

    with open(logfile) as f:
        for line in f:
            match = pattern.search(line)
            if match:
                frame_numbers.append(int(match.group(1)))

    num_frames = len(frame_numbers)

    if print_output:
        print(f"Number of frames processed: {num_frames}")
        print(f"Frames: {frame_numbers}")

    return num_frames

def get_job_file_sizes(logfile, print_output=False):
    """
    Parse a HTCondor submit log to extract input/output file paths and their sizes.
    Returns a list of dictionaries with 'job', 'infile', 'outfile', 'infile_size', 'outfile_size'.
    """
    jobs = []
    current_job = {}

    infile_pattern = re.compile(r'INFILES="(.+)"')
    outfile_pattern = re.compile(r'OUTFILE="(.+)"')
    job_pattern = re.compile(r'JOB (\S+)')

    with open(logfile) as f:
        for line in f:
            line = line.strip()

            # Job line
            job_match = job_pattern.match(line)
            if job_match:
                if current_job:
                    jobs.append(current_job)
                current_job = {'job': job_match.group(1), 'infile': None, 'outfile': None,
                               'infile_size': None, 'outfile_size': None}

            # Input file
            infile_match = infile_pattern.search(line)
            if infile_match and current_job:
                infile = infile_match.group(1)
                current_job['infile'] = infile
                if os.path.exists(infile):
                    current_job['infile_size'] = os.path.getsize(infile)
                else:
                    current_job['infile_size'] = None

            # Output file
            outfile_match = outfile_pattern.search(line)
            if outfile_match and current_job:
                outfile = outfile_match.group(1)
                current_job['outfile'] = outfile
                if os.path.exists(outfile):
                    current_job['outfile_size'] = os.path.getsize(outfile)
                else:
                    current_job['outfile_size'] = None

    # Append last job
    if current_job:
        jobs.append(current_job)

    if print_output:
        for job in jobs:
            print(f"Job: {job['job']}")
            print(f"  Input: {job['infile']} ({job['infile_size']} bytes)")
            print(f"  Output: {job['outfile']} ({job['outfile_size']} bytes)\n")

    return jobs

def process_all_logs(dag_path, plot=True):

    logs_path = dag_path + "/logs"

    wall_times = []
    cpu_times = []
    mems = []
    num_frames = []
    in_sizes = []
    out_sizes = []

    # Loop over all .log files in the directory
    for file_counter, logfile in enumerate(glob.glob(os.path.join(logs_path, "*.log"))):
        try:
            wall, cpu, mem = extract_time_mem(logfile, print_output=False)
            if wall and cpu:
                wall_times.append(wall.total_seconds() / 60.0)  # minutes
                cpu_times.append(cpu.total_seconds() / 60.0)    # minutes
                mems.append( mem )
            num_frames.append( count_frames( logfile.replace(".log",".out") ) )
        except Exception as e:
            print(f"Error processing {logfile}: {e}")
        
    # file sizes
    job_files = get_job_file_sizes(f"{dag_path}/submit.dag")
    # Extract file sizes from submit file
    for job in job_files:
        if job['infile_size'] is not None:
            in_sizes.append(job['infile_size'] / 1e6)   # convert to MB
        if job['outfile_size'] is not None:
            out_sizes.append(job['outfile_size'] / 1e6) # convert to MB

    # Compute averages
    avg_wall = np.mean(wall_times) if wall_times else 0
    avg_cpu = np.mean(cpu_times) if cpu_times else 0
    avg_mem = np.mean(mems) if mems else 0
    avg_frames = np.mean(num_frames) if num_frames else 0
    avg_in_size = np.mean(in_sizes) if in_sizes else 0
    avg_out_size = np.mean(out_sizes) if out_sizes else 0

    max_mem = max(mems)

    print(20*"*", dag_path.split("/")[-1])
    print(f"Processed {len(wall_times)} logs")
    print(f"Average wall time: {avg_wall:.2f} min")
    print(f"Average CPU time:  {avg_cpu:.2f} min")
    print(f"Average/max memory:  {avg_mem:.2f} / {max_mem:.2f} MB")
    print(f"Average frames:  {avg_frames:.2f}")
    print(f"Average input file size:  {avg_in_size:.2f} MB")
    print(f"Average output file size: {avg_out_size:.2f} MB")

    # Plot histograms
    if plot and wall_times and cpu_times:
        plt.figure(figsize=(10,4))

        plt.subplot(1,2,1)
        plt.hist(wall_times, bins=20, alpha=0.7)
        plt.xlabel("Wall time (minutes)")
        plt.ylabel("Counts")
        plt.title("Wall time distribution")

        plt.subplot(1,2,2)
        plt.hist(cpu_times, bins=20, alpha=0.7, color="orange")
        plt.xlabel("CPU time (minutes)")
        plt.ylabel("Counts")
        plt.title("CPU time distribution")

        plt.tight_layout()
        plt.show()

    return avg_wall, avg_cpu, avg_frames, avg_mem, max_mem, avg_in_size, avg_out_size

# Example usage
if __name__ == "__main__":

    processing_data = {
        "NuE_midE"    : {"id" : "22613"},
        "NuE_highE"   : {"id" : "22612"},
        "NuMu_midE"   : {"id" : "22645"},
        "NuMu_highE"  : {"id" : "22644"},
        "NuTau_midE"  : {"id" : "22634"},
        "NuTau_highE" : {"id" : "22635"},
    }

    for dataset_type, data_dict in processing_data.items():
        dag_path = f"/scratch/tvaneede/reco/run_taupede_tianlu/v9/reco_dag_v9_{data_dict['id']}_0001000-0001999"
        data_dict["avg_wall"], data_dict["avg_cpu"], data_dict["avg_frames"], data_dict["avg_mem"], data_dict["max_mem"], data_dict["avg_in_size"], data_dict["avg_out_size"] = process_all_logs(dag_path)


    # Append the custom module path
    sys.path.append("/data/user/tvaneede/GlobalFit/reco_processing")
    # Import the datasets module
    from datasets import datasets
    # set the inputs
    reco_version = "ftp_l3casc"
    # Dynamically select the desired dataset
    simulation_datasets = getattr(datasets, reco_version)

    # Prepare data
    table_data = []

    for simulation_dataset in simulation_datasets:
        dataset_type = simulation_dataset[:-1]
        
        row = {
            "Dataset": simulation_dataset,
            "Total Files": simulation_datasets[simulation_dataset]["nfiles"],
            "Avg CPU (hr)": processing_data[dataset_type]["avg_cpu"]/60,
            "Total CPU (hr)": (processing_data[dataset_type]["avg_cpu"]*simulation_datasets[simulation_dataset]["nfiles"])/60,
            "Max Mem (MB)": processing_data[dataset_type]["max_mem"],
            "Avg Input Size (MB)": processing_data[dataset_type]["avg_in_size"],
            "Total Input Size (GB)": processing_data[dataset_type]["avg_in_size"]*simulation_datasets[simulation_dataset]["nfiles"]/1000,
            "Avg Output Size (MB)": processing_data[dataset_type]["avg_out_size"],
            "Total Output Size (GB)": processing_data[dataset_type]["avg_out_size"]*simulation_datasets[simulation_dataset]["nfiles"]/1000,
        }
        table_data.append(row)

    # Create DataFrame
    df = pd.DataFrame(table_data)

    # Compute totals for numeric columns
    totals = {
        "Dataset": "TOTAL",
        "Total Files": df["Total Files"].sum(),
        "Avg CPU (hr)": "",  # Average of averages could also be computed if desired
        "Total CPU (hr)": df["Total CPU (hr)"].sum(),
        "Max Mem (MB)": "",
        "Avg Input Size (MB)": "",
        "Total Input Size (GB)": df["Total Input Size (GB)"].sum(),
        "Avg Output Size (MB)": "",
        "Total Output Size (GB)": df["Total Output Size (GB)"].sum(),
    }

    # Append totals row
    df = pd.concat([df, pd.DataFrame([totals])], ignore_index=True)

    # Display nicely
    print(df.to_string(index=False))

    # Export as LaTeX table
    df["Dataset"] = df["Dataset"].str.replace("_", " ", regex=False)
    print(df.to_latex(index=False, float_format=lambda x: "%.1f" % x))


