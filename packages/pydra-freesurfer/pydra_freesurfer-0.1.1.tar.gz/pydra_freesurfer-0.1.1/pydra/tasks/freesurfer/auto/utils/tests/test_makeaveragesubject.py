from fileformats.generic import Directory
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.make_average_subject import MakeAverageSubject
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_makeaveragesubject_1():
    task = MakeAverageSubject()
    task.inputs.out_name = "average"
    task.inputs.subjects_dir = Directory.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_makeaveragesubject_2():
    task = MakeAverageSubject()
    task.inputs.subjects_ids = ["s1", "s2"]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
