from fileformats.datascience import DatFile
from fileformats.generic import Directory
from fileformats.medimage import Nifti1
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Nifti1,
        {"help_string": "source volume", "argstr": "--i {in_file}", "mandatory": True},
    ),
    (
        "reg_file",
        DatFile,
        {
            "help_string": "registers volume to surface anatomical ",
            "argstr": "--reg {reg_file}",
            "mandatory": True,
        },
    ),
    (
        "smoothed_file",
        Path,
        {
            "help_string": "output volume",
            "argstr": "--o {smoothed_file}",
            "output_file_template": '"foo_out.nii"',
        },
    ),
    (
        "proj_frac_avg",
        ty.Any,
        {
            "help_string": "average a long normal min max delta",
            "argstr": "--projfrac-avg {proj_frac_avg[0]:.2} {proj_frac_avg[1]:.2} {proj_frac_avg[2]:.2}",
            "xor": ["proj_frac"],
        },
    ),
    (
        "proj_frac",
        float,
        {
            "help_string": "project frac of thickness a long surface normal",
            "argstr": "--projfrac {proj_frac}",
            "xor": ["proj_frac_avg"],
        },
    ),
    (
        "surface_fwhm",
        ty.Any,
        {
            "help_string": "surface FWHM in mm",
            "argstr": "--fwhm {surface_fwhm}",
            "mandatory": True,
            "requires": ["reg_file"],
            "xor": ["num_iters"],
        },
    ),
    (
        "num_iters",
        ty.Any,
        {
            "help_string": "number of iterations instead of fwhm",
            "argstr": "--niters {num_iters}",
            "mandatory": True,
            "xor": ["surface_fwhm"],
        },
    ),
    (
        "vol_fwhm",
        ty.Any,
        {
            "help_string": "volume smoothing outside of surface",
            "argstr": "--vol-fwhm {vol_fwhm}",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
Smooth_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Smooth_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Smooth(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience import DatFile
    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.freesurfer.auto.preprocess.smooth import Smooth

    >>> task = Smooth()
    >>> task.inputs.in_file = Nifti1.mock("functional.nii")
    >>> task.inputs.reg_file = DatFile.mock("register.dat")
    >>> task.inputs.smoothed_file = "foo_out.nii"
    >>> task.inputs.surface_fwhm = 10
    >>> task.inputs.vol_fwhm = 6
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_volsmooth --i functional.nii --reg register.dat --o foo_out.nii --fwhm 10.000000 --vol-fwhm 6.000000'


    """

    input_spec = Smooth_input_spec
    output_spec = Smooth_output_spec
    executable = "mris_volsmooth"
