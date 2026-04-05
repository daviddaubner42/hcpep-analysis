import numpy as np
import pandas as pd
import os
import argparse
import pickle

parser = argparse.ArgumentParser(description="Use NSP to calculate a integration and segregation coeffs")
parser.add_argument("--input_dir", type=str, help="The path to the dir with coeffs")
parser.add_argument("--out_dir", type=str, help="The path to dir where the output files will be saved")
parser.add_argument("--subid", type=str)
parser.add_argument("--thread", type=str)
args = parser.parse_args()

with open(os.path.join(args.input_dir, f"sub-{args.subid}_windowed_H_In_{args.thread}.pkl"), "rb") as f:
    H_Ins = pickle.load(f)
with open(os.path.join(args.input_dir, f"sub-{args.subid}_windowed_H_Se_{args.thread}.pkl"), "rb") as f:
    H_Ses = pickle.load(f)

# Calculate integration and segregation strength as average over time
H_In = np.mean(H_Ins)
H_Se = np.mean(H_Ses)

with open(os.path.join(args.out_dir, f"sub-{args.subid}_H_In_{args.thread}.pkl"), "wb") as f:
    pickle.dump(H_In, f)
with open(os.path.join(args.out_dir, f"sub-{args.subid}_H_Se_{args.thread}.pkl"), "wb") as f:
    pickle.dump(H_Se, f)

# Calculate integrationa and segregation variability as standard deviation over time
F_In = np.std(H_Ins)
F_Se = np.std(H_Ses)

with open(os.path.join(args.out_dir, f"sub-{args.subid}_F_In_{args.thread}.pkl"), "wb") as f:
    pickle.dump(F_In, f)
with open(os.path.join(args.out_dir, f"sub-{args.subid}_F_Se_{args.thread}.pkl"), "wb") as f:
    pickle.dump(F_Se, f)