from fileformats.datascience import DatFile
from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
from fileformats.medimage_freesurfer import Label
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.model.label_2_vol import Label2Vol
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_label2vol_1():
    task = Label2Vol()
    task.inputs.label_file = [Label.sample(seed=0)]
    task.inputs.annot_file = File.sample(seed=1)
    task.inputs.seg_file = File.sample(seed=2)
    task.inputs.template_file = Nifti1.sample(seed=4)
    task.inputs.reg_file = DatFile.sample(seed=5)
    task.inputs.reg_header = File.sample(seed=6)
    task.inputs.label_hit_file = File.sample(seed=16)
    task.inputs.map_label_stat = File.sample(seed=17)
    task.inputs.subjects_dir = Directory.sample(seed=19)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_label2vol_2():
    task = Label2Vol()
    task.inputs.label_file = [Label.sample(seed=0)]
    task.inputs.template_file = Nifti1.sample(seed=4)
    task.inputs.reg_file = DatFile.sample(seed=5)
    task.inputs.fill_thresh = 0.5
    task.inputs.vol_label_file = "foo_out.nii"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
