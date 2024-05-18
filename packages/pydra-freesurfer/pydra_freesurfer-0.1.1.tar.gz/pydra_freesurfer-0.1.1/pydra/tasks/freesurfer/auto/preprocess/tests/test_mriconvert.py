from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.mri_convert import MRIConvert
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mriconvert_1():
    task = MRIConvert()
    task.inputs.autoalign_matrix = File.sample(seed=37)
    task.inputs.apply_transform = File.sample(seed=39)
    task.inputs.apply_inv_transform = File.sample(seed=40)
    task.inputs.in_file = Nifti1.sample(seed=54)
    task.inputs.reslice_like = File.sample(seed=62)
    task.inputs.in_like = File.sample(seed=72)
    task.inputs.color_file = File.sample(seed=76)
    task.inputs.status_file = File.sample(seed=78)
    task.inputs.sdcm_list = File.sample(seed=79)
    task.inputs.subjects_dir = Directory.sample(seed=83)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mriconvert_2():
    task = MRIConvert()
    task.inputs.out_type = "mgz"
    task.inputs.in_file = Nifti1.sample(seed=54)
    task.inputs.out_file = "outfile.mgz"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
