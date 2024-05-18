from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.unpack_sdicom_dir import UnpackSDICOMDir
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_unpacksdicomdir_1():
    task = UnpackSDICOMDir()
    task.inputs.source_dir = Directory.sample(seed=0)
    task.inputs.output_dir = Directory.sample(seed=1)
    task.inputs.config = File.sample(seed=3)
    task.inputs.seq_config = File.sample(seed=4)
    task.inputs.scan_only = File.sample(seed=7)
    task.inputs.log_file = File.sample(seed=8)
    task.inputs.subjects_dir = Directory.sample(seed=11)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_unpacksdicomdir_2():
    task = UnpackSDICOMDir()
    task.inputs.source_dir = "."
    task.inputs.output_dir = "."
    task.inputs.run_info = (5, "mprage", "nii", "struct")
    task.inputs.dir_structure = "generic"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
