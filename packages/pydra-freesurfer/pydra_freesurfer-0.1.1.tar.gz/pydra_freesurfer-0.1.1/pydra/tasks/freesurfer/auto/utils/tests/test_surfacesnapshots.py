from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.surface_snapshots import SurfaceSnapshots
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_surfacesnapshots_1():
    task = SurfaceSnapshots()
    task.inputs.overlay = File.sample(seed=5)
    task.inputs.overlay_reg = File.sample(seed=6)
    task.inputs.annot_file = File.sample(seed=15)
    task.inputs.label_file = File.sample(seed=17)
    task.inputs.colortable = File.sample(seed=19)
    task.inputs.patch_file = File.sample(seed=22)
    task.inputs.subjects_dir = Directory.sample(seed=31)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
