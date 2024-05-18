from fileformats.generic import Directory
from fileformats.medimage import MghGz
from fileformats.text import TextFile
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.registration.register_av_ito_talairach import (
    RegisterAVItoTalairach,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_registeravitotalairach_1():
    task = RegisterAVItoTalairach()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.target = MghGz.sample(seed=1)
    task.inputs.vox2vox = TextFile.sample(seed=2)
    task.inputs.out_file = "talairach.auto.xfm"
    task.inputs.subjects_dir = Directory.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registeravitotalairach_2():
    task = RegisterAVItoTalairach()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.target = MghGz.sample(seed=1)
    task.inputs.vox2vox = TextFile.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
