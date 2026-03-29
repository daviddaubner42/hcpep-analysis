import numpy as np
import pandas as pd
import argparse
import pickle
import os
from scipy.stats import permutation_test
from sklearn.linear_model import LinearRegression

parser = argparse.ArgumentParser(description="Compare the global metrics between the two groups")
parser.add_argument("--metric_path", type=str, help="The path to the csv file with global metrics")
parser.add_argument("--thread", type=str)
parser.add_argument("--out_dir", type=str, help="The directory where the output files will be saved")
parser.add_argument("--demo_data_path", type=str, help="Path to the demographic data")
parser.add_argument("--subids", type=str, nargs="+", help="All the subids to be included")
args = parser.parse_args()

demo_data = pd.read_table(args.demo_data_path)

confounds = []

# Create the confounds matrix
for subid in args.subids:
    cur_sub = demo_data[demo_data["src_subject_id"] == subid]
    confounds.append([int(cur_sub.phenotype.item() == "Patient"), int(cur_sub.interview_age.item()), int(cur_sub.sex.item() == 'F')])
confounds = np.array(confounds)

# Load the global metrics data
props = pd.read_csv(args.metric_path)

ps = {}
stats = {}

metric_names = ["abs_mean_connectivity", "avg_clustering", "modularity", "global_efficiency", "assortativity", "robustness_random", "robustness_targeted"]

def statistic(x, y, axis):
    return np.mean(x, axis=axis) - np.mean(y, axis=axis)

for metric in metric_names:
    # Regress confounds out
    target = []
    for subid in args.subids:
        target.append(props[props["subid"] == int(subid)][metric].values)
    reg = LinearRegression().fit(confounds, target)

    for i, subid in enumerate(args.subids):
        props.loc[props["subid"] == subid, metric] -= confounds[i, 1]*reg.coef_[0][1] + confounds[i, 2]*reg.coef_[0][2]

    # Compare groups
    patient_values = props[props["patient"] == 1][metric].values
    hc_values = props[props["patient"] == 0][metric].values
    res = permutation_test([patient_values, hc_values], statistic, permutation_type="independent", n_resamples=100000, rng=13)
    ps[metric] = res.pvalue
    stats[metric] = res.statistic

# Save results
with open(os.path.join(args.out_dir, f"global_metric_ps_{args.thread}.pkl"), "wb") as f:
    pickle.dump(ps, f)
with open(os.path.join(args.out_dir, f"global_metric_stats_{args.thread}.pkl"), "wb") as f:
    pickle.dump(stats, f)