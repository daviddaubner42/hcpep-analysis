import numpy as np
import pandas as pd
import os
import argparse
import pickle

parser = argparse.ArgumentParser(description="Use NSP to calculate a integration and segregation coeffs")
parser.add_argument("--inp_dir", type=str, help="The path to the directory with NSP coeffs")
parser.add_argument("--out_dir", type=str, help="The path to dir where the output files will be saved")
parser.add_argument("--subids", nargs="+", type=str)
parser.add_argument("--thread", type=str)
parser.add_argument("--demo_data_path", type=str, help="Path to the demographic data")
args = parser.parse_args()

# Load the demographic data
demo_data = pd.read_table(args.demo_data_path)

nsp_coeffs = {}
for subid in args.subids:
    with open(os.path.join(args.inp_dir, f"sub-{subid}", f"sub-{subid}_H_In_{{thread}}.pkl"), "rb") as f:
        H_In = pickle.load(f)
    with open(os.path.join(args.inp_dir, f"sub-{subid}", f"sub-{subid}_H_Se_{{thread}}.pkl"), "rb") as f:
        H_Se = pickle.load(f)
    with open(os.path.join(args.inp_dir, f"sub-{subid}", f"sub-{subid}_F_In_{{thread}}.pkl"), "rb") as f:
        F_In = pickle.load(f)
    with open(os.path.join(args.inp_dir, f"sub-{subid}", f"sub-{subid}_F_Se_{{thread}}.pkl"), "rb") as f:
        F_Se = pickle.load(f)
    
    nsp_coeffs[subid] = {
        "subid": subid,
        "patient": demo_data[demo_data["src_subject_id"] == subid].phenotype.item() == "Patient",
        "H_In": H_In,
        "H_Se": H_Se,
        "F_In": F_In,
        "F_Se": F_Se
    }

# Save the aggregated metrics to a csv file
nsp_coeffs_df = pd.DataFrame.from_dict(nsp_coeffs, orient='index')
nsp_coeffs_df.to_csv(os.path.join(args.out_dir, f"nsp_coeffs_{args.thread}.csv"), index=False)