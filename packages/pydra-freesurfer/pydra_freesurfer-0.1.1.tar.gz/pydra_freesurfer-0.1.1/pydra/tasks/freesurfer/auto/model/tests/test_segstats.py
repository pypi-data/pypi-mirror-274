from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.model.seg_stats import SegStats
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_segstats_1():
    task = SegStats()
    task.inputs.segmentation_file = File.sample(seed=0)
    task.inputs.partial_volume_file = File.sample(seed=4)
    task.inputs.in_file = Nifti1.sample(seed=5)
    task.inputs.color_table_file = File.sample(seed=10)
    task.inputs.gca_color_table = File.sample(seed=12)
    task.inputs.mask_file = File.sample(seed=20)
    task.inputs.brainmask_file = File.sample(seed=27)
    task.inputs.in_intensity = File.sample(seed=38)
    task.inputs.subjects_dir = Directory.sample(seed=40)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_segstats_2():
    task = SegStats()
    task.inputs.annot = ("PWS04", "lh", "aparc")
    task.inputs.summary_file = "summary.stats"
    task.inputs.in_file = Nifti1.sample(seed=5)
    task.inputs.avgwf_txt_file = "avgwf.txt"
    task.inputs.subjects_dir = "."
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
