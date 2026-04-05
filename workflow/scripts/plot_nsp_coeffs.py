import matplotlib.pyplot as plt
import matplotlib
import pickle
import scienceplots
import os
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Plot the comparison of NSP coeffs between patient patients and healthy controls")
parser.add_argument("--inp_dir", type=str, help="The path to the directory with the NSP coeffs")
parser.add_argument("--thread", type=str)
args = parser.parse_args()

# Plotting settings
matplotlib.rcParams.update(matplotlib.rcParamsDefault)
plt.style.use(['ieee'])
plt.rcParams.update({
    "text.usetex": False,
    "font.family": "serif"
})

cm = 1/2.54

# Load the NSP coeffs data
nsp_coeffs = pd.read_csv(os.path.join(args.inp_dir, f"nsp_coeffs_{args.thread}.csv"))
with open(os.path.join(args.inp_dir, f"nsp_coeffs_ps_{args.thread}.pkl"), "rb") as f:
    ps = pickle.load(f)
with open(os.path.join(args.inp_dir, f"nsp_coeffs_stats_{args.thread}.pkl"), "rb") as f:
    stats = pickle.load(f)

fig, ax = plt.subplots(4, 2, figsize=(14.5*cm, 14.5*cm), dpi=600)

patients = []
hcs = []

metric = 'H_In'

for subid in nsp_coeffs["subid"]:
    if nsp_coeffs[nsp_coeffs["subid"] == subid]["patient"].item() == 1:
        patients.append(nsp_coeffs[nsp_coeffs["subid"] == subid][metric].item())
    else:
        hcs.append(nsp_coeffs[nsp_coeffs["subid"] == subid][metric].item())

patient_idxs = 2*np.ones(len(patients))
hc_idxs = np.ones(len(hcs))
idxs = np.concatenate([hc_idxs, patient_idxs])

ax[0][0].violinplot([hcs, patients], showmeans=True, showextrema=False)
ax[0][0].scatter(idxs, np.concatenate([hcs, patients]), s=3, color=(0, 0, 0, 0.2))
ax[0][0].tick_params(labelsize=9)
ax[0][0].set_xticks([1, 2], ["Healthy Controls", "Patients"], fontsize=9)
ax[0][0].set_ylabel("Integration strength $H_In$", fontsize=9)

if ps[metric] < 0.05:
    ymax = max(np.max(patients), np.max(hcs))
    y_offset = ymax / 10
    ax[0][0].plot([1, 1, 2, 2], [ymax, ymax + y_offset, ymax + y_offset, ymax], color='black')
    ax[0][0].set_facecolor("#eeebeb")
    ax[0][0].text(1.5, ymax + y_offset + 0.1, '*', fontsize=16, ha='center')
if ps[metric] < 0.05 / 10:
    ax[0][0].text(1.5, ymax + y_offset + 0.2, '*', fontsize=16, ha='center')
if ps[metric] < 0.05 / 100:
    ax[0][0].text(1.5, ymax + y_offset + 0.3, '*', fontsize=16, ha='center')

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

patients = []
hcs = []

metric = 'H_Se'

for subid in nsp_coeffs["subid"]:
    if nsp_coeffs[nsp_coeffs["subid"] == subid]["patient"].item() == 1:
        patients.append(nsp_coeffs[nsp_coeffs["subid"] == subid][metric].item())
    else:
        hcs.append(nsp_coeffs[nsp_coeffs["subid"] == subid][metric].item())

patient_idxs = 2*np.ones(len(patients))
hc_idxs = np.ones(len(hcs))
idxs = np.concatenate([hc_idxs, patient_idxs])

ax[0][1].violinplot([hcs, patients], showmeans=True, showextrema=False)
ax[0][1].scatter(idxs, np.concatenate([hcs, patients]), s=3, color=(0, 0, 0, 0.2))
ax[0][1].tick_params(labelsize=9)
ax[0][1].set_xticks([1, 2], ["Healthy Controls", "Patients"], fontsize=9)
ax[0][1].set_ylabel("Segregation strength $H_Se$", fontsize=9)

