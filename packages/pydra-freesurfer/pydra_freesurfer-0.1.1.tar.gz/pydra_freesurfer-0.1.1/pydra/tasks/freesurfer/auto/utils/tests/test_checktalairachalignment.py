from fileformats.datascience import TextMatrix
from fileformats.generic import Directory
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.check_talairach_alignment import (
    CheckTalairachAlignment,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_checktalairachalignment_1():
    task = CheckTalairachAlignment()
    task.inputs.in_file = TextMatrix.sample(seed=0)
    task.inputs.threshold = 0.01
    task.inputs.subjects_dir = Directory.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_checktalairachalignment_2():
    task = CheckTalairachAlignment()
    task.inputs.in_file = TextMatrix.sample(seed=0)
    task.inputs.threshold = 0.005
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
