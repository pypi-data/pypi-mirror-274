from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.mr_is_inflate import MRIsInflate
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mrisinflate_1():
    task = MRIsInflate()
    task.inputs.in_file = Pial.sample(seed=0)
    task.inputs.subjects_dir = Directory.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mrisinflate_2():
    task = MRIsInflate()
    task.inputs.in_file = Pial.sample(seed=0)
    task.inputs.no_save_sulc = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
