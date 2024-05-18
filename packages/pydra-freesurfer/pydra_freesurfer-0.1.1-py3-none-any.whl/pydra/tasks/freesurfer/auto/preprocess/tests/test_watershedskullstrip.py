from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Lta
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.watershed_skull_strip import (
    WatershedSkullStrip,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_watershedskullstrip_1():
    task = WatershedSkullStrip()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.brain_atlas = File.sample(seed=3)
    task.inputs.transform = Lta.sample(seed=4)
    task.inputs.subjects_dir = Directory.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_watershedskullstrip_2():
    task = WatershedSkullStrip()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.out_file = "brainmask.auto.mgz"
    task.inputs.t1 = True
    task.inputs.transform = Lta.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
