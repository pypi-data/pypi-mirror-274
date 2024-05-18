from fileformats.generic import Directory
from fileformats.medimage import MghGz
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        MghGz,
        {
            "help_string": "source surface file",
            "argstr": "--sval {in_file}",
            "mandatory": True,
        },
    ),
    (
        "subject_id",
        ty.Any,
        {
            "help_string": "subject id of surface file",
            "argstr": "--s {subject_id}",
            "mandatory": True,
        },
    ),
    (
        "hemi",
        ty.Any,
        {
            "help_string": "hemisphere to operate on",
            "argstr": "--hemi {hemi}",
            "mandatory": True,
        },
    ),
    (
        "fwhm",
        float,
        {
            "help_string": "effective FWHM of the smoothing process",
            "argstr": "--fwhm {fwhm:.4}",
            "xor": ["smooth_iters"],
        },
    ),
    (
        "smooth_iters",
        int,
        {
            "help_string": "iterations of the smoothing process",
            "argstr": "--smooth {smooth_iters}",
            "xor": ["fwhm"],
        },
    ),
    (
        "cortex",
        bool,
        True,
        {
            "help_string": "only smooth within ``$hemi.cortex.label``",
            "argstr": "--cortex",
        },
    ),
    (
        "reshape",
        bool,
        {
            "help_string": "reshape surface vector to fit in non-mgh format",
            "argstr": "--reshape",
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
SurfaceSmooth_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
SurfaceSmooth_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SurfaceSmooth(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage import MghGz
    >>> from pydra.tasks.freesurfer.auto.utils.surface_smooth import SurfaceSmooth

    >>> task = SurfaceSmooth()
    >>> task.inputs.in_file = MghGz.mock("lh.cope1.mgz")
    >>> task.inputs.subject_id = "subj_1"
    >>> task.inputs.hemi = "lh"
    >>> task.inputs.fwhm = 5
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_surf2surf --cortex --fwhm 5.0000 --hemi lh --sval lh.cope1.mgz --tval ...lh.cope1_smooth5.mgz --s subj_1'


    """

    input_spec = SurfaceSmooth_input_spec
    output_spec = SurfaceSmooth_output_spec
    executable = "mri_surf2surf"
