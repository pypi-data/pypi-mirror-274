from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.sphere import Sphere
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_sphere_1():
    task = Sphere()
    task.inputs.in_file = Pial.sample(seed=0)
    task.inputs.in_smoothwm = File.sample(seed=4)
    task.inputs.subjects_dir = Directory.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_sphere_2():
    task = Sphere()
    task.inputs.in_file = Pial.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
