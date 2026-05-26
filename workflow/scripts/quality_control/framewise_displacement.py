import os
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib
import scienceplots
import argparse
import json

# Plotting settings

matplotlib.rcParams.update(matplotlib.rcParamsDefault)

plt.style.use(['ieee'])

plt.rcParams.update({
    "text.usetex": False,
    "mathtext.fontset": "stix"
})

cm = 1/2.54

parser = argparse.ArgumentParser(description='Calculate framewise displacement from fmriprep confounds')
parser.add_argument('--derivatives_dir', type=str, required=True, help='Path to the derivatives directory')
parser.add_argument('--output_dir', type=str, required=True, help='Path to the output directory where results will be saved')
parser.add_argument('--subids', type=str, nargs='+', required=True, help='List of subject IDs to process')
args = parser.parse_args()

""" Framewise displacement """

derivatives_dir = args.derivatives_dir

# subids = [i[4:] for i in os.listdir(os.path.join(derivatives_dir, "fmriprep", "sourcedata", "freesurfer")) if i.startswith("sub-")]
subids = args.subids

# assert len(subids) == 81

# table = pd.read_csv(os.path.join(args.output_dir, "desc-qualityControl_summary.tsv"), sep='\t')
# table["Framewise displacement"] = ["Pass" for subid in table["Subject"]]

max_fds_trans = {}
mean_fds_trans = {}
pct_over_soft_trans = {}
pct_over_hard_trans = {}
max_fds_rot = {}
mean_fds_rot = {}
pct_over_soft_rot = {}
pct_over_hard_rot = {}

