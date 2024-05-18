from fileformats.generic import Directory, File
from fileformats.medimage import MghGz, NiftiGz
from fileformats.medimage_freesurfer import Lta
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.petsurfer.gtmpvc import GTMPVC
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_gtmpvc_1():
    task = GTMPVC()
    task.inputs.in_file = NiftiGz.sample(seed=0)
    task.inputs.segmentation = MghGz.sample(seed=3)
    task.inputs.reg_file = Lta.sample(seed=4)
    task.inputs.mask_file = File.sample(seed=8)
    task.inputs.contrast = [File.sample(seed=12)]
    task.inputs.color_table_file = File.sample(seed=21)
    task.inputs.subjects_dir = Directory.sample(seed=55)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_gtmpvc_2():
    task = GTMPVC()
    task.inputs.in_file = NiftiGz.sample(seed=0)
    task.inputs.psf = 4
    task.inputs.segmentation = MghGz.sample(seed=3)
    task.inputs.reg_file = Lta.sample(seed=4)
    task.inputs.pvc_dir = "pvc"
    task.inputs.auto_mask = (1, 0.1)
    task.inputs.default_seg_merge = True
    task.inputs.no_rescale = True
    task.inputs.km_ref = ["8 47"]
    task.inputs.km_hb = ["11 12 50 51"]
    task.inputs.save_input = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_gtmpvc_3():
    task = GTMPVC()
    task.inputs.in_file = NiftiGz.sample(seed=0)
    task.inputs.segmentation = MghGz.sample(seed=3)
    task.inputs.regheader = True
    task.inputs.pvc_dir = "pvc"
    task.inputs.mg = (0.5, ["ROI1", "ROI2"])
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
