from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.model.mris_preproc import MRISPreproc
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mrispreproc_1():
    task = MRISPreproc()
    task.inputs.fsgd_file = File.sample(seed=6)
    task.inputs.subject_file = File.sample(seed=7)
    task.inputs.surf_measure_file = [File.sample(seed=8)]
    task.inputs.subjects_dir = Directory.sample(seed=18)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mrispreproc_2():
    task = MRISPreproc()
    task.inputs.out_file = "concatenated_file.mgz"
    task.inputs.target = "fsaverage"
    task.inputs.hemi = "lh"
    task.inputs.vol_measure_file = [
        ("cont1.nii", "register.dat"),
        ("cont1a.nii", "register.dat"),
    ]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
