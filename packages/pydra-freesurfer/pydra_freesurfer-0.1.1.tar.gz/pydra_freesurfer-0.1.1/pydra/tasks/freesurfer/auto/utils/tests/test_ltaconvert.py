from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.lta_convert import LTAConvert
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_ltaconvert_1():
    task = LTAConvert()
    task.inputs.in_fsl = File.sample(seed=1)
    task.inputs.in_mni = File.sample(seed=2)
    task.inputs.in_reg = File.sample(seed=3)
    task.inputs.in_niftyreg = File.sample(seed=4)
    task.inputs.in_itk = File.sample(seed=5)
    task.inputs.source_file = File.sample(seed=13)
    task.inputs.target_file = File.sample(seed=14)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
