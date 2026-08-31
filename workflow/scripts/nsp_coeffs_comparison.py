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
parser.add_argument("--exclusion_dict", type=str, help="Path to the exclusion dictionary")
args = parser.parse_args()

nsp_coeffs = pd.read_csv(args.input_path)
demo_data = pd.read_table(args.demo_data)

with open(args.exclusion_dict, "rb") as f:
    exclusion_dict = pickle.load(f)

subids = exclusion_dict["FC"]

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
        target.append(nsp_coeffs[nsp_coeffs["subid"] == int(subid)][metric].item())
    reg = LinearRegression().fit(confounds, target)

    for i, subid in enumerate(subids):
        nsp_coeffs.loc[nsp_coeffs["subid"] == subid, metric] -= confounds[i, 1]*reg.coef_[1] + confounds[i, 2]*reg.coef_[2]

    # Compare groups
    patient_values = nsp_coeffs.loc[(nsp_coeffs["patient"] == 1) & (nsp_coeffs["subid"].isin([int(id) for id in subids]))][metric].values
    hc_values = nsp_coeffs.loc[(nsp_coeffs["patient"] == 0) & (nsp_coeffs["subid"].isin([int(id) for id in subids]))][metric].values
    res = permutation_test([patient_values, hc_values], statistic, permutation_type="independent", n_resamples=100000, rng=13)
    ps[metric] = res.pvalue
    stats[metric] = res.statistic

# Save results
with open(os.path.join(args.out_dir, f"nsp_coeffs_ps_{args.thread}.pkl"), "wb") as f:
    pickle.dump(ps, f)
with open(os.path.join(args.out_dir, f"nsp_coeffs_stats_{args.thread}.pkl"), "wb") as f:
    pickle.dump(stats, f)