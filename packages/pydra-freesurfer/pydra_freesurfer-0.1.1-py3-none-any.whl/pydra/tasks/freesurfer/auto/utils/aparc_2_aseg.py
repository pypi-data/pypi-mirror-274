from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial
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
            "help_string": "Subject being processed",
            "argstr": "--s {subject_id}",
            "mandatory": True,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Full path of file to save the output segmentation in",
            "argstr": "--o {out_file}",
            "mandatory": True,
        },
    ),
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
    (
        "lh_ribbon",
        MghGz,
        {
            "help_string": "Input file must be <subject_id>/mri/lh.ribbon.mgz",
            "mandatory": True,
        },
    ),
    (
        "rh_ribbon",
        MghGz,
        {
            "help_string": "Input file must be <subject_id>/mri/rh.ribbon.mgz",
            "mandatory": True,
        },
    ),
    (
        "ribbon",
        MghGz,
        {
            "help_string": "Input file must be <subject_id>/mri/ribbon.mgz",
            "mandatory": True,
        },
    ),
    (
        "lh_annotation",
        Pial,
        {
            "help_string": "Input file must be <subject_id>/label/lh.aparc.annot",
            "mandatory": True,
        },
    ),
    (
        "rh_annotation",
        Pial,
        {
            "help_string": "Input file must be <subject_id>/label/rh.aparc.annot",
            "mandatory": True,
        },
    ),
    (
        "filled",
        File,
        {"help_string": "Implicit input filled file. Only required with FS v5.3."},
    ),
    ("aseg", File, {"help_string": "Input aseg file", "argstr": "--aseg {aseg}"}),
    ("volmask", bool, {"help_string": "Volume mask flag", "argstr": "--volmask"}),
    ("ctxseg", File, {"help_string": "", "argstr": "--ctxseg {ctxseg}"}),
    (
        "label_wm",
        bool,
        {
            "help_string": "For each voxel labeled as white matter in the aseg, re-assign\nits label to be that of the closest cortical point if its\ndistance is less than dmaxctx.",
            "argstr": "--labelwm",
        },
    ),
    (
        "hypo_wm",
        bool,
        {"help_string": "Label hypointensities as WM", "argstr": "--hypo-as-wm"},
    ),
    (
        "rip_unknown",
        bool,
        {
            "help_string": "Do not label WM based on 'unknown' corical label",
            "argstr": "--rip-unknown",
        },
    ),
    ("a2009s", bool, {"help_string": "Using the a2009s atlas", "argstr": "--a2009s"}),
    (
        "copy_inputs",
        bool,
        {
            "help_string": "If running as a node, set this to True.This will copy the input files to the node directory."
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
Aparc2Aseg_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", MghGz, {"help_string": "Output aseg file"})]
Aparc2Aseg_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Aparc2Aseg(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.utils.aparc_2_aseg import Aparc2Aseg

    >>> task = Aparc2Aseg()
    >>> task.inputs.out_file = "aparc+aseg.mgz"
    >>> task.inputs.lh_white = Pial.mock("lh.pial")
    >>> task.inputs.rh_white = Pial.mock("lh.pial")
    >>> task.inputs.lh_pial = Pial.mock("lh.pial")
    >>> task.inputs.rh_pial = Pial.mock("lh.pial")
    >>> task.inputs.lh_ribbon = MghGz.mock("label.mgz")
    >>> task.inputs.rh_ribbon = MghGz.mock("label.mgz")
    >>> task.inputs.ribbon = MghGz.mock("label.mgz")
    >>> task.inputs.lh_annotation = Pial.mock("lh.pial")
    >>> task.inputs.rh_annotation = Pial.mock("lh.pial")
    >>> task.inputs.filled = File.mock()
    >>> task.inputs.aseg = File.mock()
    >>> task.inputs.ctxseg = File.mock()
    >>> task.inputs.label_wm = True
    >>> task.inputs.rip_unknown = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_aparc2aseg --labelwm --o aparc+aseg.mgz --rip-unknown --s subject_id'


    """

    input_spec = Aparc2Aseg_input_spec
    output_spec = Aparc2Aseg_output_spec
    executable = "mri_aparc2aseg"
