from fileformats.generic import Directory
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.relabel_hypointensities import (
    RelabelHypointensities,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_relabelhypointensities_1():
    task = RelabelHypointensities()
    task.inputs.lh_white = Pial.sample(seed=0)
    task.inputs.rh_white = Pial.sample(seed=1)
    task.inputs.aseg = MghGz.sample(seed=2)
    task.inputs.surf_directory = Directory.sample(seed=3)
    task.inputs.subjects_dir = Directory.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_relabelhypointensities_2():
    task = RelabelHypointensities()
    task.inputs.lh_white = Pial.sample(seed=0)
    task.inputs.rh_white = Pial.sample(seed=1)
    task.inputs.aseg = MghGz.sample(seed=2)
    task.inputs.surf_directory = "."
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
