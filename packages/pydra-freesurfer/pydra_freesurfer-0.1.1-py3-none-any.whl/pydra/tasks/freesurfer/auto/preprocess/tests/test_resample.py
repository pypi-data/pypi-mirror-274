from fileformats.generic import Directory
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.resample import Resample
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_resample_1():
    task = Resample()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.subjects_dir = Directory.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_resample_2():
    task = Resample()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.resampled_file = "resampled.nii"
    task.inputs.voxel_size = (2.1, 2.1, 2.1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
