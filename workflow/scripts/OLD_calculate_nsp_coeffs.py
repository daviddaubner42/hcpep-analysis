import numpy as np
import pandas as pd
import os
import argparse
import pickle
from numpy.linalg import eigh

parser = argparse.ArgumentParser(description="Use NSP to calculate a integration and segregation coeffs")
parser.add_argument("--input", type=str, help="The path to the input FC file")
parser.add_argument("--out_dir", type=str, help="The path to dir where the output files will be saved")
parser.add_argument("--subid", type=str)
parser.add_argument("--thread", type=str)
args = parser.parse_args()

fc = np.loadtxt(args.input, delimiter=',')

# Set negative connectivity to 0
fc[fc < 0] = 0

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

N = module_map.shape[1]
H_In = H_i(0, module_map, eigenvalues) / N
H_Se = np.sum([ H_i(i, module_map, eigenvalues) for i in range(1, len(module_map)) ]) / N

# Save the integration and segregation coeffs
with open(os.path.join(args.out_dir, f"sub-{args.subid}_H_In_{args.thread}.pkl"), "wb") as f:
    pickle.dump(H_In, f)
with open(os.path.join(args.out_dir, f"sub-{args.subid}_H_Se_{args.thread}.pkl"), "wb") as f:
    pickle.dump(H_Se, f)
