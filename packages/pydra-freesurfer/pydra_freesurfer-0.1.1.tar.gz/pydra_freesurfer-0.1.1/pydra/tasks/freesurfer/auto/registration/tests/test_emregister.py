from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.registration.em_register import EMRegister
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_emregister_1():
    task = EMRegister()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.template = MghGz.sample(seed=1)
    task.inputs.mask = File.sample(seed=4)
    task.inputs.transform = File.sample(seed=6)
    task.inputs.subjects_dir = Directory.sample(seed=8)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_emregister_2():
    task = EMRegister()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.template = MghGz.sample(seed=1)
    task.inputs.out_file = "norm_transform.lta"
    task.inputs.skull = True
    task.inputs.nbrspacing = 9
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
