from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.apply_mask import ApplyMask
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_applymask_1():
    task = ApplyMask()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.mask_file = File.sample(seed=1)
    task.inputs.xfm_file = File.sample(seed=3)
    task.inputs.xfm_source = File.sample(seed=5)
    task.inputs.xfm_target = File.sample(seed=6)
    task.inputs.subjects_dir = Directory.sample(seed=11)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
