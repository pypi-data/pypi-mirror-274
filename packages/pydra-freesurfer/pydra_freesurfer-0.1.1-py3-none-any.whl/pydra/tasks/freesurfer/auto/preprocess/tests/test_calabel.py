from fileformats.datascience import TextMatrix
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz, Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.ca_label import CALabel
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_calabel_1():
    task = CALabel()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.transform = TextMatrix.sample(seed=2)
    task.inputs.template = Nifti1.sample(seed=3)
    task.inputs.in_vol = File.sample(seed=4)
    task.inputs.intensities = File.sample(seed=5)
    task.inputs.label = File.sample(seed=10)
    task.inputs.aseg = File.sample(seed=11)
    task.inputs.subjects_dir = Directory.sample(seed=13)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_calabel_2():
    task = CALabel()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.out_file = "out.mgz"
    task.inputs.transform = TextMatrix.sample(seed=2)
    task.inputs.template = Nifti1.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
