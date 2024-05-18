from fileformats.generic import Directory, File
from fileformats.medimage import MghGz, Nifti1
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.make_surfaces import MakeSurfaces
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_makesurfaces_1():
    task = MakeSurfaces()
    task.inputs.in_orig = Pial.sample(seed=2)
    task.inputs.in_wm = MghGz.sample(seed=3)
    task.inputs.in_filled = MghGz.sample(seed=4)
    task.inputs.in_white = File.sample(seed=5)
    task.inputs.in_label = Nifti1.sample(seed=6)
    task.inputs.orig_white = File.sample(seed=7)
    task.inputs.orig_pial = Pial.sample(seed=8)
    task.inputs.in_aseg = File.sample(seed=12)
    task.inputs.in_T1 = MghGz.sample(seed=13)
    task.inputs.subjects_dir = Directory.sample(seed=20)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_makesurfaces_2():
    task = MakeSurfaces()
    task.inputs.hemisphere = "lh"
    task.inputs.subject_id = "10335"
    task.inputs.in_orig = Pial.sample(seed=2)
    task.inputs.in_wm = MghGz.sample(seed=3)
    task.inputs.in_filled = MghGz.sample(seed=4)
    task.inputs.in_label = Nifti1.sample(seed=6)
    task.inputs.orig_pial = Pial.sample(seed=8)
    task.inputs.in_T1 = MghGz.sample(seed=13)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
