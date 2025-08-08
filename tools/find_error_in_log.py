#!/usr/bin/env python
import os

def read_jobs(dag_path):
    submit_file = os.path.join(dag_path, "submit.dag")

    if not os.path.exists(submit_file):
        raise FileNotFoundError(f"{submit_file} does not exist.")

    jobs = {}
    with open(submit_file, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("JOB"):
                parts = line.split()
                jobname = parts[1]
                jobs[jobname] = {}
            elif line.startswith("VARS"):
                parts = line.split(None, 2)
                jobname = parts[1]
                vars_part = parts[2]
                # Parse key="value" pairs
                for entry in vars_part.split():
                    if "=" in entry:
                        key, val = entry.split("=", 1)
                        jobs[jobname][key] = val.strip('"')

    return jobs

def check_missing_logs(dag_path, jobs):
    log_dir = os.path.join(dag_path, "logs")
    if not os.path.isdir(log_dir):
        raise NotADirectoryError(f"{log_dir} does not exist or is not a directory.")

    missing_jobs = {}
    error_jobs = {}
    gulliver_error_jobs = {}

    for jobname, info in jobs.items():
        jobid = info.get("JOBID")
        if not jobid:
            continue  # skip if no JOBID is defined

        out_file = os.path.join(log_dir, f"{jobid}.out")
        err_file = os.path.join(log_dir, f"{jobid}.err")

        if not os.path.isfile(out_file) or not os.path.isfile(err_file):
            missing_jobs[jobname] = info  # return the original job dict
            continue

        # find errors
        with open(err_file, "r") as f:
            for line in f:
                if "ERROR" in line:
                    error_jobs[jobname] = info
                    if "I3Gulliver" in line:
                        gulliver_error_jobs[jobname] = info




    return missing_jobs, error_jobs, gulliver_error_jobs


# Example usage:
if __name__ == "__main__":

    # dag_path = "/scratch/tvaneede/reco/hdf_taupede_tianlu/spice_l3casc/hdf_dag_spice_l3casc" 
    # dag_path = "/scratch/tvaneede/reco/hdf_taupede_tianlu/ftp_l3casc/hdf_dag_ftp_l3casc" 

    base_path = "/scratch/tvaneede/reco/run_taupede_tianlu/v5"
    # base_path = "/scratch/tvaneede/reco/hdf_taupede_tianlu/v5/"

    for dag_name in os.listdir(base_path):
        dag_path = os.path.join(base_path, dag_name)
        print(dag_path)

        job_dict = read_jobs(dag_path)
        missing_job_dicts, error_job_dicts, gulliver_error_jobs = check_missing_logs(dag_path, job_dict)

        print(f"\nMissing jobs: {len(missing_job_dicts)}")
        print(f"\nError jobs: {len(error_job_dicts)}")
        print(f"\nGulliver error jobs: {len(gulliver_error_jobs)}")
        # print(error_job_dicts)