from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.recon_all import ReconAll
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_reconall_1():
    task = ReconAll()
    task.inputs.subject_id = "recon_all"
    task.inputs.directive = "all"
    task.inputs.T1_files = [Nifti1.sample(seed=3)]
    task.inputs.T2_file = File.sample(seed=4)
    task.inputs.FLAIR_file = File.sample(seed=5)
    task.inputs.expert = File.sample(seed=16)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_reconall_2():
    task = ReconAll()
    task.inputs.subject_id = "foo"
    task.inputs.directive = "all"
    task.inputs.T1_files = [Nifti1.sample(seed=3)]
    task.inputs.subjects_dir = "."
    task.inputs.flags = ["-cw256", "-qcache"]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_reconall_3():
    task = ReconAll()
    task.inputs.hemi = "lh"
    task.inputs.flags = []
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_reconall_4():
    task = ReconAll()
    task.inputs.directive = "autorecon-hemi"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_reconall_5():
    task = ReconAll()
    task.inputs.subject_id = "foo"
    task.inputs.directive = "all"
    task.inputs.T1_files = [Nifti1.sample(seed=3)]
    task.inputs.hippocampal_subfields_T1 = False
    task.inputs.hippocampal_subfields_T2 = ("structural.nii", "test")
    task.inputs.subjects_dir = "."
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
