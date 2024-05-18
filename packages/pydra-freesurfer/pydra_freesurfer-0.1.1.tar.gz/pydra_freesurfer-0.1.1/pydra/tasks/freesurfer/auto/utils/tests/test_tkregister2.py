from fileformats.datascience import TextMatrix
from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.tkregister_2 import Tkregister2
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_tkregister2_1():
    task = Tkregister2()
    task.inputs.target_image = Nifti1.sample(seed=0)
    task.inputs.moving_image = Nifti1.sample(seed=2)
    task.inputs.fsl_in_matrix = TextMatrix.sample(seed=3)
    task.inputs.xfm = File.sample(seed=4)
    task.inputs.lta_in = File.sample(seed=5)
    task.inputs.noedit = True
    task.inputs.subjects_dir = Directory.sample(seed=16)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_tkregister2_2():
    task = Tkregister2()
    task.inputs.target_image = Nifti1.sample(seed=0)
    task.inputs.moving_image = Nifti1.sample(seed=2)
    task.inputs.reg_file = "T1_to_native.dat"
    task.inputs.reg_header = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_tkregister2_3():
    task = Tkregister2()
    task.inputs.moving_image = Nifti1.sample(seed=2)
    task.inputs.fsl_in_matrix = TextMatrix.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
