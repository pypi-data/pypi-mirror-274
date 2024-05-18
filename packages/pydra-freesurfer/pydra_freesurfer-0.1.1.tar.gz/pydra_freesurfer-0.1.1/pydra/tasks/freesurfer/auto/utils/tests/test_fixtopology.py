from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Inflated, Nofix, Orig
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.fix_topology import FixTopology
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_fixtopology_1():
    task = FixTopology()
    task.inputs.in_orig = Orig.sample(seed=0)
    task.inputs.in_inflated = Inflated.sample(seed=1)
    task.inputs.in_brain = File.sample(seed=2)
    task.inputs.in_wm = File.sample(seed=3)
    task.inputs.sphere = Nofix.sample(seed=10)
    task.inputs.subjects_dir = Directory.sample(seed=11)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_fixtopology_2():
    task = FixTopology()
    task.inputs.in_orig = Orig.sample(seed=0)
    task.inputs.in_inflated = Inflated.sample(seed=1)
    task.inputs.hemisphere = "lh"
    task.inputs.subject_id = "10335"
    task.inputs.ga = True
    task.inputs.mgz = True
    task.inputs.sphere = Nofix.sample(seed=10)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
