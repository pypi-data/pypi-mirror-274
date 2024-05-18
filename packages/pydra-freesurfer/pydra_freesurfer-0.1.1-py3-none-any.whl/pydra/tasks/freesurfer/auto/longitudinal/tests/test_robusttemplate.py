from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.longitudinal.robust_template import RobustTemplate
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_robusttemplate_1():
    task = RobustTemplate()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.initial_transforms = [File.sample(seed=12)]
    task.inputs.in_intensity_scales = [File.sample(seed=13)]
    task.inputs.subjects_dir = Directory.sample(seed=15)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_robusttemplate_2():
    task = RobustTemplate()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.out_file = "T1.nii"
    task.inputs.auto_detect_sensitivity = True
    task.inputs.subsample_threshold = 200
    task.inputs.average_metric = "mean"
    task.inputs.initial_timepoint = 1
    task.inputs.fixed_timepoint = True
    task.inputs.no_iteration = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_robusttemplate_3():
    task = RobustTemplate()
    task.inputs.transform_outputs = ["structural.lta", "functional.lta"]
    task.inputs.scaled_intensity_outputs = [
        "structural-iscale.txt",
        "functional-iscale.txt",
    ]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_robusttemplate_4():
    task = RobustTemplate()
    task.inputs.transform_outputs = True
    task.inputs.scaled_intensity_outputs = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
