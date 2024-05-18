from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.bb_register import BBRegister
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_bbregister_1():
    task = BBRegister()
    task.inputs.init_reg_file = File.sample(seed=1)
    task.inputs.source_file = Nifti1.sample(seed=3)
    task.inputs.intermediate_file = File.sample(seed=5)
    task.inputs.subjects_dir = Directory.sample(seed=17)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_bbregister_2():
    task = BBRegister()
    task.inputs.init = "header"
    task.inputs.subject_id = "me"
    task.inputs.source_file = Nifti1.sample(seed=3)
    task.inputs.contrast_type = "t2"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
