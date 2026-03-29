import matplotlib.pyplot as plt
import matplotlib
import pickle
import scienceplots
import os
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Plot the results of the pairwise FC comparison")
parser.add_argument("--fc_dir", type=str, help="The path to the raw FC directory")
parser.add_argument("--thread", type=str, help="The 'thread' being processed (mean/session/direction/...)")
parser.add_argument("--subids", type=str, nargs='+', help="All the subids to be included")
parser.add_argument("--demo_data_path", type=str, help="Path to the demographic data")
parser.add_argument("--network_path", type=str, help="Path to the network information")
args = parser.parse_args()

# Plotting settings
matplotlib.rcParams.update(matplotlib.rcParamsDefault)
plt.style.use(['ieee'])
plt.rcParams.update({
    "text.usetex": False,
    "font.family": "serif"
})

cm = 1/2.54

# Load the average FC matrices for each group
avg_patient_fc = np.loadtxt(os.path.join(args.fc_dir, f"{args.thread}_avg_patient_fc_reordered.csv"), delimiter=',')
avg_hc_fc = np.loadtxt(os.path.join(args.fc_dir, f"{args.thread}_avg_hc_fc_reordered.csv"), delimiter=',')

# Load network information
with open(os.path.join(args.network_path), "rb") as f:
    networks = pickle.load(f)
network_names = list(networks.keys())

# Plot the average FC matrices for each group, with network boundaries
fig, ax = plt.subplots(1, 2, figsize=(14.5*cm,8.96*cm), dpi=600)
hc = ax[0].imshow(avg_hc_fc, cmap="viridis", vmin=-0.6, vmax=1)
ax[0].set_title("Healthy Controls", fontsize=7)
patient = ax[1].imshow(avg_patient_fc, cmap="viridis", vmin=-0.6, vmax=1)
ax[1].set_title("Patients", fontsize=7)

n = len(avg_patient_fc)

start = 0
end = 0
region_centers = []
for net, labels in networks.items():
    end += len(labels)
    if end < 84:
        ax[0].hlines(end-0.5, 0, n-0.5, colors="white", linewidth=0.15)
        ax[0].vlines(end-0.5, 0, n-0.5, colors="white", linewidth=0.15)
        ax[1].hlines(end-0.5, 0, n-0.5, colors="white", linewidth=0.15)
        ax[1].vlines(end-0.5, 0, n-0.5, colors="white", linewidth=0.15)
    region_centers.append(start + (end-start)/2)
    start = end
ax[0].set_yticks(region_centers, network_names, fontsize=7)
ax[0].set_xticks(region_centers, network_names, fontsize=7, rotation=90)
ax[1].set_yticks([])
ax[1].set_xticks(region_centers, network_names, fontsize=7, rotation=90)

ax[0].tick_params(length = 0)
ax[1].tick_params(length = 0)

for part in ['bottom', 'left', 'right', 'top']:
    ax[0].spines[part].set_linewidth(0.2)
    ax[1].spines[part].set_linewidth(0.2)

cbar = fig.colorbar(hc, ax=ax, orientation='vertical', shrink=0.6)
cbar.set_label('Pearson correlation $r$', fontsize=7)
cbar.ax.set_yticks([-0.6, 0.0, 1])
cbar.ax.tick_params(labelsize=7, length=0)
cbar.outline.set_linewidth(0.1)

fig.savefig(os.path.join(args.fc_dir, "images", f"{args.thread}_avg_fc_comparison.png"), bbox_inches='tight')

# Plot the significant differences between the average FC matrices, with network boundaries
with open(os.path.join(args.fc_dir, f"{args.thread}_p_vals.csv"), "rb") as f:
    p_vals = np.loadtxt(f, delimiter=',')
with open(os.path.join(args.fc_dir, f"{args.thread}_stats.csv"), "rb") as f:
    stats = np.loadtxt(f, delimiter=',')
with open(os.path.join(args.fc_dir, f"{args.thread}_p_vals_fdr.csv"), "rb") as f:    
    p_vals_fdr = np.loadtxt(f, delimiter=',')

fig, ax = plt.subplots(1, 2, figsize=(14.5*cm,8.96*cm), dpi=600)
hc = ax[0].imshow(avg_hc_fc, cmap="viridis", vmin=-0.6, vmax=1)
ax[0].set_title("Healthy Controls", fontsize=7)
patient = ax[1].imshow(avg_patient_fc, cmap="viridis", vmin=-0.6, vmax=1)
ax[1].set_title("Patients", fontsize=7)

n = len(avg_patient_fc)

