import os
import pandas as pd
import nibabel as nib
import numpy as np
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--derivatives_dir", type=str, help="The path to the derivatives directory")
parser.add_argument("--demo_data_path", type=str, help="Path to the demographic data")
parser.add_argument("--motion_summary", type=str, help="Path to the motion summary file")
parser.add_argument("--qc_summary", type=str, help="Path to the QC summary file")
parser.add_argument("--output", type=str, help="Path to the output file")
args = parser.parse_args()

# derivatives_dir = "/Users/brainsimulation/Desktop/hcpep-derivatives"

# raw_subids = []
# print(f"Length of raw_subids: {len(raw_subids)}")

fmriprep_subids = [f[4:] for f in os.listdir(os.path.join(args.derivatives_dir, "fmriprep")) if f.startswith("sub-") and not f.endswith(".html")]
print(f"Number of fmriprep processed participants: {len(fmriprep_subids)}")

xcpd_subids = [f[4:] for f in os.listdir(os.path.join(args.derivatives_dir, "xcp_d")) if f.startswith("sub-") and not f.endswith(".html")]
print(f"Number of xcp-d processed participants: {len(xcpd_subids)}")

demo_data = pd.read_table(args.demo_data_path, sep="\t")
analysable_subids = [subid for subid in xcpd_subids if subid in demo_data["src_subject_id"].values]
print(f"Number of participants with demographic info: {len(analysable_subids)}")

# Coverage

excluded_coverage = []

for ses in ["1", "2"]:
    for dir in ["AP", "PA"]:
        for subid in xcpd_subids:
            ts = np.array(nib.load(os.path.join(args.derivatives_dir, "xcp_d", f"sub-{subid}", f"ses-{ses}", "func", f"sub-{subid}_ses-{ses}_task-rest_dir-{dir}_space-fsLR_seg-Glasser_den-91k_stat-mean_timeseries.ptseries.nii")).dataobj)
            for i in range(ts.shape[1]):
                if np.all(np.isnan(ts[:, i])):
                    if not i in [119, 299, 118, 298]:
                        excluded_coverage.append(int(subid))

coverage_subids = [subid for subid in analysable_subids if not int(subid) in excluded_coverage]
print(f"Number of participants passing coverage QC: {len(coverage_subids)}")

# Motion
motion = pd.read_csv(args.motion_summary, sep="\t")

excluded_motion = {}

for thread in ["mean", "ses-1_mean", "ses-2_mean", "ses-1_dir-AP", "ses-1_dir-PA", "ses-2_dir-AP", "ses-2_dir-PA"]:
    excluded_motion[thread] = []

    thread_ses = False
    thread_dir = False
    if "mean" in thread:
        if "ses" in thread:
            thread_ses = thread.split("_")[0].split("-")[1]
    else:
        thread_ses = thread.split("_")[0].split("-")[1]
        thread_dir = thread.split("_")[1].split("-")[1]
    for i in range(len(motion)):
        subid = motion.loc[i, "subid"]
        ses = motion.loc[i, "ses"]
        dir = motion.loc[i, "dir"]
        max_fds_trans = motion.loc[i, "max_fd_trans"]
        max_fds_rot = motion.loc[i, "max_fd_rot"]
        if max_fds_trans > 3 or max_fds_rot > 3:
            if not thread_ses:
                excluded_motion[thread].append(int(subid))
            elif ses == int(thread_ses):
                if not thread_dir:
                    excluded_motion[thread].append(int(subid))
                elif dir == thread_dir:
                    excluded_motion[thread].append(int(subid))

motion_subids = [subid for subid in coverage_subids if not int(subid) in excluded_motion["mean"]]
print(f"Number of participants passing motion QC: {len(motion_subids)}")

qc_summary = pd.read_csv(args.qc_summary, sep=",")

excluded_fc = []
also_motion = 0

for i in range(qc_summary.shape[0]):
    subid = qc_summary.loc[i, "sub"][4:]
    ses = qc_summary.loc[i, "ses"]
    dir = qc_summary.loc[i, "dir"]
    if ses == 'ses-1':
        if qc_summary.loc[i, "any_attention"]:
            if subid not in excluded_fc:
                excluded_fc.append(int(subid))

qc_subids = [subid for subid in motion_subids if not int(subid) in excluded_fc]
print(f"Number of participants passing FC QC: {len(qc_subids)}")

exclusion_dict = {
    "fmriprep": fmriprep_subids,
    "xcp-d": xcpd_subids,
    "demographics": analysable_subids,
    "coverage": coverage_subids,
    "motion": motion_subids,
    "FC": qc_subids
}

# Save the exclusion dictionary
with open(args.output, "wb") as f:
    pickle.dump(exclusion_dict, f)