from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.model.ms__lda import MS_LDA
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_ms_lda_1():
    task = MS_LDA()
    task.inputs.label_file = MghGz.sample(seed=3)
    task.inputs.mask_file = File.sample(seed=4)
    task.inputs.images = [MghGz.sample(seed=8)]
    task.inputs.subjects_dir = Directory.sample(seed=9)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_ms_lda_2():
    task = MS_LDA()
    task.inputs.lda_labels = [grey_label, white_label]
    task.inputs.weight_file = "weights.txt"
    task.inputs.vol_synth_file = "synth_out.mgz"
    task.inputs.label_file = MghGz.sample(seed=3)
    task.inputs.shift = zero_value
    task.inputs.conform = True
    task.inputs.use_weights = True
    task.inputs.images = [MghGz.sample(seed=8)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
