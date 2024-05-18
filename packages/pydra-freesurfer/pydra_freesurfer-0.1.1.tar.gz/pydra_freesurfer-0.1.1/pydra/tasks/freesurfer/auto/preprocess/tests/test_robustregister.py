from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.robust_register import RobustRegister
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_robustregister_1():
    task = RobustRegister()
    task.inputs.source_file = Nifti1.sample(seed=0)
    task.inputs.target_file = Nifti1.sample(seed=1)
    task.inputs.out_reg_file = True
    task.inputs.in_xfm_file = File.sample(seed=7)
    task.inputs.mask_source = File.sample(seed=25)
    task.inputs.mask_target = File.sample(seed=26)
    task.inputs.subjects_dir = Directory.sample(seed=29)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_robustregister_2():
    task = RobustRegister()
    task.inputs.source_file = Nifti1.sample(seed=0)
    task.inputs.target_file = Nifti1.sample(seed=1)
    task.inputs.auto_sens = True
    task.inputs.init_orient = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
