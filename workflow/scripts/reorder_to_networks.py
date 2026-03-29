import numpy as np
import pandas as pd
import argparse
import os
import pickle

parser = argparse.ArgumentParser(description="Reorder the average FCs, p-values and statistics to be organized by network")
parser.add_argument("--results_dir", type=str, help="The path to the results directory for the pairwise FC comparison")
parser.add_argument("--network_path", type=str)
parser.add_argument("--thread", type=str)
args = parser.parse_args()

# Load the average FC matrices, p-values, statistics, and network information
avg_patient_fc = np.loadtxt(os.path.join(args.results_dir, f"{args.thread}_avg_patient_fc.csv"), delimiter=',')
avg_hc_fc = np.loadtxt(os.path.join(args.results_dir, f"{args.thread}_avg_hc_fc.csv"), delimiter=',')
p_vals = np.loadtxt(os.path.join(args.results_dir, f"{args.thread}_p_vals.csv"), delimiter=',')
p_vals_fdr = np.loadtxt(os.path.join(args.results_dir, f"{args.thread}_p_vals_fdr.csv"), delimiter=',')
stats = np.loadtxt(os.path.join(args.results_dir, f"{args.thread}_stats.csv"), delimiter=',')
with open(os.path.join(args.network_dir, f"network_idxs.pkl"), "rb") as f:
    network_idxs = pickle.load(f)

network_ordering = []
for net, idxs in network_idxs:
    for i in idxs:
        network_ordering.append(i)
idx_transform = {}
for net_i, og_i in enumerate(network_ordering):
    idx_transform[og_i] = net_i


# Reorder the p-values and statistics according to the new ordering
n = len(p_vals)
new_p_vals = np.zeros((n, n))
new_p_vals_fdr = np.zeros((n, n))
new_stats = np.zeros((n, n))
new_avg_patient_fc = np.zeros((n, n))
new_avg_hc_fc = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        new_i = idx_transform[i]
        new_j = idx_transform[j]
        new_p_vals[new_i, new_j] = p_vals[i, j]
        new_p_vals_fdr[new_i, new_j] = p_vals_fdr[i, j]
        new_stats[new_i, new_j] = stats[i, j]
        new_avg_patient_fc[new_i, new_j] = avg_patient_fc[i, j]
        new_avg_hc_fc[new_i, new_j] = avg_hc_fc[i, j]

# Save the average FC matrices and reordered p-values and statistics
np.savetxt(os.path.join(args.results_dir, f"{args.thread}_p_vals_reordered.csv"), new_p_vals, delimiter=',')
np.savetxt(os.path.join(args.results_dir, f"{args.thread}_p_vals_fdr_reordered.csv"), new_p_vals_fdr, delimiter=',')
np.savetxt(os.path.join(args.results_dir, f"{args.thread}_stats_reordered.csv"), new_stats, delimiter=',')
np.savetxt(os.path.join(args.results_dir, f"{args.thread}_avg_patient_fc_reordered.csv"), new_avg_patient_fc, delimiter=',')
np.savetxt(os.path.join(args.results_dir, f"{args.thread}_avg_hc_fc_reordered.csv"), new_avg_hc_fc, delimiter=',')