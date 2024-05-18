from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.curvature_stats import CurvatureStats
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_curvaturestats_1():
    task = CurvatureStats()
    task.inputs.surface = Pial.sample(seed=0)
    task.inputs.curvfile1 = Pial.sample(seed=1)
    task.inputs.curvfile2 = Pial.sample(seed=2)
    task.inputs.subjects_dir = Directory.sample(seed=10)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_curvaturestats_2():
    task = CurvatureStats()
    task.inputs.surface = Pial.sample(seed=0)
    task.inputs.curvfile1 = Pial.sample(seed=1)
    task.inputs.curvfile2 = Pial.sample(seed=2)
    task.inputs.hemisphere = "lh"
    task.inputs.out_file = "lh.curv.stats"
    task.inputs.min_max = True
    task.inputs.values = True
    task.inputs.write = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
