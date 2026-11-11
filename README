# HCP-EP analysis pipeline

Defines a Snakemake processing pipeline that calculates static, dynamic, graph theoretic and NSP metrics from XCP-D preprocessed rs-fMRI outputs.

The input directory must contain the following directories with pre-processing outputs:
- `$DATADIR/fmriprep`
- `$DATADIR/xcp-d`
where $DATADIR is the `datadir` specified in the `config/config.yaml`.

The directories specified in `config/config.yaml` need to be changed to match the system the pipeline is running on.

If you want to use different parameters for calculating dynamic FC or graph theoretical metrics, you can change them in `config/config.yaml`.

To run the pipeline, launch a terminal in the `rootdir` specified in the `config/config.yaml` (the one where you cloned this repository), and run `snakemake --cores all --sdm apptainer --singularity-args="--cleanenv -B $DATADIR:$DATADIR -B $ROOTDIR:$ROOTDIR -B $OUTDIR:$OUTDIR"` (or whatever the desired number of cores is).
The singularity arguments clear environmental variables and bind the data and pipeline directories into the container, to avoid naming conflicts inside the containers.

To run the pipeline on a cluster with SLURM scheduling, use the following command
`snakemake --cores all --sdm apptainer --executor slurm --singularity-args="--cleanenv -B $DATADIR:$DATADIR -B $ROOTDIR:$ROOTDIR -B $OUTDIR:$OUTDIR"`