if ps[metric] < 0.05:
    ymax = max(np.max(patients), np.max(hcs))
    y_offset = ymax / 10
    ax[0][1].plot([1, 1, 2, 2], [ymax, ymax + y_offset, ymax + y_offset, ymax], color='black')
    ax[0][1].set_facecolor("#eeebeb")
    ax[0][1].text(1.5, ymax + y_offset + 0.1, '*', fontsize=16, ha='center')
if ps[metric] < 0.05 / 10:
    ax[0][1].text(1.5, ymax + y_offset + 0.2, '*', fontsize=16, ha='center')
if ps[metric] < 0.05 / 100:
    ax[0][1].text(1.5, ymax + y_offset + 0.3, '*', fontsize=16, ha='center')

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

patients = []
hcs = []

metric = 'F_In'

for subid in nsp_coeffs["subid"]:
    if nsp_coeffs[nsp_coeffs["subid"] == subid]["patient"].item() == 1:
        patients.append(nsp_coeffs[nsp_coeffs["subid"] == subid][metric].item())
    else:
        hcs.append(nsp_coeffs[nsp_coeffs["subid"] == subid][metric].item())

patient_idxs = 2*np.ones(len(patients))
hc_idxs = np.ones(len(hcs))
idxs = np.concatenate([hc_idxs, patient_idxs])

ax[1][0].violinplot([hcs, patients], showmeans=True, showextrema=False)
ax[1][0].scatter(idxs, np.concatenate([hcs, patients]), s=3, color=(0, 0, 0, 0.2))
ax[1][0].tick_params(labelsize=9)
ax[1][0].set_xticks([1, 2], ["Healthy Controls", "Patients"], fontsize=9)
ax[1][0].set_ylabel("Integration strength $F_In$", fontsize=9)

if ps[metric] < 0.05:
    ymax = max(np.max(patients), np.max(hcs))
    y_offset = ymax / 10
    ax[1][0].plot([1, 1, 2, 2], [ymax, ymax + y_offset, ymax + y_offset, ymax], color='black')
    ax[1][0].set_facecolor("#eeebeb")
    ax[1][0].text(1.5, ymax + y_offset + 0.1, '*', fontsize=16, ha='center')
if ps[metric] < 0.05 / 10:
    ax[1][0].text(1.5, ymax + y_offset + 0.2, '*', fontsize=16, ha='center')
if ps[metric] < 0.05 / 100:
    ax[1][0].text(1.5, ymax + y_offset + 0.3, '*', fontsize=16, ha='center')

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

patients = []
hcs = []

metric = 'F_Se'

for subid in nsp_coeffs["subid"]:
    if nsp_coeffs[nsp_coeffs["subid"] == subid]["patient"].item() == 1:
        patients.append(nsp_coeffs[nsp_coeffs["subid"] == subid][metric].item())
    else:
        hcs.append(nsp_coeffs[nsp_coeffs["subid"] == subid][metric].item())


patient_idxs = 2*np.ones(len(patients))
hc_idxs = np.ones(len(hcs))
idxs = np.concatenate([hc_idxs, patient_idxs])

ax[1][1].violinplot([hcs, patients], showmeans=True, showextrema=False)
ax[1][1].scatter(idxs, np.concatenate([hcs, patients]), s=3, color=(0, 0, 0, 0.2))
ax[1][1].tick_params(labelsize=9)
ax[1][1].set_xticks([1, 2], ["Healthy Controls", "Patients"], fontsize=9)
ax[1][1].set_ylabel("Segregation strength $F_Se$", fontsize=9)

if ps[metric] < 0.05:
    ymax = max(np.max(patients), np.max(hcs))
    y_offset = ymax / 10
    ax[1][1].plot([1, 1, 2, 2], [ymax, ymax + y_offset, ymax + y_offset, ymax], color='black')
    ax[1][1].set_facecolor("#eeebeb")
    ax[1][1].text(1.5, ymax + y_offset + 0.1, '*', fontsize=16, ha='center')
if ps[metric] < 0.05 / 10:
    ax[1][1].text(1.5, ymax + y_offset + 0.2, '*', fontsize=16, ha='center')
if ps[metric] < 0.05 / 100:
    ax[1][1].text(1.5, ymax + y_offset + 0.3, '*', fontsize=16, ha='center')

plt.tight_layout()
plt.savefig(os.path.join(args.inp_dir, "images", f"nsp_coeffs_comparison_{args.thread}.png"), bbox_inches='tight')