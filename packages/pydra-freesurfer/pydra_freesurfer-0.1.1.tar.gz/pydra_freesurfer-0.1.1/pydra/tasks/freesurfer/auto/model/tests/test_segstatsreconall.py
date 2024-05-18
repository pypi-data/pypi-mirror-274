from fileformats.datascience import TextMatrix
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.auto.model.seg_stats_recon_all import SegStatsReconAll
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_segstatsreconall_1():
    task = SegStatsReconAll()
    task.inputs.ribbon = MghGz.sample(seed=1)
    task.inputs.presurf_seg = MghGz.sample(seed=2)
    task.inputs.transform = TextMatrix.sample(seed=3)
    task.inputs.lh_orig_nofix = Pial.sample(seed=4)
    task.inputs.rh_orig_nofix = Pial.sample(seed=5)
    task.inputs.lh_white = Pial.sample(seed=6)
    task.inputs.rh_white = Pial.sample(seed=7)
    task.inputs.lh_pial = Pial.sample(seed=8)
    task.inputs.rh_pial = Pial.sample(seed=9)
    task.inputs.aseg = File.sample(seed=10)
    task.inputs.segmentation_file = File.sample(seed=12)
    task.inputs.partial_volume_file = File.sample(seed=16)
    task.inputs.in_file = File.sample(seed=17)
    task.inputs.color_table_file = File.sample(seed=22)
    task.inputs.gca_color_table = File.sample(seed=24)
    task.inputs.mask_file = File.sample(seed=32)
    task.inputs.brainmask_file = File.sample(seed=39)
    task.inputs.in_intensity = File.sample(seed=50)
    task.inputs.subjects_dir = Directory.sample(seed=52)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_segstatsreconall_2():
    task = SegStatsReconAll()
    task.inputs.subject_id = "10335"
    task.inputs.ribbon = MghGz.sample(seed=1)
    task.inputs.presurf_seg = MghGz.sample(seed=2)
    task.inputs.transform = TextMatrix.sample(seed=3)
    task.inputs.lh_orig_nofix = Pial.sample(seed=4)
    task.inputs.rh_orig_nofix = Pial.sample(seed=5)
    task.inputs.lh_white = Pial.sample(seed=6)
    task.inputs.rh_white = Pial.sample(seed=7)
    task.inputs.lh_pial = Pial.sample(seed=8)
    task.inputs.rh_pial = Pial.sample(seed=9)
    task.inputs.annot = ("PWS04", "lh", "aparc")
    task.inputs.summary_file = "summary.stats"
    task.inputs.exclude_id = 0
    task.inputs.exclude_ctx_gm_wm = True
    task.inputs.wm_vol_from_surf = True
    task.inputs.cortex_vol_from_surf = True
    task.inputs.empty = True
    task.inputs.brain_vol = "brain-vol-from-seg"
    task.inputs.etiv = True
    task.inputs.avgwf_txt_file = "avgwf.txt"
    task.inputs.supratent = True
    task.inputs.subcort_gm = True
    task.inputs.total_gray = True
    task.inputs.euler = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
