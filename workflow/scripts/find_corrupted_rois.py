import nibabel as nib
import numpy as np
import argparse
import pickle

parser = argparse.ArgumentParser(description="Find the ROIs for which mean timeseries could not be calculated")
parser.add_argument("--ts", type=str, help="The path to the timeseries")
parser.add_argument("--out_path", type=str, help="Path where excluded ROIs list should be stored")
args = parser.parse_args()

ts = np.array(nib.load(args.ts).dataobj)

to_delete = []
for i in range(ts.shape[1]):
    if np.all(np.isnan(ts[:, i])):
        to_delete.append(i)

with open(args.out_path, "wb") as f:
    pickle.dump(to_delete, f)