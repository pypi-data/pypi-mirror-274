from fileformats.generic import Directory, File
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "source_file",
        File,
        {
            "help_string": "surface file with source values",
            "argstr": "--sval {source_file}",
            "mandatory": True,
            "xor": ["source_annot_file"],
        },
    ),
    (
        "source_annot_file",
        File,
        {
            "help_string": "surface annotation file",
            "argstr": "--sval-annot {source_annot_file}",
            "mandatory": True,
            "xor": ["source_file"],
        },
    ),
    (
        "source_subject",
        ty.Any,
        {
            "help_string": "subject id for source surface",
            "argstr": "--srcsubject {source_subject}",
            "mandatory": True,
        },
    ),
    (
        "hemi",
        ty.Any,
        {
            "help_string": "hemisphere to transform",
            "argstr": "--hemi {hemi}",
            "mandatory": True,
        },
    ),
    (
        "target_subject",
        ty.Any,
        {
            "help_string": "subject id of target surface",
            "argstr": "--trgsubject {target_subject}",
            "mandatory": True,
        },
    ),
    (
        "target_ico_order",
        ty.Any,
        {
            "help_string": "order of the icosahedron if target_subject is 'ico'",
            "argstr": "--trgicoorder {target_ico_order}",
        },
    ),
    (
        "source_type",
        ty.Any,
        {
            "help_string": "source file format",
            "argstr": "--sfmt {source_type}",
            "requires": ["source_file"],
        },
    ),
    (
        "target_type",
        ty.Any,
        {"help_string": "output format", "argstr": "--tfmt {target_type}"},
    ),
    (
        "reshape",
        bool,
        {
            "help_string": "reshape output surface to conform with Nifti",
            "argstr": "--reshape",
        },
    ),
    (
        "reshape_factor",
        int,
        {
            "help_string": "number of slices in reshaped image",
            "argstr": "--reshape-factor",
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "surface file to write",
            "argstr": "--tval {out_file}",
            "output_file_template": "out_file",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
SurfaceTransform_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
SurfaceTransform_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SurfaceTransform(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.auto.utils.surface_transform import SurfaceTransform

    """

    input_spec = SurfaceTransform_input_spec
    output_spec = SurfaceTransform_output_spec
    executable = "mri_surf2surf"
