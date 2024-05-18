from fileformats.datascience import DatFile
from fileformats.generic import Directory
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.smooth import Smooth
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_smooth_1():
    task = Smooth()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.reg_file = DatFile.sample(seed=1)
    task.inputs.subjects_dir = Directory.sample(seed=8)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_smooth_2():
    task = Smooth()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.reg_file = DatFile.sample(seed=1)
    task.inputs.smoothed_file = "foo_out.nii"
    task.inputs.surface_fwhm = 10
    task.inputs.vol_fwhm = 6
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
