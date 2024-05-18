from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.petsurfer.mrtm2 import MRTM2
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mrtm2_1():
    task = MRTM2()
    task.inputs.in_file = Nifti1.sample(seed=2)
    task.inputs.design = File.sample(seed=4)
    task.inputs.contrast = [File.sample(seed=5)]
    task.inputs.per_voxel_reg = [File.sample(seed=8)]
    task.inputs.weighted_ls = File.sample(seed=10)
    task.inputs.fixed_fx_var = File.sample(seed=11)
    task.inputs.fixed_fx_dof_file = File.sample(seed=13)
    task.inputs.weight_file = File.sample(seed=14)
    task.inputs.label_file = File.sample(seed=22)
    task.inputs.surf_geo = "white"
    task.inputs.sim_done_file = File.sample(seed=56)
    task.inputs.subjects_dir = Directory.sample(seed=59)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mrtm2_2():
    task = MRTM2()
    task.inputs.mrtm2 = ("ref_tac.dat", "timing.dat", 0.07872)
    task.inputs.glm_dir = "mrtm2"
    task.inputs.in_file = Nifti1.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
