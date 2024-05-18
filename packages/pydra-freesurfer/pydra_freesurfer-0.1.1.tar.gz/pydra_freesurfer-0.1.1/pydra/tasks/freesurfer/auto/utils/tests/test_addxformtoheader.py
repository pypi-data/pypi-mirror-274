from fileformats.datascience import TextMatrix
from fileformats.generic import Directory
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.add_x_form_to_header import AddXFormToHeader
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_addxformtoheader_1():
    task = AddXFormToHeader()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.transform = TextMatrix.sample(seed=1)
    task.inputs.out_file = "output.mgz"
    task.inputs.subjects_dir = Directory.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_addxformtoheader_2():
    task = AddXFormToHeader()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.transform = TextMatrix.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_addxformtoheader_3():
    task = AddXFormToHeader()
    task.inputs.copy_name = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
