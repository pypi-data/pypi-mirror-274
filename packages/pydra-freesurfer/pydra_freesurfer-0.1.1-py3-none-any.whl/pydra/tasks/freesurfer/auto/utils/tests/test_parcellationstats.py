from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial, Thickness, White, Xfm
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.parcellation_stats import ParcellationStats
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_parcellationstats_1():
    task = ParcellationStats()
    task.inputs.wm = MghGz.sample(seed=2)
    task.inputs.lh_white = White.sample(seed=3)
    task.inputs.rh_white = White.sample(seed=4)
    task.inputs.lh_pial = Pial.sample(seed=5)
    task.inputs.rh_pial = Pial.sample(seed=6)
    task.inputs.transform = Xfm.sample(seed=7)
    task.inputs.thickness = Thickness.sample(seed=8)
    task.inputs.brainmask = MghGz.sample(seed=9)
    task.inputs.aseg = MghGz.sample(seed=10)
    task.inputs.ribbon = MghGz.sample(seed=11)
    task.inputs.cortex_label = File.sample(seed=12)
    task.inputs.in_cortex = File.sample(seed=15)
    task.inputs.in_annotation = File.sample(seed=16)
    task.inputs.in_label = File.sample(seed=17)
    task.inputs.subjects_dir = Directory.sample(seed=23)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_parcellationstats_2():
    task = ParcellationStats()
    task.inputs.subject_id = "10335"
    task.inputs.hemisphere = "lh"
    task.inputs.wm = MghGz.sample(seed=2)
    task.inputs.lh_white = White.sample(seed=3)
    task.inputs.rh_white = White.sample(seed=4)
    task.inputs.lh_pial = Pial.sample(seed=5)
    task.inputs.rh_pial = Pial.sample(seed=6)
    task.inputs.transform = Xfm.sample(seed=7)
    task.inputs.thickness = Thickness.sample(seed=8)
    task.inputs.brainmask = MghGz.sample(seed=9)
    task.inputs.aseg = MghGz.sample(seed=10)
    task.inputs.ribbon = MghGz.sample(seed=11)
    task.inputs.surface = "white"
    task.inputs.out_table = "lh.test.stats"
    task.inputs.out_color = "test.ctab"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
