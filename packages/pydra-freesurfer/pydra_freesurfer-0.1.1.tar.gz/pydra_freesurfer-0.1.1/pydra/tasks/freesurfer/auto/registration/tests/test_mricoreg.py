from fileformats.generic import Directory
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.registration.mri_coreg import MRICoreg
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mricoreg_1():
    task = MRICoreg()
    task.inputs.source_file = Nifti1.sample(seed=0)
    task.inputs.reference_file = Nifti1.sample(seed=1)
    task.inputs.out_lta_file = True
    task.inputs.subjects_dir = Directory.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mricoreg_2():
    task = MRICoreg()
    task.inputs.source_file = Nifti1.sample(seed=0)
    task.inputs.reference_file = Nifti1.sample(seed=1)
    task.inputs.subjects_dir = "."
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mricoreg_3():
    task = MRICoreg()
    task.inputs.source_file = Nifti1.sample(seed=0)
    task.inputs.subjects_dir = "."
    task.inputs.subject_id = "fsaverage"
    task.inputs.reference_mask = False
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mricoreg_4():
    task = MRICoreg()
    task.inputs.sep = [4]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mricoreg_5():
    task = MRICoreg()
    task.inputs.sep = [4, 5]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
