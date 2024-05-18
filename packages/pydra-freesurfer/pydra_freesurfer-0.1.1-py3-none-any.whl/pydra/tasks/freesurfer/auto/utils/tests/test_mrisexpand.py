from fileformats.generic import Directory
from fileformats.medimage_freesurfer import White
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.mr_is_expand import MRIsExpand
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mrisexpand_1():
    task = MRIsExpand()
    task.inputs.in_file = White.sample(seed=0)
    task.inputs.out_name = "expanded"
    task.inputs.sphere = "sphere"
    task.inputs.subjects_dir = Directory.sample(seed=12)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mrisexpand_2():
    task = MRIsExpand()
    task.inputs.in_file = White.sample(seed=0)
    task.inputs.distance = 0.5
    task.inputs.out_name = "graymid"
    task.inputs.thickness = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
