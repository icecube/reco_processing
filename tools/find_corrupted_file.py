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

    for jobname, info in jobs.items():
        jobid = info.get("JOBID")
        if not jobid:
            continue  # skip if no JOBID is defined

        out_file = os.path.join(log_dir, f"{jobid}.out")
        err_file = os.path.join(log_dir, f"{jobid}.err")

        if not os.path.isfile(out_file) or not os.path.isfile(err_file):
            missing_jobs[jobname] = info  # return the original job dict

    return missing_jobs

def cleanup_outputs_for_missing_jobs(missing_jobs):
    removed_files = []

    for jobname, info in missing_jobs.items():
        output_file = info.get("Outputfile")
        if output_file and os.path.isfile(output_file):
            try:
                os.remove(output_file)
                removed_files.append(output_file)
                print(f"Removed output file: {output_file}")
            except Exception as e:
                print(f"Failed to remove {output_file}: {e}")
    
    return removed_files

# Example usage:
if __name__ == "__main__":
    # dag_path = "/scratch/tvaneede/reco/run_evtgen_ftp/v0/reco_evtgen_dag_v0_22635_0000000-0000999_batch2" 
    # dag_path = "/scratch/tvaneede/reco/run_evtgen_ftp/v0/reco_evtgen_dag_v0_22635_0000000-0000999" 
    # dag_path = "/scratch/tvaneede/reco/run_evtgen_ftp/v0/reco_evtgen_dag_v0_22634_0000000-0000999" 
    # dag_path = "/scratch/tvaneede/reco/run_evtgen_ftp/v0/reco_evtgen_dag_v0_22634_0000000-0000999_batch2"
    # dag_path = "/scratch/tvaneede/reco/run_evtgen_ftp/v0/reco_evtgen_dag_v0_22612_0000000-0000999" 
    # dag_path = "/scratch/tvaneede/reco/run_evtgen_ftp/v0/reco_evtgen_dag_v0_22613_0000000-0000999" 

    for dag_path in os.listdir("/scratch/tvaneede/reco/run_pid_neha/v1/"):

        dag_path = "/scratch/tvaneede/reco/run_pid_neha/v1/" + dag_path

        job_dict = read_jobs(dag_path)
        missing_job_dicts = check_missing_logs(dag_path, job_dict)

        removed_outputs = cleanup_outputs_for_missing_jobs(missing_job_dicts)
        print(f"\nTotal removed output files: {len(removed_outputs)}")