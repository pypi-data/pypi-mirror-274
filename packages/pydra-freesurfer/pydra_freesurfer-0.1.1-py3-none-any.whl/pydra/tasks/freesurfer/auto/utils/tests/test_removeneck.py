from fileformats.datascience import TextMatrix
from fileformats.generic import Directory
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.remove_neck import RemoveNeck
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_removeneck_1():
    task = RemoveNeck()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.transform = TextMatrix.sample(seed=2)
    task.inputs.template = TextMatrix.sample(seed=3)
    task.inputs.subjects_dir = Directory.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_removeneck_2():
    task = RemoveNeck()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.transform = TextMatrix.sample(seed=2)
    task.inputs.template = TextMatrix.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