# Calculate framewise displacement based on motion confounds calculated by fmriprep
for subid in subids:
    for ses in [1, 2]:
        for dir in ['AP', 'PA']:
            warnings = []

            confounds = pd.read_csv(os.path.join(
                derivatives_dir,
                "fmriprep",
                f"sub-{subid}",
                f"ses-{ses}",
                "func",
                f"sub-{subid}_ses-{ses}_task-rest_dir-{dir}_desc-confounds_timeseries.tsv"
            ), sep='\t')

            trans_x = confounds["trans_x"]
            trans_y = confounds["trans_y"]
            trans_z = confounds["trans_z"]

            rot_x = confounds["rot_x"]
            rot_y = confounds["rot_y"]
            rot_z = confounds["rot_z"]

            n_slices = len(trans_x)

            fd_trans = np.array([math.sqrt(float(x) ** 2 + float(y) ** 2 + float(z) ** 2) for x, y, z in zip(trans_x, trans_y, trans_z)])
            fd_rot = np.array([math.sqrt(float(x) ** 2 + float(y) ** 2 + float(z) ** 2) for x, y, z in zip(rot_x, rot_y, rot_z)])

            os.makedirs(f"{args.output_dir}/sub-{subid}/figures", exist_ok=True)

            fig, ax = plt.subplots(1, 2, figsize=(14.5*cm, 5*cm))

            ax[0].plot(range(len(fd_trans)), fd_trans)
            ax[0].set_title("REST Framewise Displacement Translation", fontsize=7)
            ax[0].set_xlabel('frames number', fontsize=7)
            ax[0].set_ylabel('translation (in mm)', fontsize=7)
            ax[0].axhline(y=1.5, color='r', linestyle='--')  
            ax[0].axhline(y=3, color='r', linestyle='-')

            ax[1].plot(range(len(fd_rot)), fd_rot)
            ax[1].set_title("REST Framewise Displacement Rotation", fontsize=7)
            ax[1].set_xlabel('frames number', fontsize=7)
            ax[1].set_ylabel('rotation (in degrees)', fontsize=7)
            ax[1].axhline(y=1.5, color='r', linestyle='--')  
            ax[1].axhline(y=3, color='r', linestyle='-')

            fig.savefig(f"{args.output_dir}/sub-{subid}/figures/sub-{subid}_ses-{ses}_task-rest_dir-{dir}_desc-framewiseDisplacement_figure.png", bbox_inches="tight")
            plt.close()

            np.savetxt(f"{args.output_dir}/sub-{subid}/sub-{subid}_ses-{ses}_task-rest_dir-{dir}_desc-framewiseDisplacementTranslational_timeseries.tsv", fd_trans, delimiter='\t')
            np.savetxt(f"{args.output_dir}/sub-{subid}/sub-{subid}_ses-{ses}_task-rest_dir-{dir}_desc-framewiseDisplacementRotational_timeseries.tsv", fd_rot, delimiter='\t')

            # # Create json sidecar
            # with open("resources/qa_sidecar.json", "rb") as f:
            #     sidecar = json.load(f)

            # sidecar["Sources"] = [f"derivatives:fmriprep:sub-{subid}/func/sub-{subid}_task-rest_desc-confounds_timeseries.tsv"]

            # with open(os.path.join(args.output_dir, f"sub-{subid}/sub-{subid}_task-rest_desc-framewiseDisplacementTranslational_timeseries.json"), "w") as f:
            #     json.dump(sidecar, f)
            # with open(os.path.join(args.output_dir, f"sub-{subid}/sub-{subid}_task-rest_desc-framewiseDisplacementRotational_timeseries.json"), "w") as f:
            #     json.dump(sidecar, f)
            # with open(os.path.join(args.output_dir, f"sub-{subid}/figures/sub-{subid}_task-rest_desc-framewiseDisplacement_figure.json"), "w") as f:
            #     json.dump(sidecar, f)


            if not subid in max_fds_trans:
                max_fds_trans[subid] = {}
            if not ses in max_fds_trans[subid]:
                max_fds_trans[subid][ses] = {}
            max_fds_trans[subid][ses][dir] = np.max(fd_trans)
            if not subid in mean_fds_trans:
                mean_fds_trans[subid] = {}
            if not ses in mean_fds_trans[subid]:
                mean_fds_trans[subid][ses] = {}
            mean_fds_trans[subid][ses][dir] = np.mean(fd_trans)
            if not subid in pct_over_soft_trans:
                pct_over_soft_trans[subid] = {}
            if not ses in pct_over_soft_trans[subid]:
                pct_over_soft_trans[subid][ses] = {}
            pct_over_soft_trans[subid][ses][dir] = len(np.where(fd_trans > 1.5)) / len(fd_trans)
            if not subid in pct_over_hard_trans:
                pct_over_hard_trans[subid] = {}
            if not ses in pct_over_hard_trans[subid]:
                pct_over_hard_trans[subid][ses] = {}
            pct_over_hard_trans[subid][ses][dir] = len(np.where(fd_trans > 3)) / len(fd_trans)
            if not subid in max_fds_rot:
                max_fds_rot[subid] = {}
            if not ses in max_fds_rot[subid]:
                max_fds_rot[subid][ses] = {}
            max_fds_rot[subid][ses][dir] = np.max(fd_rot)
            if not subid in mean_fds_rot:
                mean_fds_rot[subid] = {}
            if not ses in mean_fds_rot[subid]:
                mean_fds_rot[subid][ses] = {}
            mean_fds_rot[subid][ses][dir] = np.mean(fd_rot)
            if not subid in pct_over_soft_rot:
                pct_over_soft_rot[subid] = {}
            if not ses in pct_over_soft_rot[subid]:
                pct_over_soft_rot[subid][ses] = {}
            pct_over_soft_rot[subid][ses][dir] = len(np.where(fd_rot > 1.5)) / len(fd_rot)
            if not subid in pct_over_hard_rot:
                pct_over_hard_rot[subid] = {}
            if not ses in pct_over_hard_rot[subid]:
                pct_over_hard_rot[subid][ses] = {}
            pct_over_hard_rot[subid][ses][dir] = len(np.where(fd_rot > 3)) / len(fd_rot)

            if np.max(fd_trans) >= 3:
                warnings.append(f"ses-{ses}_dir-{dir} Translational framewise displacement crossed the 3mm treshold and should be excluded")
                print(f"sub-{subid} translational framewise displacement {np.max(fd_trans):.2f} crossed the 3mm treshold and should be excluded.")
            elif np.max(fd_trans) >= 1.5:
                print(f"sub-{subid} translational framewise displacement {np.max(fd_trans):.2f} crossed the 1.5mm treshold and should be inspected.")
            
            if np.max(fd_rot) >= 3:
                warnings.append(f"ses-{ses}_dir-{dir} Rotational framewise displacement crossed the 3 degree treshold and should be excluded")
                print(f"sub-{subid} rotational framewise displacement {np.max(fd_rot):.2f} crossed the 3 degree treshold and should be excluded.")
            elif np.max(fd_rot) >= 1.5:
                print(f"sub-{subid} rotational framewise displacement {np.max(fd_rot):.2f} crossed the 1.5 degree treshold and should be inspected.")

            # if len(warnings) > 0:
            #     print(subid)
            #     table.loc[table["Subject"] == subid, "Framewise displacement"] = "Warning: " + "; ".join(warnings)
        
