from fileformats.generic import Directory
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.surface_smooth import SurfaceSmooth
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_surfacesmooth_1():
    task = SurfaceSmooth()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.cortex = True
    task.inputs.subjects_dir = Directory.sample(seed=8)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_surfacesmooth_2():
    task = SurfaceSmooth()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.subject_id = "subj_1"
    task.inputs.hemi = "lh"
    task.inputs.fwhm = 5
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
