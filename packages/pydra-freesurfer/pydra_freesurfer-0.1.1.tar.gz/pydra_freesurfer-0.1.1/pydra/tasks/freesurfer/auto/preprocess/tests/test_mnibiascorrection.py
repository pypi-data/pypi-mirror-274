from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.mni_bias_correction import MNIBiasCorrection
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mnibiascorrection_1():
    task = MNIBiasCorrection()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.iterations = 4
    task.inputs.mask = File.sample(seed=6)
    task.inputs.transform = File.sample(seed=7)
    task.inputs.subjects_dir = Directory.sample(seed=10)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mnibiascorrection_2():
    task = MNIBiasCorrection()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.iterations = 6
    task.inputs.protocol_iterations = 1000
    task.inputs.distance = 50
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
