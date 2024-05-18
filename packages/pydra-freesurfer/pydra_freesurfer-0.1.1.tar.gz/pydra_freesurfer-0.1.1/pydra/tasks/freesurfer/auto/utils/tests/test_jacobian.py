from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.jacobian import Jacobian
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_jacobian_1():
    task = Jacobian()
    task.inputs.in_origsurf = Pial.sample(seed=0)
    task.inputs.in_mappedsurf = Pial.sample(seed=1)
    task.inputs.subjects_dir = Directory.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_jacobian_2():
    task = Jacobian()
    task.inputs.in_origsurf = Pial.sample(seed=0)
    task.inputs.in_mappedsurf = Pial.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
