from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.model.label_2_annot import Label2Annot
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_label2annot_1():
    task = Label2Annot()
    task.inputs.orig = Pial.sample(seed=4)
    task.inputs.color_table = File.sample(seed=7)
    task.inputs.subjects_dir = Directory.sample(seed=9)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_label2annot_2():
    task = Label2Annot()
    task.inputs.hemisphere = "lh"
    task.inputs.subject_id = "10335"
    task.inputs.in_labels = ["lh.aparc.label"]
    task.inputs.out_annot = "test"
    task.inputs.orig = Pial.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
