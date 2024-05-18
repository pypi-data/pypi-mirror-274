from fileformats.generic import Directory
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.mri_pretess import MRIPretess
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mripretess_1():
    task = MRIPretess()
    task.inputs.in_filled = MghGz.sample(seed=0)
    task.inputs.in_norm = MghGz.sample(seed=2)
    task.inputs.subjects_dir = Directory.sample(seed=7)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mripretess_2():
    task = MRIPretess()
    task.inputs.in_filled = MghGz.sample(seed=0)
    task.inputs.in_norm = MghGz.sample(seed=2)
    task.inputs.nocorners = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
