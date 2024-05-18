from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.registration.mp_rto_mni305 import MPRtoMNI305
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mprtomni305_1():
    task = MPRtoMNI305()
    task.inputs.reference_dir = Directory.sample(seed=0)
    task.inputs.in_file = File.sample(seed=2)
    task.inputs.subjects_dir = Directory.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mprtomni305_2():
    task = MPRtoMNI305()
    task.inputs.reference_dir = "."  # doctest: +SKIP
    task.inputs.target = "structural.nii"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
