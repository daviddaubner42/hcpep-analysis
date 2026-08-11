import numpy as np
import pandas as pd
import os
import argparse
import pickle
from numpy.linalg import eigh

def create_modules(module_map, level):
    modules = []
    for m in np.unique(module_map[level]):
        module = []
        for i in range(len(module_map[level])):
            if module_map[level, i] == m:
                module.append(i)
        modules.append(module)
    return modules

def H_i(i, module_map, eigenvalues):
    modules = create_modules(module_map, i)
    N = module_map.shape[1]
    M_i = len(modules)
    p_i = np.sum([np.abs(len(m_j) - N/M_i) for m_j in modules]) / N
    return ( eigenvalues[i]**2 * M_i * (1 - p_i) ) / N

parser = argparse.ArgumentParser(description="Use NSP to calculate a integration and segregation coeffs")
parser.add_argument("--input", type=str, help="The path to the input FC file")
parser.add_argument("--out_dir", type=str, help="The path to dir where the output files will be saved")
parser.add_argument("--subid", type=str)
parser.add_argument("--thread", type=str)
args = parser.parse_args()

with open(args.input, "rb") as f:
    fcs = pickle.load(f)

H_Ins = []
H_Ses = []

global_regional_H_Ins, global_regional_H_Ses = [], []

for fc in fcs:
    # Set negative connectivity to 0
    fc[fc < 0] = 0
    np.fill_diagonal(fc, 1)

    eigenvalues, eigenvectors = eigh(fc)

    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    module_map = np.zeros_like(fc)
    n_levels = 0
    for i in range(1, len(fc)):
        eigenmode = eigenvectors[:, i]
        for j in range(len(eigenmode)):
            base = module_map[i-1, j]*2
            if eigenmode[j] > 0:
                module_map[i, j] = base + 0
            else:
                module_map[i, j] = base + 1
        if len(np.unique(module_map[i, :])) == len(fc):
            n_levels = i
            break
    module_map = module_map[:n_levels+1, :]

    N = module_map.shape[1]
    H_1 = H_i(0, module_map, eigenvalues)
    H_In = H_1 / N
    H_Se = np.sum([ H_i(i, module_map, eigenvalues) for i in range(1, len(module_map)) ]) / N

    regional_H_Ins, regional_H_Ses = [], []
    for j in range(len(fc)):
        H_In_j = H_1 * eigenvectors[0, j]**2
        H_Se_j = np.sum([H_i(i, module_map, eigenvalues) * eigenvectors[i, j]**2 for i in range(1, len(module_map))])

        regional_H_Ins.append(H_In_j)
        regional_H_Ses.append(H_Se_j)

    H_Ins.append(H_In)
    H_Ses.append(H_Se)

    global_regional_H_Ins.append(regional_H_Ins)
    global_regional_H_Ses.append(regional_H_Ses)

# Save the integration and segregation coeffs
with open(os.path.join(args.out_dir, f"sub-{args.subid}_windowed_H_In_{args.thread}.pkl"), "wb") as f:
    pickle.dump(H_Ins, f)
with open(os.path.join(args.out_dir, f"sub-{args.subid}_windowed_H_Se_{args.thread}.pkl"), "wb") as f:
    pickle.dump(H_Ses, f)

with open(os.path.join(args.out_dir, f"sub-{args.subid}_windowed_regional_H_In_{args.thread}.pkl"), "wb") as f:
    pickle.dump(global_regional_H_Ins, f)
with open(os.path.join(args.out_dir, f"sub-{args.subid}_windowed_regional_H_Se_{args.thread}.pkl"), "wb") as f:
    pickle.dump(global_regional_H_Ses, f)   
