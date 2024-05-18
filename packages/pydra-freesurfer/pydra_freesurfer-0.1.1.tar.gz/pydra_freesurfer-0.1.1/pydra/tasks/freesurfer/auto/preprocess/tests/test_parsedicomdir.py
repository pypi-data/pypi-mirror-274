from fileformats.generic import Directory
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.parse_dicom_dir import ParseDICOMDir
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_parsedicomdir_1():
    task = ParseDICOMDir()
    task.inputs.dicom_dir = Directory.sample(seed=0)
    task.inputs.dicom_info_file = "dicominfo.txt"
    task.inputs.subjects_dir = Directory.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_parsedicomdir_2():
    task = ParseDICOMDir()
    task.inputs.dicom_dir = "."
    task.inputs.sortbyrun = True
    task.inputs.summarize = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
