import numpy as np
import pandas as pd
import os
import argparse
import pickle
from scipy.stats import permutation_test

parser = argparse.ArgumentParser(description="Use NSP to calculate a integration and segregation coeffs")
parser.add_argument("--input_path", type=str, help="The path to the directory with NSP coeffs")
parser.add_argument("--out_dir", type=str, help="The path to dir where the output files will be saved")
parser.add_argument("--thread", type=str)
args = parser.parse_args()

nsp_coeffs = pd.read_csv(args.input_path)

ps = {}
stats = {}

metric_names = ["H_In", "H_Se", "F_In", "F_Se"]

def statistic(x, y, axis):
    return np.mean(x, axis=axis) - np.mean(y, axis=axis)

for metric in metric_names:
    patient_values = nsp_coeffs[nsp_coeffs["patient"] == 1][metric].values
    hc_values = nsp_coeffs[nsp_coeffs["patient"] == 0][metric].values
    res = permutation_test([patient_values, hc_values], statistic, permutation_type="independent", n_resamples=100000, rng=13)
    ps[metric] = res.pvalue
    stats[metric] = res.statistic

# Save results
with open(os.path.join(args.out_dir, f"nsp_coeffs_ps_{args.thread}.pkl"), "wb") as f:
    pickle.dump(ps, f)
with open(os.path.join(args.out_dir, f"nsp_coeffs_stats_{args.thread}.pkl"), "wb") as f:
    pickle.dump(stats, f)