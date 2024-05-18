from fileformats.datascience import DatFile
from fileformats.generic import Directory, File
from fileformats.medimage import NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.sample_to_surface import SampleToSurface
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_sampletosurface_1():
    task = SampleToSurface()
    task.inputs.source_file = NiftiGz.sample(seed=0)
    task.inputs.reference_file = File.sample(seed=1)
    task.inputs.reg_file = DatFile.sample(seed=4)
    task.inputs.mask_label = File.sample(seed=18)
    task.inputs.subjects_dir = Directory.sample(seed=35)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_sampletosurface_2():
    task = SampleToSurface()
    task.inputs.source_file = NiftiGz.sample(seed=0)
    task.inputs.hemi = "lh"
    task.inputs.reg_file = DatFile.sample(seed=4)
    task.inputs.sampling_method = "average"
    task.inputs.sampling_range = 1
    task.inputs.sampling_units = "frac"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
