from fileformats.generic import Directory
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Annot, Label, Thickness, White
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.contrast import Contrast
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_contrast_1():
    task = Contrast()
    task.inputs.thickness = Thickness.sample(seed=2)
    task.inputs.white = White.sample(seed=3)
    task.inputs.annotation = Annot.sample(seed=4)
    task.inputs.cortex = Label.sample(seed=5)
    task.inputs.orig = MghGz.sample(seed=6)
    task.inputs.rawavg = MghGz.sample(seed=7)
    task.inputs.subjects_dir = Directory.sample(seed=9)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_contrast_2():
    task = Contrast()
    task.inputs.subject_id = "10335"
    task.inputs.hemisphere = "lh"
    task.inputs.thickness = Thickness.sample(seed=2)
    task.inputs.white = White.sample(seed=3)
    task.inputs.annotation = Annot.sample(seed=4)
    task.inputs.cortex = Label.sample(seed=5)
    task.inputs.orig = MghGz.sample(seed=6)
    task.inputs.rawavg = MghGz.sample(seed=7)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
