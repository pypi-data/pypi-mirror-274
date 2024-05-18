from fileformats.generic import Directory
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.edit_w_mwith_aseg import EditWMwithAseg
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_editwmwithaseg_1():
    task = EditWMwithAseg()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.brain_file = MghGz.sample(seed=1)
    task.inputs.seg_file = MghGz.sample(seed=2)
    task.inputs.subjects_dir = Directory.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_editwmwithaseg_2():
    task = EditWMwithAseg()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.brain_file = MghGz.sample(seed=1)
    task.inputs.seg_file = MghGz.sample(seed=2)
    task.inputs.out_file = "wm.asegedit.mgz"
    task.inputs.keep_in = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
