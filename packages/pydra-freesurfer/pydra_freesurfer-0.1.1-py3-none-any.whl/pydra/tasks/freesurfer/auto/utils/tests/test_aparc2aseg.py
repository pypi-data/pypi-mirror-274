from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.aparc_2_aseg import Aparc2Aseg
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_aparc2aseg_1():
    task = Aparc2Aseg()
    task.inputs.lh_white = Pial.sample(seed=2)
    task.inputs.rh_white = Pial.sample(seed=3)
    task.inputs.lh_pial = Pial.sample(seed=4)
    task.inputs.rh_pial = Pial.sample(seed=5)
    task.inputs.lh_ribbon = MghGz.sample(seed=6)
    task.inputs.rh_ribbon = MghGz.sample(seed=7)
    task.inputs.ribbon = MghGz.sample(seed=8)
    task.inputs.lh_annotation = Pial.sample(seed=9)
    task.inputs.rh_annotation = Pial.sample(seed=10)
    task.inputs.filled = File.sample(seed=11)
    task.inputs.aseg = File.sample(seed=12)
    task.inputs.ctxseg = File.sample(seed=14)
    task.inputs.subjects_dir = Directory.sample(seed=20)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_aparc2aseg_2():
    task = Aparc2Aseg()
    task.inputs.out_file = "aparc+aseg.mgz"
    task.inputs.lh_white = Pial.sample(seed=2)
    task.inputs.rh_white = Pial.sample(seed=3)
    task.inputs.lh_pial = Pial.sample(seed=4)
    task.inputs.rh_pial = Pial.sample(seed=5)
    task.inputs.lh_ribbon = MghGz.sample(seed=6)
    task.inputs.rh_ribbon = MghGz.sample(seed=7)
    task.inputs.ribbon = MghGz.sample(seed=8)
    task.inputs.lh_annotation = Pial.sample(seed=9)
    task.inputs.rh_annotation = Pial.sample(seed=10)
    task.inputs.label_wm = True
    task.inputs.rip_unknown = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
