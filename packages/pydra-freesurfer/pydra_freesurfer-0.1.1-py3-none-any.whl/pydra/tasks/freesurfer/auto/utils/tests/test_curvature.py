from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.curvature import Curvature
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_curvature_1():
    task = Curvature()
    task.inputs.in_file = Pial.sample(seed=0)
    task.inputs.subjects_dir = Directory.sample(seed=7)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_curvature_2():
    task = Curvature()
    task.inputs.in_file = Pial.sample(seed=0)
    task.inputs.save = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
