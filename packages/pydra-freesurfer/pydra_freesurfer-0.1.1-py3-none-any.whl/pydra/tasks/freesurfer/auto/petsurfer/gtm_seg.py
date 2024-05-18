from fileformats.generic import Directory, File
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "subject_id",
        ty.Any,
        {"help_string": "subject id", "argstr": "--s {subject_id}", "mandatory": True},
    ),
    (
        "xcerseg",
        bool,
        {
            "help_string": "run xcerebralseg on this subject to create apas+head.mgz",
            "argstr": "--xcerseg",
        },
    ),
    (
        "out_file",
        Path,
        "gtmseg.mgz",
        {
            "help_string": "output volume relative to subject/mri",
            "argstr": "--o {out_file}",
        },
    ),
    (
        "upsampling_factor",
        int,
        {
            "help_string": "upsampling factor (default is 2)",
            "argstr": "--usf {upsampling_factor}",
        },
    ),
    (
        "subsegwm",
        bool,
        {"help_string": "subsegment WM into lobes (default)", "argstr": "--subsegwm"},
    ),
    (
        "keep_hypo",
        bool,
        {
            "help_string": "do not relabel hypointensities as WM when subsegmenting WM",
            "argstr": "--keep-hypo",
        },
    ),
    (
        "keep_cc",
        bool,
        {"help_string": "do not relabel corpus callosum as WM", "argstr": "--keep-cc"},
    ),
    (
        "dmax",
        float,
        {
            "help_string": "distance threshold to use when subsegmenting WM (default is 5)",
            "argstr": "--dmax {dmax}",
        },
    ),
    (
        "ctx_annot",
        ty.Any,
        {
            "help_string": "annot lhbase rhbase : annotation to use for cortical segmentation (default is aparc 1000 2000)",
            "argstr": "--ctx-annot {ctx_annot[0]} {ctx_annot[1]} {ctx_annot[2]}",
        },
    ),
    (
        "wm_annot",
        ty.Any,
        {
            "help_string": "annot lhbase rhbase : annotation to use for WM segmentation (with --subsegwm, default is lobes 3200 4200)",
            "argstr": "--wm-annot {wm_annot[0]} {wm_annot[1]} {wm_annot[2]}",
        },
    ),
    (
        "output_upsampling_factor",
        int,
        {
            "help_string": "set output USF different than USF, mostly for debugging",
            "argstr": "--output-usf {output_upsampling_factor}",
        },
    ),
    (
        "head",
        ty.Any,
        {
            "help_string": "use headseg instead of apas+head.mgz",
            "argstr": "--head {head}",
        },
    ),
    (
        "subseg_cblum_wm",
        bool,
        {
            "help_string": "subsegment cerebellum WM into core and gyri",
            "argstr": "--subseg-cblum-wm",
        },
    ),
    (
        "no_pons",
        bool,
        {
            "help_string": "do not add pons segmentation when doing ---xcerseg",
            "argstr": "--no-pons",
        },
    ),
    (
        "no_vermis",
        bool,
        {
            "help_string": "do not add vermis segmentation when doing ---xcerseg",
            "argstr": "--no-vermis",
        },
    ),
    (
        "colortable",
        File,
        {"help_string": "colortable", "argstr": "--ctab {colortable}"},
    ),
    (
        "no_seg_stats",
        bool,
        {
            "help_string": "do not compute segmentation stats",
            "argstr": "--no-seg-stats",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
GTMSeg_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", File, {"help_string": "GTM segmentation"})]
GTMSeg_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class GTMSeg(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.auto.petsurfer.gtm_seg import GTMSeg

    >>> task = GTMSeg()
    >>> task.inputs.subject_id = "subject_id"
    >>> task.inputs.colortable = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'gtmseg --o gtmseg.mgz --s subject_id'


    """

    input_spec = GTMSeg_input_spec
    output_spec = GTMSeg_output_spec
    executable = "gtmseg"
