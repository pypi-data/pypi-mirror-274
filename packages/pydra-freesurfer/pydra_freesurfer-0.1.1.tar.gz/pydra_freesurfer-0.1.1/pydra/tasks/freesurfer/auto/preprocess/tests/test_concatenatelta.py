from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Lta
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.preprocess.concatenate_lta import ConcatenateLTA
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_concatenatelta_1():
    task = ConcatenateLTA()
    task.inputs.in_lta1 = Lta.sample(seed=0)
    task.inputs.tal_source_file = File.sample(seed=7)
    task.inputs.tal_template_file = File.sample(seed=8)
    task.inputs.subjects_dir = Directory.sample(seed=10)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_concatenatelta_2():
    task = ConcatenateLTA()
    task.inputs.in_lta1 = Lta.sample(seed=0)
    task.inputs.in_lta2 = "lta2.lta"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_concatenatelta_3():
    task = ConcatenateLTA()
    task.inputs.in_lta2 = "identity.nofile"
    task.inputs.out_file = "inv1.lta"
    task.inputs.invert_1 = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_concatenatelta_4():
    task = ConcatenateLTA()
    task.inputs.out_type = "RAS2RAS"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
