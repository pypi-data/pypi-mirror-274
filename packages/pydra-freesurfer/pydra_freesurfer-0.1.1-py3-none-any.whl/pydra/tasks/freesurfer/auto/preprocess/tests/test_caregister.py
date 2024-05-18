from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.ca_register import CARegister
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_caregister_1():
    task = CARegister()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.template = File.sample(seed=2)
    task.inputs.mask = File.sample(seed=3)
    task.inputs.transform = File.sample(seed=6)
    task.inputs.l_files = [File.sample(seed=10)]
    task.inputs.subjects_dir = Directory.sample(seed=12)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_caregister_2():
    task = CARegister()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.out_file = "talairach.m3z"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
