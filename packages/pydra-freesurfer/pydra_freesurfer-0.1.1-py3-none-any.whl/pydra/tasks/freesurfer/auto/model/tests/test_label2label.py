from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Pial
from fileformats.model import Stl
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.model.label_2_label import Label2Label
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_label2label_1():
    task = Label2Label()
    task.inputs.sphere_reg = Pial.sample(seed=2)
    task.inputs.white = Pial.sample(seed=3)
    task.inputs.source_sphere_reg = Pial.sample(seed=4)
    task.inputs.source_white = Pial.sample(seed=5)
    task.inputs.source_label = Stl.sample(seed=6)
    task.inputs.registration_method = "surface"
    task.inputs.subjects_dir = Directory.sample(seed=11)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_label2label_2():
    task = Label2Label()
    task.inputs.hemisphere = "lh"
    task.inputs.subject_id = "10335"
    task.inputs.sphere_reg = Pial.sample(seed=2)
    task.inputs.white = Pial.sample(seed=3)
    task.inputs.source_sphere_reg = Pial.sample(seed=4)
    task.inputs.source_white = Pial.sample(seed=5)
    task.inputs.source_label = Stl.sample(seed=6)
    task.inputs.source_subject = "fsaverage"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
