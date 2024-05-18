from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.smooth_tessellation import SmoothTessellation
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_smoothtessellation_1():
    task = SmoothTessellation()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.subjects_dir = Directory.sample(seed=14)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
