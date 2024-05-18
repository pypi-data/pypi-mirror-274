from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.mr_is_combine import MRIsCombine
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mriscombine_1():
    task = MRIsCombine()
    task.inputs.in_files = [Pial.sample(seed=0)]
    task.inputs.subjects_dir = Directory.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mriscombine_2():
    task = MRIsCombine()
    task.inputs.in_files = [Pial.sample(seed=0)]
    task.inputs.out_file = "bh.pial"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
