import os
import sys

import subprocess as sp
from tempfile import TemporaryDirectory
import shutil
from pathlib import Path, PurePosixPath

sys.path.insert(0, os.path.dirname(__file__))

import common


def test_ome_zarr_to_nii():

    with TemporaryDirectory() as tmpdir:
        workdir = Path(tmpdir) / "workdir"
        data_path = PurePosixPath(".tests/unit/ome_zarr_to_nii/data")
        expected_path = PurePosixPath(".tests/unit/ome_zarr_to_nii/expected")

        # Copy data to the temporary workdir.
        shutil.copytree(data_path, workdir)

        # dbg
        print("bids/derivatives/resampled/sub-mouse1/micr/sub-mouse1_sample-brain_acq-blaze1x_stain-abeta_res-3x_SPIM.nii", file=sys.stderr)

        # Run the test job.
        sp.check_output([
            "python",
            "-m",
            "snakemake", 
            "bids/derivatives/resampled/sub-mouse1/micr/sub-mouse1_sample-brain_acq-blaze1x_stain-abeta_res-3x_SPIM.nii",
            "-f", 
            "-j1",
            "--target-files-omit-workdir-adjustment",
			"--use-singularity",
    
            "--directory",
            workdir,
        ])

        # Check the output byte by byte using cmp.
        # To modify this behavior, you can inherit from common.OutputChecker in here
        # and overwrite the method `compare_files(generated_file, expected_file), 
        # also see common.py.
        common.OutputChecker(data_path, expected_path, workdir).check()
