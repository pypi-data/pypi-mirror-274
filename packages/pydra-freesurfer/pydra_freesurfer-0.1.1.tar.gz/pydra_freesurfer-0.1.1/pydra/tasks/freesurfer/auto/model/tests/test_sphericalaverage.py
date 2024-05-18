from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.model.spherical_average import SphericalAverage
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_sphericalaverage_1():
    task = SphericalAverage()
    task.inputs.in_surf = Pial.sample(seed=2)
    task.inputs.in_orig = File.sample(seed=8)
    task.inputs.subjects_dir = Directory.sample(seed=10)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_sphericalaverage_2():
    task = SphericalAverage()
    task.inputs.out_file = "test.out"
    task.inputs.in_average = "."
    task.inputs.in_surf = Pial.sample(seed=2)
    task.inputs.hemisphere = "lh"
    task.inputs.fname = "lh.entorhinal"
    task.inputs.which = "label"
    task.inputs.subject_id = "10335"
    task.inputs.erode = 2
    task.inputs.threshold = 5
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
