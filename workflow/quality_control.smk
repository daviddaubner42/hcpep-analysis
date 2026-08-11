""" Quality assurance procedure rules """

# rule create_data_description_qa:
#     input:
#         os.path.join("resources", "dataset_description_qa.json")
#     params:
#         workflowdir = workflowdir,
#         outdir = outdir
#     output:
#         os.path.join(outdir, "quality_control", "dataset_description.json")
#     conda:
#         os.path.join(environmentdir, "environment.yaml")
#     shell:
#         "mkdir -p {params.outdir}/quality_control && "
#         "cp {input} {output}"

# rule get_dicom_metadata:
#     input:
#         os.path.join(outdir, "dicom", "LE_GK_010_1_", "20120707_PAUL_KOPF", "MR_Seq._10_FieldMapping_BOLD", "0000.dcm")
#     params:
#         dicomdir=os.path.join(outdir, "dicom"),
#         outdir=outdir,
#         workflowdir=workflowdir
#     output:
#         os.path.join(outdir, "quality_control", "desc-dicomMetadata_summary.pkl"),
#         os.path.join(outdir, "quality_control", "desc-dicomMetadata_summary.json"),
#         os.path.join(outdir, "quality_control", "desc-getDicomMetadata_log.txt"),
#         os.path.join(outdir, "quality_control", "desc-getDicomMetadata_log.json")
#     conda:
#         os.path.join(environmentdir, "environment.yaml")
#     shell:
#         "mkdir -p {params.outdir}/quality_control && "
#         "python {params.workflowdir}/scripts/quality_control/get_dicom_metadata.py --dicom_dir {params.dicomdir} --output_dir {params.outdir}/quality_control > {params.outdir}/quality_control/desc-getDicomMetadata_log.txt"

rule metadata_check:
    input:
        # os.path.join(outdir, "quality_control", "desc-dicomMetadata_summary.pkl"),
        expand(os.path.join(rawdir, "BIDS", "sub-{subid}", "ses-1", "func", "sub-{subid}_ses-1_task-rest_dir-AP_bold.nii.gz"), subid=subids)
    params:
        outdir=outdir,
        workflowdir=workflowdir,
        rawdir=rawdir
    output:
        os.path.join(outdir, "quality_control", "desc-metadataCheck_log.txt"),
        # os.path.join(outdir, "quality_control", "desc-metadataCheck_log.json"),
        # os.path.join(outdir, "quality_control", "desc-qualityControl_summary.tsv"),
        # os.path.join(outdir, "quality_control", "desc-qualityControl_summary.json")
    conda:
        os.path.join(environmentdir, "environment.yaml")
    shell:
        "python {params.workflowdir}/scripts/quality_control/metadata_check.py --bids_dir {params.rawdir} --output_dir {params.outdir}/quality_control > {output[0]}"

rule framewise_displacement:
    input:
        expand(os.path.join(outdir, "fmriprep", "sub-{subid}", "ses-1", "func", "sub-{subid}_ses-1_task-rest_dir-AP_desc-confounds_timeseries.tsv"), subid=subids),
        # os.path.join(outdir, "quality_control", "desc-qualityControl_summary.tsv")
    params:
        outdir=outdir,
        workflowdir=workflowdir,
        subids=subids
    output:
        expand([os.path.join(outdir, "quality_control", "sub-{subid}", "figures", "sub-{subid}_ses-1_task-rest_dir-AP_desc-framewiseDisplacement_figure.png"),
        # os.path.join(outdir, "quality_control", "sub-{subid}", "figures", "sub-{subid}_task-rest_desc-framewiseDisplacement_figure.json"),
        os.path.join(outdir, "quality_control", "sub-{subid}", "sub-{subid}_ses-1_task-rest_dir-AP_desc-framewiseDisplacementTranslational_timeseries.tsv"),
        # os.path.join(outdir, "quality_control", "sub-{subid}", "sub-{subid}_task-rest_desc-framewiseDisplacementTranslational_timeseries.json"),
        os.path.join(outdir, "quality_control", "sub-{subid}", "sub-{subid}_ses-1_task-rest_dir-AP_desc-framewiseDisplacementRotational_timeseries.tsv")], subid=subids),
        # os.path.join(outdir, "quality_control", "sub-{subid}", "sub-{subid}_task-rest_desc-framewiseDisplacementRotational_timeseries.json")], subid=subids),
        os.path.join(outdir, "quality_control", "task-rest_desc-framewiseDisplacement_summary.tsv"),
        # os.path.join(outdir, "quality_control", "task-rest_desc-framewiseDisplacement_summary.json"),
        os.path.join(outdir, "quality_control", "figures", "task-rest_desc-maxFramewiseDisplacementScatter_figure.png"),
        # os.path.join(outdir, "quality_control", "figures", "task-rest_desc-maxFramewiseDisplacementScatter_figure.json"),
        os.path.join(outdir, "quality_control", "task-rest_desc-framewiseDisplacement_log.txt"),
        # os.path.join(outdir, "quality_control", "task-rest_desc-framewiseDisplacement_log.json")
    conda:
        os.path.join(environmentdir, "environment.yaml")
    shell:
        "mkdir -p {params.outdir}/quality_control/figures && "
        "python {params.workflowdir}/scripts/quality_control/framewise_displacement.py --derivatives_dir {params.outdir} --output_dir {params.outdir}/quality_control --subids {params.subids} > {params.outdir}/quality_control/task-rest_desc-framewiseDisplacement_log.txt"

