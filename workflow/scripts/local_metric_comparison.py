import numpy as np
import pandas as pd
import argparse
import pickle
import os
from scipy.stats import permutation_test, false_discovery_control

parser = argparse.ArgumentParser(description="Perform group comparison for this metric")
parser.add_argument("--input_path", type=str)
parser.add_argument("--output_path", type=str)
parser.add_argument("--metric", type=str, help="The metric to be analysed")
parser.add_argument("--demo_data_path", type=str, help="Path to the demographical data")
parser.add_argument("--motion_summary", type=str)
parser.add_argument("--thread", type=str)
args = parser.parse_args()

# Load demo data
demo_data = pd.read_table(args.demo_data_path)

# Load aggr metrics
metrics = pd.read_csv(args.input_path)
metrics.rename(columns={"Unnamed: 0": "ROI"}, inplace=True)
subids = metrics.columns.drop("ROI")
rois = list(metrics["ROI"])

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

subids = [subid for subid in subids if subid not in excluded]

def statistic(x, y, axis):
    return np.mean(x, axis=axis) - np.mean(y, axis=axis)

ps = {}
stats = {}
# Perform group comparison for each ROI
for roi in rois:
    hcs = []
    nmdares = []
    for subid in subids:
        if demo_data.loc[demo_data["src_subject_id"] == subid].phenotype.item() == "Patient":
            nmdares.append(metrics[metrics["ROI"] == roi][subid])
        else:
            hcs.append(metrics[metrics["ROI"] == roi][subid])
    
    res = permutation_test([hcs, nmdares], statistic, n_resamples=10000)
    ps[roi] = res.pvalue
    stats[roi] = res.statistic

# Perform FDR correction
ps_fdr = false_discovery_control(list(ps.values())).T[0]

# Save the results
df = pd.DataFrame(np.array([np.array(list(ps.keys())).flatten(), np.array(list(ps.values())).flatten(), np.array(ps_fdr), np.array(list(stats.values())).flatten()]).T, columns=["ROI", "p", "p_FDR", "stat"])
df.to_csv(args.output_path)