from fileformats.generic import Directory
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.talairach_avi import TalairachAVI
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_talairachavi_1():
    task = TalairachAVI()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.subjects_dir = Directory.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_talairachavi_2():
    task = TalairachAVI()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.out_file = "trans.mat"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