# rule denoising_verification:
#     input:
#         expand(os.path.join(outdir, "xcp_d", "sub-{subid}", "func", "sub-{subid}_task-rest_space-fsLR_seg-DesikanKilliany_den-91k_stat-mean_timeseries.ptseries.nii"), subid=subids),
#         expand(os.path.join(outdir, "quality_control", "sub-{subid}", "sub-{subid}_task-rest_desc-framewiseDisplacementTranslational_timeseries.tsv"), subid=subids),
#         expand(os.path.join(outdir, "atlases", "sub-{subid}", "atlas-DesikanKilliany", "atlas-DesikanKilliany_space-fsLR_den-32k_dseg.dlabel.nii"), subid=subids)
#     params:
#         outdir=outdir,
#         workflowdir=workflowdir
#     output:
#         expand([os.path.join(outdir, "quality_control", "sub-{subid}", "figures", "sub-{subid}_task-rest_desc-rawVsClean_figure.png"),
#         os.path.join(outdir, "quality_control", "sub-{subid}", "figures", "sub-{subid}_task-rest_desc-rawVsClean_figure.json")], subid=subids),
#         os.path.join(outdir, "quality_control", "task-rest_desc-denoisingVerification_log.txt"),
#         os.path.join(outdir, "quality_control", "task-rest_desc-denoisingVerification_log.json")
#     # container:
#     #     config["containers"]["wb_command"]
#     conda:
#         os.path.join(environmentdir, "environment.yaml")
#     shell:
#         "python {params.workflowdir}/scripts/quality_control/denoising_verification.py --derivatives_dir {params.outdir} --output_dir {params.outdir}/quality_control > {params.outdir}/quality_control/task-rest_desc-denoisingVerification_log.txt"

rule qc_fc:
    input:
        os.path.join(outdir, "quality_control", "task-rest_desc-framewiseDisplacement_summary.tsv"),
        os.path.join(resourcedir, "atlas-Glasser_dseg.tsv"),
        os.path.join(resourcedir, "glasser_region_coords.csv"),
        os.path.join(outdir, "intermediaries", "to_delete.pkl"),
        expand(os.path.join(outdir, "static", "sub-{subid}", "sub-{subid}_FC_{thread}_raw.csv"), subid=subids, thread=threads)
    params:
        outdir=outdir,
        workflowdir=workflowdir,
        subids=subids
    output:
        os.path.join(outdir, "quality_control", "figures", "ses-1_task-rest_dir-AP_desc-qcFcCorrelationHistograms_figure.png"),
        os.path.join(outdir, "quality_control", "figures", "ses-2_task-rest_dir-AP_desc-qcFcCorrelationHistograms_figure.png"),
        os.path.join(outdir, "quality_control", "figures", "ses-1_task-rest_dir-PA_desc-qcFcCorrelationHistograms_figure.png"),
        os.path.join(outdir, "quality_control", "figures", "ses-2_task-rest_dir-PA_desc-qcFcCorrelationHistograms_figure.png"),
        # os.path.join(outdir, "quality_control", "figures", "ses-1_task-rest_dir-AP_desc-qcFcCorrelationHistograms_figure.json"),
        # os.path.join(outdir, "quality_control", "figures", "ses-2_task-rest_dir-AP_desc-qcFcCorrelationHistograms_figure.json"),
        # os.path.join(outdir, "quality_control", "figures", "ses-1_task-rest_dir-PA_desc-qcFcCorrelationHistograms_figure.json"),
        # os.path.join(outdir, "quality_control", "figures", "ses-2_task-rest_dir-PA_desc-qcFcCorrelationHistograms_figure.json"),
        os.path.join(outdir, "quality_control", "figures", "ses-1_task-rest_dir-AP_desc-qcFcDistanceCorrelation_figure.png"),
        os.path.join(outdir, "quality_control", "figures", "ses-2_task-rest_dir-AP_desc-qcFcDistanceCorrelation_figure.png"),
        os.path.join(outdir, "quality_control", "figures", "ses-1_task-rest_dir-PA_desc-qcFcDistanceCorrelation_figure.png"),
        os.path.join(outdir, "quality_control", "figures", "ses-2_task-rest_dir-PA_desc-qcFcDistanceCorrelation_figure.png"),
        # os.path.join(outdir, "quality_control", "figures", "ses-1_task-rest_dir-AP_desc-qcFcDistanceCorrelation_figure.json"),
        # os.path.join(outdir, "quality_control", "figures", "ses-2_task-rest_dir-AP_desc-qcFcDistanceCorrelation_figure.json"),
        # os.path.join(outdir, "quality_control", "figures", "ses-1_task-rest_dir-PA_desc-qcFcDistanceCorrelation_figure.json"),
        # os.path.join(outdir, "quality_control", "figures", "ses-2_task-rest_dir-PA_desc-qcFcDistanceCorrelation_figure.json"),
        os.path.join(outdir, "quality_control", "task-rest_desc-qcFc_log.txt"),
    conda:
        os.path.join(environmentdir, "environment.yaml")
    shell:
        "python {params.workflowdir}/scripts/quality_control/qc_fc.py --motion_summary {input[0]} --atlas_tsv {input[1]} --region_coords {input[2]} --excluded_rois_path {input[3]} --fc_dir {params.outdir}/static/ --output_dir {params.outdir}/quality_control --subids {params.subids} > {params.outdir}/quality_control/task-rest_desc-qcFc_log.txt"