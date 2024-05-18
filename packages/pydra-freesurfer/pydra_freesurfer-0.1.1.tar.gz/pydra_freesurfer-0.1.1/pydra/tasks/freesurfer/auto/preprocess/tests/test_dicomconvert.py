from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.dicom_convert import DICOMConvert
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_dicomconvert_1():
    task = DICOMConvert()
    task.inputs.dicom_dir = Directory.sample(seed=0)
    task.inputs.base_output_dir = Directory.sample(seed=1)
    task.inputs.subject_dir_template = "S.%04d"
    task.inputs.out_type = "niigz"
    task.inputs.dicom_info = File.sample(seed=6)
    task.inputs.subjects_dir = Directory.sample(seed=9)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
