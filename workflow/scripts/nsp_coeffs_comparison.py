import numpy as np
import pandas as pd
import os
import argparse
import pickle
from scipy.stats import permutation_test
from sklearn.linear_model import LinearRegression

parser = argparse.ArgumentParser(description="Use NSP to calculate a integration and segregation coeffs")
parser.add_argument("--input_path", type=str, help="The path to the directory with NSP coeffs")
parser.add_argument("--out_dir", type=str, help="The path to dir where the output files will be saved")
parser.add_argument("--thread", type=str)
parser.add_argument("--motion_summary", type=str)
parser.add_argument("--demo_data", type=str)
args = parser.parse_args()

nsp_coeffs = pd.read_csv(args.input_path)
demo_data = args.demo_data

# Find excluded participants for this thread
motion = pd.read_csv(args.motion_summary, sep="\t")

excluded = []

thread_ses = False
thread_dir = False
if "mean" in args.thread:
    if "ses" in args.thread:
        thread_ses = args.thread.split("_")[0].split("-")[1]
else:
    thread_ses = args.thread.split("_")[0].split("-")[1]
    thread_dir = args.thread.split("_")[1].split("-")[1]
for i in range(len(motion)):
    subid = motion.loc[i, "subid"]
    ses = motion.loc[i, "ses"]
    dir = motion.loc[i, "dir"]
    max_fds_trans = motion.loc[i, "max_fd_trans"]
    max_fds_rot = motion.loc[i, "max_fd_rot"]
    if max_fds_trans > 3 or max_fds_rot > 3:
        if not ses:
            excluded.append(int(subid))
        elif ses == thread_ses:
            if not dir:
                excluded.append(int(subid))
            elif dir == thread_dir:
                excluded.append(int(subid))

subids = nsp_coeffs["subid"]
subids = [subid for subid in subids if subid not in excluded]

confounds = []

# Create the confounds matrix
for subid in subids:
    cur_sub = demo_data[demo_data["src_subject_id"] == subid]
    confounds.append([int(cur_sub.phenotype.item() == "Patient"), int(cur_sub.interview_age.item()), int(cur_sub.sex.item() == 'F')])
confounds = np.array(confounds)

ps = {}
stats = {}

metric_names = ["H_In", "H_Se", "F_In", "F_Se"]

def statistic(x, y, axis):
    return np.mean(x, axis=axis) - np.mean(y, axis=axis)

for metric in metric_names:
    # Regress confounds out
    target = []
    for subid in subids:
        target.append(nsp_coeffs[nsp_coeffs["subid"] == subid][metric].values)
    reg = LinearRegression().fit(confounds, target)

    for i, subid in enumerate(subids):
        nsp_coeffs.loc[nsp_coeffs["subid"] == subid, metric] -= confounds[i, 1]*reg.coef_[0][1] + confounds[i, 2]*reg.coef_[0][2]

    # Compare groups
    patient_values = nsp_coeffs[(nsp_coeffs["patient"] == 1) & (nsp_coeffs["subid"] not in excluded)][metric].values
    hc_values = nsp_coeffs[(nsp_coeffs["patient"] == 0) & (nsp_coeffs["subid"] not in excluded)][metric].values
    res = permutation_test([patient_values, hc_values], statistic, permutation_type="independent", n_resamples=100000, rng=13)
    ps[metric] = res.pvalue
    stats[metric] = res.statistic

# Save results
with open(os.path.join(args.out_dir, f"nsp_coeffs_ps_{args.thread}.pkl"), "wb") as f:
    pickle.dump(ps, f)
with open(os.path.join(args.out_dir, f"nsp_coeffs_stats_{args.thread}.pkl"), "wb") as f:
    pickle.dump(stats, f)