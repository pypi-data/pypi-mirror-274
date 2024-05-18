from fileformats.generic import Directory
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.synthesize_flash import SynthesizeFLASH
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_synthesizeflash_1():
    task = SynthesizeFLASH()
    task.inputs.t1_image = MghGz.sample(seed=4)
    task.inputs.pd_image = MghGz.sample(seed=5)
    task.inputs.subjects_dir = Directory.sample(seed=7)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_synthesizeflash_2():
    task = SynthesizeFLASH()
    task.inputs.tr = 20
    task.inputs.flip_angle = 30
    task.inputs.te = 3
    task.inputs.t1_image = MghGz.sample(seed=4)
    task.inputs.pd_image = MghGz.sample(seed=5)
    task.inputs.out_file = "flash_30syn.mgz"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
