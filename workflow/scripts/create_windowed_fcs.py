import pandas as pd
import numpy as np
import pickle
import argparse
import nibabel as nib
import os

parser = argparse.ArgumentParser(description="Calculate an FC matrix from a parcellated time series")
parser.add_argument("--ts_dir", type=str)
parser.add_argument("--excluded_rois_path", type=str, help="Path to file with regions not to be included in FC calculation")
parser.add_argument("--out_dir", type=str)
parser.add_argument("--subid", type=str)
parser.add_argument("--window_size", type=int, help="The size of the window to be used for calculating windowed FCs")
parser.add_argument("--step_size", type=int, help="The step size to be used for calculating windowed FCs")
args = parser.parse_args()

with open(args.excluded_rois_path, "rb") as f:
    to_delete = pickle.load(f)


""" For each session and direction ... """

""" --------- """
""" Session 1 """
""" --------- """

""" AP """
# Load the parcellated time series and delete the excluded regions
ts_AP = np.array(nib.load(os.path.join(args.ts_dir, "ses-1", "func", f"sub-{args.subid}_ses-1_task-rest_dir-AP_space-fsLR_seg-Glasser_den-91k_stat-mean_timeseries.ptseries.nii")).dataobj)
ts_AP = np.delete(ts_AP, to_delete, 1)

# Calculate the windowed FC matrices
n_windows = len(range(0, ts_AP.shape[0] - args.window_size, args.step_size))
windowed_fcs = []
for i in range(0, ts_AP.shape[0] - args.window_size, args.step_size):
    window_ts = ts_AP[i:i+args.window_size, :]
    fc = np.corrcoef(window_ts, rowvar=False)
    np.fill_diagonal(fc, np.nan)
    windowed_fcs.append(fc)

# Save the windowed FC matrices
with open(os.path.join(args.out_dir, f"sub-{args.subid}_windowed_FCs_ses-1_dir-AP.pkl"), "wb") as f:
    pickle.dump(windowed_fcs, f)

""" PA """

# Load the parcellated time series and delete the excluded regions
ts_PA = np.array(nib.load(os.path.join(args.ts_dir, "ses-1", "func", f"sub-{args.subid}_ses-1_task-rest_dir-PA_space-fsLR_seg-Glasser_den-91k_stat-mean_timeseries.ptseries.nii")).dataobj)
ts_PA = np.delete(ts_PA, to_delete, 1)

# Calculate the windowed FC matrices
n_windows = len(range(0, ts_PA.shape[0] - args.window_size, args.step_size))
windowed_fcs = []
for i in range(0, ts_PA.shape[0] - args.window_size, args.step_size):
    window_ts = ts_PA[i:i+args.window_size, :]
    fc = np.corrcoef(window_ts, rowvar=False)
    np.fill_diagonal(fc, np.nan)
    windowed_fcs.append(fc)

# Save the windowed FC matrices
with open(os.path.join(args.out_dir, f"sub-{args.subid}_windowed_FCs_ses-1_dir-PA.pkl"), "wb") as f:
    pickle.dump(windowed_fcs, f)

""" Session 1 mean """
ts_1 = (ts_AP + ts_PA) / 2

# Calculate the windowed FC matrices
n_windows = len(range(0, ts_1.shape[0] - args.window_size, args.step_size))
windowed_fcs = []
for i in range(0, ts_1.shape[0] - args.window_size, args.step_size):
    window_ts = ts_1[i:i+args.window_size, :]
    fc = np.corrcoef(window_ts, rowvar=False)
    np.fill_diagonal(fc, np.nan)
    windowed_fcs.append(fc)

# Save the windowed FC matrices
with open(os.path.join(args.out_dir, f"sub-{args.subid}_windowed_FCs_ses-1_mean.pkl"), "wb") as f:
    pickle.dump(windowed_fcs, f)

""" --------- """
""" Session 2 """
""" --------- """

""" AP """
# Load the parcellated time series and delete the excluded regions
ts_AP = np.array(nib.load(os.path.join(args.ts_dir, "ses-2", "func", f"sub-{args.subid}_ses-2_task-rest_dir-AP_space-fsLR_seg-Glasser_den-91k_stat-mean_timeseries.ptseries.nii")).dataobj)
ts_AP = np.delete(ts_AP, to_delete, 1)

# Calculate the windowed FC matrices
n_windows = len(range(0, ts_AP.shape[0] - args.window_size, args.step_size))
windowed_fcs = []
for i in range(0, ts_AP.shape[0] - args.window_size, args.step_size):
    window_ts = ts_AP[i:i+args.window_size, :]
    fc = np.corrcoef(window_ts, rowvar=False)
    np.fill_diagonal(fc, np.nan)
    windowed_fcs.append(fc)

# Save the windowed FC matrices
with open(os.path.join(args.out_dir, f"sub-{args.subid}_windowed_FCs_ses-2_dir-AP.pkl"), "wb") as f:
    pickle.dump(windowed_fcs, f)

""" PA """

# Load the parcellated time series and delete the excluded regions
ts_PA = np.array(nib.load(os.path.join(args.ts_dir, "ses-2", "func", f"sub-{args.subid}_ses-2_task-rest_dir-PA_space-fsLR_seg-Glasser_den-91k_stat-mean_timeseries.ptseries.nii")).dataobj)
ts_PA = np.delete(ts_PA, to_delete, 1)

# Calculate the windowed FC matrices
n_windows = len(range(0, ts_PA.shape[0] - args.window_size, args.step_size))
windowed_fcs = []
for i in range(0, ts_PA.shape[0] - args.window_size, args.step_size):
    window_ts = ts_PA[i:i+args.window_size, :]
    fc = np.corrcoef(window_ts, rowvar=False)
    np.fill_diagonal(fc, np.nan)
    windowed_fcs.append(fc)

# Save the windowed FC matrices
with open(os.path.join(args.out_dir, f"sub-{args.subid}_windowed_FCs_ses-2_dir-PA.pkl"), "wb") as f:
    pickle.dump(windowed_fcs, f)

""" Session 2 mean """
ts_2 = (ts_AP + ts_PA) / 2

# Calculate the windowed FC matrices
n_windows = len(range(0, ts_2.shape[0] - args.window_size, args.step_size))
windowed_fcs = []
for i in range(0, ts_2.shape[0] - args.window_size, args.step_size):
    window_ts = ts_2[i:i+args.window_size, :]
    fc = np.corrcoef(window_ts, rowvar=False)
    np.fill_diagonal(fc, np.nan)
    windowed_fcs.append(fc)

# Save the windowed FC matrices
with open(os.path.join(args.out_dir, f"sub-{args.subid}_windowed_FCs_ses-2_mean.pkl"), "wb") as f:
    pickle.dump(windowed_fcs, f)

""" --------- """
"""    Mean   """
""" --------- """
ts = (ts_1 + ts_2) / 2

# Calculate the windowed FC matrices
n_windows = len(range(0, ts.shape[0] - args.window_size, args.step_size))
windowed_fcs = []
for i in range(0, ts.shape[0] - args.window_size, args.step_size):
    window_ts = ts[i:i+args.window_size, :]
    fc = np.corrcoef(window_ts, rowvar=False)
    np.fill_diagonal(fc, np.nan)
    windowed_fcs.append(fc)

# Save the windowed FC matrices
with open(os.path.join(args.out_dir, f"sub-{args.subid}_windowed_FCs_mean.pkl"), "wb") as f:
    pickle.dump(windowed_fcs, f)