from fileformats.datascience import DatFile
from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.apply_vol_transform import ApplyVolTransform
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_applyvoltransform_1():
    task = ApplyVolTransform()
    task.inputs.source_file = Nifti1.sample(seed=0)
    task.inputs.target_file = File.sample(seed=2)
    task.inputs.reg_file = DatFile.sample(seed=6)
    task.inputs.lta_file = File.sample(seed=7)
    task.inputs.lta_inv_file = File.sample(seed=8)
    task.inputs.fsl_reg_file = File.sample(seed=9)
    task.inputs.xfm_reg_file = File.sample(seed=10)
    task.inputs.m3z_file = File.sample(seed=17)
    task.inputs.subjects_dir = Directory.sample(seed=20)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_applyvoltransform_2():
    task = ApplyVolTransform()
    task.inputs.source_file = Nifti1.sample(seed=0)
    task.inputs.transformed_file = "struct_warped.nii"
    task.inputs.fs_target = True
    task.inputs.reg_file = DatFile.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
