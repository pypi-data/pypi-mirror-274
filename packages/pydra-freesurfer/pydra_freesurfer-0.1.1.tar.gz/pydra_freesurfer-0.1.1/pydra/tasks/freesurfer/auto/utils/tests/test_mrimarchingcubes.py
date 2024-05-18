from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.mri_marching_cubes import MRIMarchingCubes
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mrimarchingcubes_1():
    task = MRIMarchingCubes()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.connectivity_value = 1
    task.inputs.subjects_dir = Directory.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
