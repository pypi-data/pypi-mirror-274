from fileformats.generic import Directory
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.registration.register import Register
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_register_1():
    task = Register()
    task.inputs.in_surf = Pial.sample(seed=0)
    task.inputs.target = MghGz.sample(seed=1)
    task.inputs.in_sulc = Pial.sample(seed=2)
    task.inputs.in_smoothwm = Pial.sample(seed=5)
    task.inputs.subjects_dir = Directory.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_register_2():
    task = Register()
    task.inputs.in_surf = Pial.sample(seed=0)
    task.inputs.target = MghGz.sample(seed=1)
    task.inputs.in_sulc = Pial.sample(seed=2)
    task.inputs.out_file = "lh.pial.reg"
    task.inputs.curv = True
    task.inputs.in_smoothwm = Pial.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
