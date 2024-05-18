from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.model.binarize import Binarize
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_binarize_1():
    task = Binarize()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.merge_file = File.sample(seed=16)
    task.inputs.mask_file = File.sample(seed=17)
    task.inputs.subjects_dir = Directory.sample(seed=26)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_binarize_2():
    task = Binarize()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.min = 10
    task.inputs.binary_file = "foo_out.nii"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
