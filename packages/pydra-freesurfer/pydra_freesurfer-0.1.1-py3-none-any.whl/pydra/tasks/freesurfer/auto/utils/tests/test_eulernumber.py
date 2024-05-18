from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.euler_number import EulerNumber
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_eulernumber_1():
    task = EulerNumber()
    task.inputs.in_file = Pial.sample(seed=0)
    task.inputs.subjects_dir = Directory.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_eulernumber_2():
    task = EulerNumber()
    task.inputs.in_file = Pial.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
