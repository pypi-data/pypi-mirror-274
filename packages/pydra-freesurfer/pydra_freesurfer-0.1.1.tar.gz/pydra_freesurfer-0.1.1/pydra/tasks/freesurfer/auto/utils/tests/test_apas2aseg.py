from fileformats.generic import Directory
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.apas_2_aseg import Apas2Aseg
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_apas2aseg_1():
    task = Apas2Aseg()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.subjects_dir = Directory.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_apas2aseg_2():
    task = Apas2Aseg()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.out_file = "output.mgz"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
