import os
import nibabel as nib
import pandas as pd
import numpy as np
import pickle
import argparse

parser = argparse.ArgumentParser(description="Create the files describing ROIs and networks they belong to")
parser.add_argument("--seg_file", type=str, help="The path to the atlas segmentation file")
parser.add_argument("--ts", type=str, help="The path to the timeseries")
parser.add_argument("--out_dir", type=str, help="Path to directory where results should be stored")
parser.add_argument("--community", type=str)
args = parser.parse_args()

# Identify corrupted ROIs
ts = np.array(nib.load(args.ts).dataobj)

to_delete = []
for i in range(ts.shape[1]):
    if np.all(np.isnan(ts[:, i])):
        to_delete.append(i)

with open(os.path.join(args.out_dir, "to_delete.pkl"), "wb") as f:
    pickle.dump(to_delete, f)

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