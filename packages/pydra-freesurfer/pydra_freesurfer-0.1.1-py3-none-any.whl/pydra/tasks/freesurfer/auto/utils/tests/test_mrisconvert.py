from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.mr_is_convert import MRIsConvert
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mrisconvert_1():
    task = MRIsConvert()
    task.inputs.annot_file = File.sample(seed=0)
    task.inputs.parcstats_file = File.sample(seed=1)
    task.inputs.label_file = File.sample(seed=2)
    task.inputs.scalarcurv_file = File.sample(seed=3)
    task.inputs.functional_file = File.sample(seed=4)
    task.inputs.labelstats_outfile = File.sample(seed=5)
    task.inputs.in_file = File.sample(seed=15)
    task.inputs.subjects_dir = Directory.sample(seed=20)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