start = 0
end = 0
region_centers = []
for net, labels in networks.items():
    end += len(labels)
    if end < 84:
        ax[0].hlines(end-0.5, 0, n-0.5, colors="white", linewidth=0.15)
        ax[0].vlines(end-0.5, 0, n-0.5, colors="white", linewidth=0.15)
        ax[1].hlines(end-0.5, 0, n-0.5, colors="white", linewidth=0.15)
        ax[1].vlines(end-0.5, 0, n-0.5, colors="white", linewidth=0.15)
    region_centers.append(start + (end-start)/2)
    start = end
ax[0].set_yticks(region_centers, network_names, fontsize=7)
ax[0].set_xticks(region_centers, network_names, fontsize=7, rotation=90)
ax[1].set_yticks([])
ax[1].set_xticks(region_centers, network_names, fontsize=7, rotation=90)

for i in range(p_vals.shape[0]):
    for j in range(p_vals.shape[1]):
        if p_vals[i, j] < 0.001:
            if stats[i, j] > 0:
                ax[0].add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=False, edgecolor='red', linewidth=0.5))
                ax[1].add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=False, edgecolor='red', linewidth=0.5))
            if stats[i, j] < 0:
                ax[0].add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=False, edgecolor='cyan', linewidth=0.5))
                ax[1].add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=False, edgecolor='cyan', linewidth=0.5))

ax[0].tick_params(length = 0)
ax[1].tick_params(length = 0)

for part in ['bottom', 'left', 'right', 'top']:
    ax[0].spines[part].set_linewidth(0.2)
    ax[1].spines[part].set_linewidth(0.2)

cbar = fig.colorbar(hc, ax=ax, orientation='vertical', shrink=0.6)
cbar.set_label('Pearson correlation $r$', fontsize=7)
cbar.ax.set_yticks([-0.6, 0.0, 1])
cbar.ax.tick_params(labelsize=7, length=0)
cbar.outline.set_linewidth(0.1)

fig.savefig(os.path.join(args.fc_dir, "images", f"{args.thread}_p_vals_uncorrected.png"), bbox_inches='tight')

# Plot the corrected p-values
fig, ax = plt.subplots(1, 2, figsize=(14.5*cm,8.96*cm), dpi=600)
hc = ax[0].imshow(avg_hc_fc, cmap="viridis", vmin=-0.6, vmax=1)
ax[0].set_title("Healthy Controls", fontsize=7)
patient = ax[1].imshow(avg_patient_fc, cmap="viridis", vmin=-0.6, vmax=1)
ax[1].set_title("Patients", fontsize=7)

n = len(avg_patient_fc)

start = 0
end = 0
region_centers = []
for net, labels in networks.items():
    end += len(labels)
    if end < 84:
        ax[0].hlines(end-0.5, 0, n-0.5, colors="white", linewidth=0.15)
        ax[0].vlines(end-0.5, 0, n-0.5, colors="white", linewidth=0.15)
        ax[1].hlines(end-0.5, 0, n-0.5, colors="white", linewidth=0.15)
        ax[1].vlines(end-0.5, 0, n-0.5, colors="white", linewidth=0.15)
    region_centers.append(start + (end-start)/2)
    start = end
ax[0].set_yticks(region_centers, network_names, fontsize=7)
ax[0].set_xticks(region_centers, network_names, fontsize=7, rotation=90)
ax[1].set_yticks([])
ax[1].set_xticks(region_centers, network_names, fontsize=7, rotation=90)

for i in range(p_vals.shape[0]):
    for j in range(p_vals.shape[1]):
        if p_vals_fdr[i, j] < 0.05:
            if stats[i, j] > 0:
                ax[0].add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=False, edgecolor='red', linewidth=0.5))
                ax[1].add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=False, edgecolor='red', linewidth=0.5))
            if stats[i, j] < 0:
                ax[0].add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=False, edgecolor='cyan', linewidth=0.5))
                ax[1].add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=False, edgecolor='cyan', linewidth=0.5))

ax[0].tick_params(length = 0)
ax[1].tick_params(length = 0)

for part in ['bottom', 'left', 'right', 'top']:
    ax[0].spines[part].set_linewidth(0.2)
    ax[1].spines[part].set_linewidth(0.2)

cbar = fig.colorbar(hc, ax=ax, orientation='vertical', shrink=0.6)
cbar.set_label('Pearson correlation $r$', fontsize=7)
cbar.ax.set_yticks([-0.6, 0.0, 1])
cbar.ax.tick_params(labelsize=7, length=0)
cbar.outline.set_linewidth(0.1)

fig.savefig(os.path.join(args.fc_dir, "images", f"{args.thread}_p_vals_fdr.png"), bbox_inches='tight')