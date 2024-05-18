from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Area, Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.utils.mr_is_calc import MRIsCalc
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mriscalc_1():
    task = MRIsCalc()
    task.inputs.in_file1 = Area.sample(seed=0)
    task.inputs.in_file2 = Pial.sample(seed=3)
    task.inputs.subjects_dir = Directory.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mriscalc_2():
    task = MRIsCalc()
    task.inputs.in_file1 = Area.sample(seed=0)
    task.inputs.action = "add"
    task.inputs.out_file = "area.mid"
    task.inputs.in_file2 = Pial.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
