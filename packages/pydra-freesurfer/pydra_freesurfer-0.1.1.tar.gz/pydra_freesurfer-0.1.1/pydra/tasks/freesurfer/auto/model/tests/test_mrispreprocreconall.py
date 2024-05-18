from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.model.mris_preproc_recon_all import MRISPreprocReconAll
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mrispreprocreconall_1():
    task = MRISPreprocReconAll()
    task.inputs.surf_measure_file = File.sample(seed=0)
    task.inputs.surfreg_files = [File.sample(seed=1)]
    task.inputs.lh_surfreg_target = File.sample(seed=2)
    task.inputs.rh_surfreg_target = File.sample(seed=3)
    task.inputs.subject_id = "subject_id"
    task.inputs.fsgd_file = File.sample(seed=12)
    task.inputs.subject_file = File.sample(seed=13)
    task.inputs.subjects_dir = Directory.sample(seed=23)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mrispreprocreconall_2():
    task = MRISPreprocReconAll()
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
