from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.volume_mask import VolumeMask
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_volumemask_1():
    task = VolumeMask()
    task.inputs.lh_pial = Pial.sample(seed=4)
    task.inputs.rh_pial = Pial.sample(seed=5)
    task.inputs.lh_white = Pial.sample(seed=6)
    task.inputs.rh_white = Pial.sample(seed=7)
    task.inputs.aseg = File.sample(seed=8)
    task.inputs.in_aseg = File.sample(seed=10)
    task.inputs.subjects_dir = Directory.sample(seed=13)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_volumemask_2():
    task = VolumeMask()
    task.inputs.left_whitelabel = 2
    task.inputs.left_ribbonlabel = 3
    task.inputs.right_whitelabel = 41
    task.inputs.right_ribbonlabel = 42
    task.inputs.lh_pial = Pial.sample(seed=4)
    task.inputs.rh_pial = Pial.sample(seed=5)
    task.inputs.lh_white = Pial.sample(seed=6)
    task.inputs.rh_white = Pial.sample(seed=7)
    task.inputs.subject_id = "10335"
    task.inputs.save_ribbon = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
