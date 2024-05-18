from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.model.concatenate import Concatenate
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_concatenate_1():
    task = Concatenate()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.multiply_matrix_file = File.sample(seed=9)
    task.inputs.mask_file = File.sample(seed=14)
    task.inputs.subjects_dir = Directory.sample(seed=17)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_concatenate_2():
    task = Concatenate()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.concatenated_file = "bar.nii"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
