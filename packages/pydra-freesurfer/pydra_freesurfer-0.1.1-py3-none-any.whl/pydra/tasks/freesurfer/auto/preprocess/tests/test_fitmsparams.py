from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.fit_ms_params import FitMSParams
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_fitmsparams_1():
    task = FitMSParams()
    task.inputs.in_files = [MghGz.sample(seed=0)]
    task.inputs.xfm_list = [File.sample(seed=4)]
    task.inputs.subjects_dir = Directory.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_fitmsparams_2():
    task = FitMSParams()
    task.inputs.in_files = [MghGz.sample(seed=0)]
    task.inputs.out_dir = "flash_parameters"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
