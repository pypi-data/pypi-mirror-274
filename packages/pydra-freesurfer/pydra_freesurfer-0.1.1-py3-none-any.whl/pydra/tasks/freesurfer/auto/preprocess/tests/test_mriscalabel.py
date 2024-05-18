from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.mr_is_ca_label import MRIsCALabel
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mriscalabel_1():
    task = MRIsCALabel()
    task.inputs.canonsurf = Pial.sample(seed=2)
    task.inputs.classifier = Nifti1.sample(seed=3)
    task.inputs.smoothwm = Pial.sample(seed=4)
    task.inputs.curv = Pial.sample(seed=5)
    task.inputs.sulc = Pial.sample(seed=6)
    task.inputs.label = File.sample(seed=8)
    task.inputs.aseg = File.sample(seed=9)
    task.inputs.subjects_dir = Directory.sample(seed=13)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mriscalabel_2():
    task = MRIsCALabel()
    task.inputs.subject_id = "test"
    task.inputs.hemisphere = "lh"
    task.inputs.canonsurf = Pial.sample(seed=2)
    task.inputs.classifier = Nifti1.sample(seed=3)
    task.inputs.smoothwm = Pial.sample(seed=4)
    task.inputs.curv = Pial.sample(seed=5)
    task.inputs.sulc = Pial.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
