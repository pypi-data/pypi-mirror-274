from fileformats.generic import Directory
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.segment_cc import SegmentCC
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_segmentcc_1():
    task = SegmentCC()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.in_norm = MghGz.sample(seed=1)
    task.inputs.subjects_dir = Directory.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_segmentcc_2():
    task = SegmentCC()
    task.inputs.in_file = MghGz.sample(seed=0)
    task.inputs.in_norm = MghGz.sample(seed=1)
    task.inputs.out_rotation = "cc.lta"
    task.inputs.subject_id = "test"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
