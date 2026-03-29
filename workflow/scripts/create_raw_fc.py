import pandas as pd
import numpy as np
import pickle
import argparse
import nibabel as nib
import os

parser = argparse.ArgumentParser(description="Calculate an FC matrix from a parcellated time series")
parser.add_argument("--ts_dir", type=str, help="The directory with the parcellated time series")
parser.add_argument("--excluded_rois_path", type=str, help="Path to file with regions not to be included in FC calculation")
parser.add_argument("--out_dir", type=str, help="Path to the desired output directory")
parser.add_argument("--subid", type=str)
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

# Calculate the FC matrix
cutoff = 5
ts_AP = ts_AP[cutoff:]
fc = np.corrcoef(ts_AP, rowvar=False)

np.savetxt(os.path.join(args.out_dir, f"sub-{args.subid}_FC_ses-1_dir-AP_raw.csv"), fc, delimiter=',')

""" PA """

# Load the parcellated time series and delete the excluded regions
ts_PA = np.array(nib.load(os.path.join(args.ts_dir, "ses-1", "func", f"sub-{args.subid}_ses-1_task-rest_dir-PA_space-fsLR_seg-Glasser_den-91k_stat-mean_timeseries.ptseries.nii")).dataobj)
ts_PA = np.delete(ts_PA, to_delete, 1)

# Calculate the FC matrix
cutoff = 5
ts_PA = ts_PA[cutoff:]
fc = np.corrcoef(ts_PA, rowvar=False)

np.savetxt(os.path.join(args.out_dir, f"sub-{args.subid}_FC_ses-1_dir-PA_raw.csv"), fc, delimiter=',')

""" Session 1 mean """
ts_1 = (ts_AP + ts_PA) / 2

cutoff = 5
ts_1 = ts_1[cutoff:]
fc = np.corrcoef(ts_1, rowvar=False)

np.savetxt(os.path.join(args.out_dir, f"sub-{args.subid}_FC_ses-1_mean_raw.csv"), fc, delimiter=',')

""" --------- """
""" Session 2 """
""" --------- """

""" AP """
# Load the parcellated time series and delete the excluded regions
ts_AP = np.array(nib.load(os.path.join(args.ts_dir, "ses-2", "func", f"sub-{args.subid}_ses-2_task-rest_dir-AP_space-fsLR_seg-Glasser_den-91k_stat-mean_timeseries.ptseries.nii")).dataobj)
ts_AP = np.delete(ts_AP, to_delete, 1)

# Calculate the FC matrix
cutoff = 5
ts_AP = ts_AP[cutoff:]
fc = np.corrcoef(ts_AP, rowvar=False)

np.savetxt(os.path.join(args.out_dir, f"sub-{args.subid}_FC_ses-2_dir-AP_raw.csv"), fc, delimiter=',')

""" PA """

# Load the parcellated time series and delete the excluded regions
ts_PA = np.array(nib.load(os.path.join(args.ts_dir, "ses-2", "func", f"sub-{args.subid}_ses-2_task-rest_dir-PA_space-fsLR_seg-Glasser_den-91k_stat-mean_timeseries.ptseries.nii")).dataobj)
ts_PA = np.delete(ts_PA, to_delete, 1)

# Calculate the FC matrix
cutoff = 5
ts_PA = ts_PA[cutoff:]
fc = np.corrcoef(ts_PA, rowvar=False)

np.savetxt(os.path.join(args.out_dir, f"sub-{args.subid}_FC_ses-2_dir-PA_raw.csv"), fc, delimiter=',')

""" Session 2 mean """
ts_2 = (ts_AP + ts_PA) / 2

cutoff = 5
ts_2 = ts_2[cutoff:]
fc = np.corrcoef(ts_2, rowvar=False)

np.savetxt(os.path.join(args.out_dir, f"sub-{args.subid}_FC_ses-2_mean_raw.csv"), fc, delimiter=',')

""" --------- """
"""    Mean   """
""" --------- """
ts = (ts_1 + ts_2) / 2

cutoff = 5
ts = ts[cutoff:]
fc = np.corrcoef(ts, rowvar=False)

np.savetxt(os.path.join(args.out_dir, f"sub-{args.subid}_FC_mean_raw.csv"), fc, delimiter=',')
