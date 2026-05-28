import os
import nibabel as nib
import pandas as pd
import numpy as np
import pickle
import argparse

parser = argparse.ArgumentParser(description="Create the files describing ROIs and networks they belong to")
parser.add_argument("--seg_file", type=str, help="The path to the atlas segmentation file")
parser.add_argument("--ts_dir", type=str, help="The path to the timeseries directory")
parser.add_argument("--subids", type=str, nargs="+")
parser.add_argument("--motion_summary", type=str)
parser.add_argument("--out_dir", type=str, help="Path to directory where results should be stored")
parser.add_argument("--community", type=str)
args = parser.parse_args()

to_delete_global = {}

# Identify corrupted ROIs
for ses in [1, 2]:
    for dir in ['AP', 'PA']:

        # Find excluded participants for this thread
        motion = pd.read_csv(args.motion_summary, sep="\t")

        excluded = []

        thread_ses = ses
        thread_dir = ses
        for i in range(len(motion)):
            subid = motion.loc[i, "subid"]
            cur_ses = motion.loc[i, "ses"]
            cur_dir = motion.loc[i, "dir"]
            max_fds_trans = motion.loc[i, "max_fd_trans"]
            max_fds_rot = motion.loc[i, "max_fd_rot"]
            if max_fds_trans > 3 or max_fds_rot > 3:
                if cur_ses == thread_ses:
                    if cur_dir == thread_dir:
                        excluded.append(int(subid))

        subids = [subid for subid in args.subids if subid not in excluded]
        
        for subid in subids:
            ts = np.array(nib.load(os.path.join(args.ts_dir, f"sub-{subid}", f"ses-{ses}", "func", f"sub-{subid}_ses-{ses}_task-rest_dir-{dir}_space-fsLR_seg-Glasser_den-91k_stat-mean_timeseries.ptseries.nii").dataobj))

        to_delete = []
        for i in range(ts.shape[1]):
            if np.all(np.isnan(ts[:, i])):
                to_delete.append(i)
        
        to_delete_global[f"ses-{ses}_dir-{dir}"] = to_delete

with open(os.path.join(args.out_dir, "to_delete.pkl"), "wb") as f:
    pickle.dump(to_delete_global, f)

# Load atlas label table
atlas_desc = pd.read_table(args.seg_file)

# Delete corrupted ROIs
atlas_desc = atlas_desc.drop(to_delete, axis=0)
atlas_desc['index'] = np.arange(0, len(atlas_desc))
atlas_desc.set_index('index', inplace=True)

# Save labels
atlas_labels = list(atlas_desc['label'])
with open(os.path.join(args.out_dir, 'labels.pkl'), "wb") as f:
    pickle.dump(atlas_labels, f)

# Get regions belonging to each network
networks = {}
network_idxs = {}
for network in np.unique(atlas_desc[f'community_{args.community}']):
    networks[network] = list(atlas_desc[atlas_desc[f'community_{args.community}'] == network].label)
    network_idxs[network] = list(atlas_desc[atlas_desc[f'community_{args.community}'] == network].index)

# Create a partition to be used for modularity and participation coefficient calculation
partition = []
partition_idxs = []
for network, labels in networks.items():
    partition.append(set(labels))
for network, idxs in network_idxs.items():
    partition_idxs.append(set(idxs))

# Save the results
outdir = args.out_dir
os.makedirs(outdir, exist_ok=True)

with open(f'{outdir}/networks.pkl', 'wb') as f:
    pickle.dump(networks, f)
with open(f'{outdir}/network_idxs.pkl', 'wb') as f:
    pickle.dump(network_idxs, f)
with open(f'{outdir}/partition.pkl', 'wb') as f:
    pickle.dump(partition, f)
with open(f'{outdir}/partition_idxs.pkl', 'wb') as f:
    pickle.dump(partition, f)