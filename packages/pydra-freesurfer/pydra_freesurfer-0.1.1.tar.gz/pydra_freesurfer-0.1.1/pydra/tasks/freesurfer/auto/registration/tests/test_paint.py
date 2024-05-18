from fileformats.generic import Directory
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.registration.paint import Paint
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_paint_1():
    task = Paint()
    task.inputs.in_surf = Pial.sample(seed=0)
    task.inputs.template = MghGz.sample(seed=1)
    task.inputs.subjects_dir = Directory.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_paint_2():
    task = Paint()
    task.inputs.in_surf = Pial.sample(seed=0)
    task.inputs.template = MghGz.sample(seed=1)
    task.inputs.averages = 5
    task.inputs.out_file = "lh.avg_curv"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
