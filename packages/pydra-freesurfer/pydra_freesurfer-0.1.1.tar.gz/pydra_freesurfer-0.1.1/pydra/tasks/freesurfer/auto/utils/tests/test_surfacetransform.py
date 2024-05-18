from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.surface_transform import SurfaceTransform
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_surfacetransform_1():
    task = SurfaceTransform()
    task.inputs.source_file = File.sample(seed=0)
    task.inputs.source_annot_file = File.sample(seed=1)
    task.inputs.subjects_dir = Directory.sample(seed=11)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