# table.to_csv(os.path.join(args.output_dir, "desc-qualityControl_summary.tsv"), index=False, sep='\t')

rows = []
for subid in subids:
    for ses in [1, 2]:
        for dir in ['AP', 'PA']:
            rows.append({
                "subid": subid,
                "ses": ses,
                "dir": dir,
                "max_fd_trans": max_fds_trans[subid][ses][dir],
                "max_fd_rot": max_fds_rot[subid][ses][dir], 
                "mean_fd_trans": mean_fds_trans[subid][ses][dir],
                "mean_fd_rot": mean_fds_rot[subid][ses][dir],
                "pct_over_soft_trans": pct_over_soft_trans[subid][ses][dir],
                "pct_over_hard_trans": pct_over_hard_trans[subid][ses][dir],
                "pct_over_soft_rot": pct_over_soft_rot[subid][ses][dir],
                "pct_over_hard_rot": pct_over_hard_rot[subid][ses][dir]
            })
df = pd.concat([pd.DataFrame(rows)], ignore_index=True)
df.to_csv(f"{args.output_dir}/task-rest_desc-framewiseDisplacement_summary.tsv", index=False, sep='\t')

fig, ax = plt.subplots(1, 1, figsize=(7.25*cm, 5*cm))

motion = df

for ses in [1, 2]:
    for dir in ['AP', 'PA']:
        ax.scatter([motion[(motion['subid'] == str(subid)) & (motion['ses'] == ses) & (motion['dir'] == dir)].max_fd_trans.item() for subid in subids], [motion[(motion['subid'] == str(subid)) & (motion['ses'] == ses) & (motion['dir'] == dir)].max_fd_rot.item() for subid in subids], s=1, label=f"ses-{ses}_dir-{dir}")
        # ax.scatter([max_fds_trans[subid][ses][dir] for subid in subids], [max_fds_trans[subid][ses][dir] for subid in subids], s=1, label=f"ses-{ses}_dir-{dir}")
ax.set_xlim(0, 3.5)
ax.set_xlabel("Max. translation FD (mm)", fontsize=7)
ax.set_xticklabels([0, 1, 2, 3], fontsize=7)
ax.set_ylim(0, 0.1)
ax.set_ylabel("Max. rotation FD (degrees)", fontsize=7)
ax.set_yticklabels(np.arange(0, 0.06, 0.01), fontsize=7)
ax.vlines([1.5, 3], 0, 0.099, "red", linestyles=["dashed", "solid"], lw=1)
os.makedirs(os.path.join(args.output_dir, "figures"), exist_ok=True)
fig.legend(fontsize=7, loc='upper right', bbox_to_anchor=(1.5, 1))
fig.savefig(f"{args.output_dir}/figures/task-rest_desc-maxFramewiseDisplacementScatter_figure.png", bbox_inches="tight")
plt.close()

# Create json sidecar
# with open("resources/qa_sidecar.json", "rb") as f:
#     sidecar = json.load(f)

# with open(os.path.join(args.output_dir, "desc-qualityControl_summary.json"), "r") as f:
#     table_sidecar = json.load(f)

# sources = []
# table_sources = table_sidecar["Sources"]
# for subid in subids:
#     sources.append(f"derivatives:fmriprep:sub-{subid}/func/sub-{subid}_task-rest_desc-confounds_timeseries.tsv")
#     table_sources.append(f"derivatives:fmriprep:sub-{subid}/func/sub-{subid}_task-rest_desc-confounds_timeseries.tsv")

# sidecar["Sources"] = sources
# table_sidecar["Sources"] = table_sources

# with open(os.path.join(args.output_dir, f"task-rest_desc-framewiseDisplacement_summary.json"), "w") as f:
#     json.dump(sidecar, f)

# with open(os.path.join(args.output_dir, f"figures/task-rest_desc-maxFramewiseDisplacementScatter_figure.json"), "w") as f:
#     json.dump(sidecar, f)

# with open(os.path.join(args.output_dir, f"task-rest_desc-framewiseDisplacement_log.json"), "w") as f:
#     json.dump(sidecar, f)

# with open(os.path.join(args.output_dir, f"desc-qualityControl_summary.json"), "w") as f:
#     json.dump(table_sidecar, f)