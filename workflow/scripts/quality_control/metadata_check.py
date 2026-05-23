import nibabel as nib
import os
import json
import pydicom
from os.path import join
import pickle
import argparse
import pandas as pd

""" NIFTI Metadata """
""" We get NIFTI metadata to compare with DICOM, and to check consistency across subjects """

parser = argparse.ArgumentParser(description='Check metadata consistency in the BIDS dataset.')
# parser.add_argument('--dicom_meta', type=str, required=True, help='Path to the DICOM metadata file.')
parser.add_argument('--bids_dir', type=str, required=True, help='Path to the BIDS dataset directory.')
parser.add_argument('--output_dir', type=str, required=True, help='Path to the output directory for QA results.')
args = parser.parse_args()

rawdir = args.bids_dir

subids = [subid[4:] for subid in os.listdir(rawdir) if subid.startswith("sub-")]

table = pd.DataFrame(columns=["Subject", "Metadata Check"])

# Check if files exist
for subid in subids:
    try:
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-1",
            "anat",
            f"sub-{subid}_ses-1_dir-AP_T1w.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-1",
            "anat",
            f"sub-{subid}_ses-1_dir-PA_T1w.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-1",
            "anat",
            f"sub-{subid}_ses-2_dir-AP_T1w.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-1",
            "anat",
            f"sub-{subid}_ses-2_dir-PA_T1w.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-1",
            "anat",
            f"sub-{subid}_ses-1_dir-AP_T2w.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-1",
            "anat",
            f"sub-{subid}_ses-1_dir-PA_T2w.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-2",
            "anat",
            f"sub-{subid}_ses-2_dir-AP_T2w.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-2",
            "anat",
            f"sub-{subid}_ses-2_dir-PA_T2w.nii.gz"
        ))

        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-1",
            "func",
            f"sub-{subid}_ses-1_task-rest_dir-AP_bold.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-1",
            "func",
            f"sub-{subid}_ses-1_task-rest_dir-PA_bold.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-2",
            "func",
            f"sub-{subid}_ses-2_task-rest_dir-AP_bold.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-2",
            "func",
            f"sub-{subid}_ses-2_task-rest_dir-PA_bold.nii.gz"
        ))

        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-1",
            "fmap",
            f"sub-{subid}_ses-1_dir-AP_magnitude1.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-1",
            "fmap",
            f"sub-{subid}_ses-1_dir-PA_magnitude1.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-2",
            "fmap",
            f"sub-{subid}_ses-2_dir-AP_magnitude1.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-2",
            "fmap",
            f"sub-{subid}_ses-2_dir-PA_magnitude1.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-1",
            "fmap",
            f"sub-{subid}_ses-1_dir-AP_magnitude2.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-1",
            "fmap",
            f"sub-{subid}_ses-1_dir-PA_magnitude2.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-2",
            "fmap",
            f"sub-{subid}_ses-2_dir-AP_magnitude2.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-2",
            "fmap",
            f"sub-{subid}_ses-2_dir-PA_magnitude2.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-1",
            "fmap",
            f"sub-{subid}_ses-1_dir-AP_phasediff.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-1",
            "fmap",
            f"sub-{subid}_ses-1_dir-PA_phasediff.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-2",
            "fmap",
            f"sub-{subid}_ses-2_dir-PA_phasediff.nii.gz"
        ))
        assert os.path.exists(os.path.join(
            rawdir,
            f"sub-{subid}",
            "ses-2",
            "fmap",
            f"sub-{subid}_ses-2_dir-PA_phasediff.nii.gz"
        ))
    except AssertionError:
        print(f"sub-{subid} - files missing.")
print("All files present.")

t1_size = (176, 256, 256)
t1_tr = 1.9
t2_sizes = (176, 256, 256)
t2_tr = 6
bold_size = (64, 64, 37, 260)
bold_tr = 2.25
bold_slice_thickness = 3.4

