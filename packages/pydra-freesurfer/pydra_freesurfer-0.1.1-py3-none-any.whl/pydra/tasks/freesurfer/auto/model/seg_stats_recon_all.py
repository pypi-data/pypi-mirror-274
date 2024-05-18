from fileformats.datascience import TextMatrix
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial
from fileformats.text import TextFile
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "subject_id",
        ty.Any,
        {
            "help_string": "Subject id being processed",
            "argstr": "--subject {subject_id}",
            "mandatory": True,
        },
    ),
    ("ribbon", MghGz, {"help_string": "Input file mri/ribbon.mgz", "mandatory": True}),
    ("presurf_seg", MghGz, {"help_string": "Input segmentation volume"}),
    (
        "transform",
        TextMatrix,
        {"help_string": "Input transform file", "mandatory": True},
    ),
    ("lh_orig_nofix", Pial, {"help_string": "Input lh.orig.nofix", "mandatory": True}),
    ("rh_orig_nofix", Pial, {"help_string": "Input rh.orig.nofix", "mandatory": True}),
    (
        "lh_white",
        Pial,
        {
            "help_string": "Input file must be <subject_id>/surf/lh.white",
            "mandatory": True,
        },
    ),
    (
        "rh_white",
        Pial,
        {
            "help_string": "Input file must be <subject_id>/surf/rh.white",
            "mandatory": True,
        },
    ),
    (
        "lh_pial",
        Pial,
        {
            "help_string": "Input file must be <subject_id>/surf/lh.pial",
            "mandatory": True,
        },
    ),
    (
        "rh_pial",
        Pial,
        {
            "help_string": "Input file must be <subject_id>/surf/rh.pial",
            "mandatory": True,
        },
    ),
    ("aseg", File, {"help_string": "Mandatory implicit input in 5.3"}),
    (
        "copy_inputs",
        bool,
        {
            "help_string": "If running as a node, set this to True otherwise, this will copy the implicit inputs to the node directory."
        },
    ),
    (
        "segmentation_file",
        File,
        {
            "help_string": "segmentation volume path",
            "argstr": "--seg {segmentation_file}",
            "mandatory": True,
            "xor": ("segmentation_file", "annot", "surf_label"),
        },
    ),
    (
        "annot",
        ty.Any,
        {
            "help_string": "subject hemi parc : use surface parcellation",
            "argstr": "--annot {annot[0]} {annot[1]} {annot[2]}",
            "mandatory": True,
            "xor": ("segmentation_file", "annot", "surf_label"),
        },
    ),
    (
        "surf_label",
        ty.Any,
        {
            "help_string": "subject hemi label : use surface label",
            "argstr": "--slabel {surf_label[0]} {surf_label[1]} {surf_label[2]}",
            "mandatory": True,
            "xor": ("segmentation_file", "annot", "surf_label"),
        },
    ),
    (
        "summary_file",
        Path,
        {
            "help_string": "Segmentation stats summary table file",
            "argstr": "--sum {summary_file}",
            "position": -1,
            "output_file_template": '"summary.stats"',
        },
    ),
    (
        "partial_volume_file",
        File,
        {
            "help_string": "Compensate for partial voluming",
            "argstr": "--pv {partial_volume_file}",
        },
    ),
    (
        "in_file",
        File,
        {
            "help_string": "Use the segmentation to report stats on this volume",
            "argstr": "--i {in_file}",
        },
    ),
    (
        "frame",
        int,
        {
            "help_string": "Report stats on nth frame of input volume",
            "argstr": "--frame {frame}",
        },
    ),
    (
        "multiply",
        float,
        {"help_string": "multiply input by val", "argstr": "--mul {multiply}"},
    ),
    (
        "calc_snr",
        bool,
        {
            "help_string": "save mean/std as extra column in output table",
            "argstr": "--snr",
        },
    ),
    (
        "calc_power",
        ty.Any,
        {
            "help_string": "Compute either the sqr or the sqrt of the input",
            "argstr": "--{calc_power}",
        },
    ),
    (
        "color_table_file",
        File,
        {
            "help_string": "color table file with seg id names",
            "argstr": "--ctab {color_table_file}",
            "xor": ("color_table_file", "default_color_table", "gca_color_table"),
        },
    ),
    (
        "default_color_table",
        bool,
        {
            "help_string": "use $FREESURFER_HOME/FreeSurferColorLUT.txt",
            "argstr": "--ctab-default",
            "xor": ("color_table_file", "default_color_table", "gca_color_table"),
        },
    ),
    (
        "gca_color_table",
        File,
        {
            "help_string": "get color table from GCA (CMA)",
            "argstr": "--ctab-gca {gca_color_table}",
            "xor": ("color_table_file", "default_color_table", "gca_color_table"),
        },
    ),
    (
        "segment_id",
        list,
        {
            "help_string": "Manually specify segmentation ids",
            "argstr": "--id {segment_id}...",
        },
    ),
    (
        "exclude_id",
        int,
        {
            "help_string": "Exclude seg id from report",
            "argstr": "--excludeid {exclude_id}",
        },
    ),
    (
        "exclude_ctx_gm_wm",
        bool,
        {
            "help_string": "exclude cortical gray and white matter",
            "argstr": "--excl-ctxgmwm",
        },
    ),
    (
        "wm_vol_from_surf",
        bool,
        {"help_string": "Compute wm volume from surf", "argstr": "--surf-wm-vol"},
    ),
    (
        "cortex_vol_from_surf",
        bool,
        {"help_string": "Compute cortex volume from surf", "argstr": "--surf-ctx-vol"},
    ),
    (
        "non_empty_only",
        bool,
        {"help_string": "Only report nonempty segmentations", "argstr": "--nonempty"},
    ),
    (
        "empty",
        bool,
        {
            "help_string": "Report on segmentations listed in the color table",
            "argstr": "--empty",
        },
    ),
    (
        "mask_file",
        File,
        {
            "help_string": "Mask volume (same size as seg",
            "argstr": "--mask {mask_file}",
        },
    ),
    (
        "mask_thresh",
        float,
        {
            "help_string": "binarize mask with this threshold <0.5>",
            "argstr": "--maskthresh {mask_thresh}",
        },
    ),
    ("mask_sign", ty.Any, {"help_string": "Sign for mask threshold: pos, neg, or abs"}),
    (
        "mask_frame",
        int,
        {
            "help_string": "Mask with this (0 based) frame of the mask volume",
            "requires": ["mask_file"],
        },
    ),
    (
        "mask_invert",
        bool,
        {"help_string": "Invert binarized mask volume", "argstr": "--maskinvert"},
    ),
    (
        "mask_erode",
        int,
        {
            "help_string": "Erode mask by some amount",
            "argstr": "--maskerode {mask_erode}",
        },
    ),
    (
        "brain_vol",
        ty.Any,
        {
            "help_string": "Compute brain volume either with ``brainmask`` or ``brain-vol-from-seg``",
            "argstr": "--{brain_vol}",
        },
    ),
    (
        "brainmask_file",
        File,
        {
            "help_string": "Load brain mask and compute the volume of the brain as the non-zero voxels in this volume",
            "argstr": "--brainmask {brainmask_file}",
        },
    ),
    (
        "etiv",
        bool,
        {"help_string": "Compute ICV from talairach transform", "argstr": "--etiv"},
    ),
    (
        "etiv_only",
        ty.Any,
        {"help_string": "Compute etiv and exit.  Use ``etiv`` or ``old-etiv``"},
    ),
    (
        "avgwf_txt_file",
        ty.Any,
        {
            "help_string": "Save average waveform into file (bool or filename)",
            "argstr": "--avgwf {avgwf_txt_file}",
        },
    ),
    (
        "avgwf_file",
        ty.Any,
        {
            "help_string": "Save as binary volume (bool or filename)",
            "argstr": "--avgwfvol {avgwf_file}",
        },
    ),
    (
        "sf_avg_file",
        ty.Any,
        {
            "help_string": "Save mean across space and time",
            "argstr": "--sfavg {sf_avg_file}",
        },
    ),
    (
        "vox",
        list,
        {
            "help_string": "Replace seg with all 0s except at C R S (three int inputs)",
            "argstr": "--vox {vox}",
        },
    ),
    (
        "supratent",
        bool,
        {"help_string": "Undocumented input flag", "argstr": "--supratent"},
    ),
    (
        "subcort_gm",
        bool,
        {
            "help_string": "Compute volume of subcortical gray matter",
            "argstr": "--subcortgray",
        },
    ),
    (
        "total_gray",
        bool,
        {"help_string": "Compute volume of total gray matter", "argstr": "--totalgray"},
    ),
    (
        "euler",
        bool,
        {
            "help_string": "Write out number of defect holes in orig.nofix based on the euler number",
            "argstr": "--euler",
        },
    ),
    (
        "in_intensity",
        File,
        {
            "help_string": "Undocumented input norm.mgz file",
            "argstr": "--in {in_intensity[0]} --in-intensity-name {in_intensity[1]}",
        },
    ),
    (
        "intensity_units",
        ty.Any,
        {
            "help_string": "Intensity units",
            "argstr": "--in-intensity-units {intensity_units}",
            "requires": ["in_intensity"],
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
SegStatsReconAll_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "avgwf_txt_file",
        TextFile,
        {"help_string": "Text file with functional statistics averaged over segs"},
    ),
    (
        "avgwf_file",
        File,
        {"help_string": "Volume with functional statistics averaged over segs"},
    ),
    (
        "sf_avg_file",
        File,
        {"help_string": "Text file with func statistics averaged over segs and framss"},
    ),
]
SegStatsReconAll_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SegStatsReconAll(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.freesurfer.auto.model.seg_stats_recon_all import SegStatsReconAll

    >>> task = SegStatsReconAll()
    >>> task.inputs.subject_id = "10335"
    >>> task.inputs.ribbon = MghGz.mock("wm.mgz")
    >>> task.inputs.presurf_seg = MghGz.mock("wm.mgz")
    >>> task.inputs.transform = TextMatrix.mock("trans.mat")
    >>> task.inputs.lh_orig_nofix = Pial.mock("lh.pial")
    >>> task.inputs.rh_orig_nofix = Pial.mock("lh.pial")
    >>> task.inputs.lh_white = Pial.mock("lh.pial")
    >>> task.inputs.rh_white = Pial.mock("lh.pial")
    >>> task.inputs.lh_pial = Pial.mock("lh.pial")
    >>> task.inputs.rh_pial = Pial.mock("lh.pial")
    >>> task.inputs.aseg = File.mock()
    >>> task.inputs.segmentation_file = File.mock()
    >>> task.inputs.annot = ("PWS04", "lh", "aparc")
    >>> task.inputs.summary_file = "summary.stats"
    >>> task.inputs.partial_volume_file = File.mock()
    >>> task.inputs.in_file = File.mock()
    >>> task.inputs.color_table_file = File.mock()
    >>> task.inputs.gca_color_table = File.mock()
    >>> task.inputs.exclude_id = 0
    >>> task.inputs.exclude_ctx_gm_wm = True
    >>> task.inputs.wm_vol_from_surf = True
    >>> task.inputs.cortex_vol_from_surf = True
    >>> task.inputs.empty = True
    >>> task.inputs.mask_file = File.mock()
    >>> task.inputs.brain_vol = "brain-vol-from-seg"
    >>> task.inputs.brainmask_file = File.mock()
    >>> task.inputs.etiv = True
    >>> task.inputs.avgwf_txt_file = "avgwf.txt"
    >>> task.inputs.supratent = True
    >>> task.inputs.subcort_gm = True
    >>> task.inputs.total_gray = True
    >>> task.inputs.euler = True
    >>> task.inputs.in_intensity = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_segstats --annot PWS04 lh aparc --avgwf ./avgwf.txt --brain-vol-from-seg --surf-ctx-vol --empty --etiv --euler --excl-ctxgmwm --excludeid 0 --subcortgray --subject 10335 --supratent --totalgray --surf-wm-vol --sum ./summary.stats'


    """

    input_spec = SegStatsReconAll_input_spec
    output_spec = SegStatsReconAll_output_spec
    executable = "mri_segstats"
