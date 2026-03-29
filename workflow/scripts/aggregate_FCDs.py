import pickle
import os
import numpy as np
import pandas as pd
import argparse
from sklearn.linear_model import LinearRegression

parser = argparse.ArgumentParser(description="Plot the results of the pairwise FC comparison")
parser.add_argument("--fcds_path", type=str, help="The path to the FCD results directory")
parser.add_argument("--subids", type=str, nargs="+", help="All the subids to be included")
parser.add_argument("--thread", type=str)
parser.add_argument("--demo_data_path", type=str, help="Path to the demographic data")
args = parser.parse_args()

# Load demographic data
demo_data = pd.read_table(args.demo_data_path)

confounds = []
fcds = {}
hists = {}

# Create the confounds matrix and load the FCD results
for subid in args.subids:
    cur_sub = demo_data.loc[demo_data["src_subject_id"] == subid]
    confounds.append([int(cur_sub.phenotype.item() == "Patient"), int(cur_sub.interview_age.item()), int(cur_sub.sex.item() == 'F')])
    
    fcds[subid] = np.loadtxt(os.path.join(args.fcds_path, f"sub-{subid}", f"sub-{subid}_FCD_{args.thread}.csv"), delimiter=',')
    hists[subid] = np.loadtxt(os.path.join(args.fcds_path, f"sub-{subid}", f"sub-{subid}_FCD_hist_{args.thread}.csv"), delimiter=',')
confounds = np.array(confounds)

# Save raw results
with open(os.path.join(args.fcds_path, f"FCDs_{args.thread}.pkl"), "wb") as f:
    pickle.dump(fcds, f)
with open(os.path.join(args.fcds_path, f"FCD_hists_{args.thread}.pkl"), "wb") as f:
    pickle.dump(hists, f)

# Regress the confounds out of the histograms
all_hists = np.array(list(hists.values()))
for bin in range(all_hists.shape[1]):
    target = all_hists[:, bin]
    reg = LinearRegression().fit(confounds, target)

    for i, subid in enumerate(args.subids):
        hists[subid][bin] -= confounds[i, 1]*reg.coef_[1] + confounds[i, 2]*reg.coef_[2]

# Save regressed histograms
with open(os.path.join(args.fcds_path, f"FCD_hists_regr_{args.thread}.pkl"), "wb") as f:
    pickle.dump(hists, f)