for subid in subids:
    for ses in [1, 2]:
        for dir in ['AP', 'PA']:
            t1 = nib.load(os.path.join(
                rawdir,
                f"sub-{subid}",
                f"ses-{ses}",
                "anat",
                f"sub-{subid}_ses-{ses}_dir-{dir}_T1w.nii.gz"
            ))

            t2 = nib.load(os.path.join(
                rawdir,
                f"sub-{subid}",
                f"ses-{ses}",
                "anat",
                f"sub-{subid}_ses-{ses}_dir-{dir}_T2w.nii.gz"
            ))
            
            bold = nib.load(os.path.join(
                rawdir,
                f"sub-{subid}",
                f"ses-{ses}",
                "func",
                f"sub-{subid}_ses-{ses}_dir-{dir}_task-rest_bold.nii.gz"
            ))

            with open(os.path.join(
                rawdir,
                f"sub-{subid}",
                f"ses-{ses}",
                "func",
                f"sub-{subid}_ses-{ses}_task-rest_dir-{dir}_bold.json"
            )) as f:
                bold_info = json.load(f)
            
            with open(os.path.join(
                rawdir,
                f"sub-{subid}",
                f"ses-{ses}",
                "anat",
                f"sub-{subid}_ses-{ses}_dir-{dir}_T2w.json"
            )) as f:
                t2_info = json.load(f)
            
            with open(os.path.join(
                rawdir,
                f"sub-{subid}",
                f"ses-{ses}",
                "anat",
                f"sub-{subid}_ses-{ses}_dir-{dir}_T1w.json"
            )) as f:
                t1_info = json.load(f)


            # Check if metadata are consistent across subjects
            print(f"sub-{subid}_ses-{ses}_dir-{dir}:")

            warnings = []

            if t1.dataobj.shape != t1_size:
                warnings.append(f"T1w size not matching: {t1.dataobj.shape}")
                print(f"T1w size not matching: {t1.dataobj.shape}")
            if t1_info["RepetitionTime"] != t1_tr:
                warnings.append(f"T1 TR not matching: {t1_info["RepetitionTime"]}")
                print(f"T1 TR not matching: {t1_info["RepetitionTime"]}")

            if t2.dataobj.shape != t2_sizes:
                warnings.append(f"T2w size not matching: {t2.dataobj.shape}")
                print(f"T2w size not matching: {t2.dataobj.shape}")
            if t2_info["RepetitionTime"] != t2_tr:
                warnings.append(f"T2 TR not matching: {t2_info["RepetitionTime"]}")
                print(f"T2 TR not matching: {t2_info["RepetitionTime"]}")

            if bold.dataobj.shape != bold_size:
                warnings.append(f"BOLD size not matching: {bold.dataobj.shape}")
                print(f"BOLD size not matching: {bold.dataobj.shape}")
            if bold_info["RepetitionTime"] != bold_tr:
                warnings.append(f"BOLD TR not matching: {bold_info["RepetitionTime"]}")
                print(f"BOLD TR not matching: {bold_info["RepetitionTime"]}")
            if bold_info["SliceThickness"] != bold_slice_thickness:
                warnings.append(f"BOLD slice thickness not matching: {bold_info["SliceThickness"]}")
                print(f"BOLD slice thickness not matching: {bold_info["SliceThickness"]}")
    

    # Record results in table
    # if len(warnings) == 0:
    #     table = table._append({"Subject": f"sub-{subid}", "Metadata Check": "Pass"}, ignore_index=True)
    # else:
    #     table = table._append({"Subject": f"sub-{subid}", "Metadata Check": "Warning: " + "; ".join(warnings)}, ignore_index=True)
    # table.to_csv(os.path.join(args.output_dir, f"desc-qualityControl_summary.tsv"), sep="\t", index=False)
    

# Create json sidecar
# with open("resources/qa_sidecar.json", "rb") as f:
#     sidecar = json.load(f)

# sources = [f"derivatives:quality_control:/desc-dicomMetadata_summary.pkl"]
# for subid in subids:
#     sources.append(os.path.join(
#         rawdir,
#         f"sub-{subid}",
#         "anat",
#         f"sub-{subid}_T1w.nii.gz"
#     ))

#     with open(os.path.join(args.output_dir, "..", "temp", f"sub-{subid}_bidsfilter.json"), "r") as f:
#         bids_filter = json.load(f)
#     if bids_filter["t2w"]["acquisition"] == "SPACE":
#         sources.append(os.path.join(
#             rawdir,
#             f"sub-{subid}",
#             "anat",
#             f"sub-{subid}_acq-SPACE_T2w.nii.gz"
#         ))
#     elif bids_filter["t2w"]["acquisition"] == "3DSPACE":
#         sources.append(os.path.join(
#             rawdir,
#             f"sub-{subid}",
#             "anat",
#             f"sub-{subid}_acq-3DSPACE_T2w.nii.gz"
#         ))

#     sources.append(os.path.join(
#         rawdir,
#         f"sub-{subid}",
#         "func",
#         f"sub-{subid}_task-rest_bold.nii.gz"
#     ))

# sidecar["Sources"] = sources

# with open(os.path.join(args.output_dir, f"desc-metadataCheck_log.json"), "w") as f:
#     json.dump(sidecar, f)
# with open(os.path.join(args.output_dir, f"desc-qualityControl_summary.json"), "w") as f:
#     json.dump(sidecar, f)