from fileformats.datascience import TextMatrix
from fileformats.medimage import MghGz, NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.surface_2_vol_transform import (
    Surface2VolTransform,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_surface2voltransform_1():
    task = Surface2VolTransform()
    task.inputs.source_file = MghGz.sample(seed=0)
    task.inputs.reg_file = TextMatrix.sample(seed=3)
    task.inputs.template_file = NiftiGz.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_surface2voltransform_2():
    task = Surface2VolTransform()
    task.inputs.source_file = MghGz.sample(seed=0)
    task.inputs.hemi = "lh"
    task.inputs.reg_file = TextMatrix.sample(seed=3)
    task.inputs.template_file = NiftiGz.sample(seed=4)
    task.inputs.subjects_dir = "."
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
