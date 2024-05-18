from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.model.one_sample_t_test import OneSampleTTest
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_onesamplettest_1():
    task = OneSampleTTest()
    task.inputs.in_file = File.sample(seed=1)
    task.inputs.design = File.sample(seed=3)
    task.inputs.contrast = [File.sample(seed=4)]
    task.inputs.per_voxel_reg = [File.sample(seed=7)]
    task.inputs.weighted_ls = File.sample(seed=9)
    task.inputs.fixed_fx_var = File.sample(seed=10)
    task.inputs.fixed_fx_dof_file = File.sample(seed=12)
    task.inputs.weight_file = File.sample(seed=13)
    task.inputs.label_file = File.sample(seed=21)
    task.inputs.surf_geo = "white"
    task.inputs.sim_done_file = File.sample(seed=56)
    task.inputs.subjects_dir = Directory.sample(seed=59)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
