from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.mri_tessellate import MRITessellate
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mritessellate_1():
    task = MRITessellate()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.subjects_dir = Directory.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
