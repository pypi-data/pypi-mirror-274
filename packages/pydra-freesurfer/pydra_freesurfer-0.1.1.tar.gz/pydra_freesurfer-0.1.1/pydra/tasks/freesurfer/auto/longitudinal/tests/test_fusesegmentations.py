from fileformats.generic import Directory
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.longitudinal.fuse_segmentations import (
    FuseSegmentations,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_fusesegmentations_1():
    task = FuseSegmentations()
    task.inputs.in_segmentations = [MghGz.sample(seed=3)]
    task.inputs.in_segmentations_noCC = [MghGz.sample(seed=4)]
    task.inputs.in_norms = [MghGz.sample(seed=5)]
    task.inputs.subjects_dir = Directory.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_fusesegmentations_2():
    task = FuseSegmentations()
    task.inputs.subject_id = "tp.long.A.template"
    task.inputs.timepoints = ["tp1", "tp2"]
    task.inputs.out_file = "aseg.fused.mgz"
    task.inputs.in_segmentations = [MghGz.sample(seed=3)]
    task.inputs.in_segmentations_noCC = [MghGz.sample(seed=4)]
    task.inputs.in_norms = [MghGz.sample(seed=5)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
