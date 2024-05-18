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
        {
            "help_string": "file to resample",
            "argstr": "-i {in_file}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "resampled_file",
        Path,
        {
            "help_string": "output filename",
            "argstr": "-o {resampled_file}",
            "position": -1,
            "output_file_template": '"resampled.nii"',
        },
    ),
    (
        "voxel_size",
        ty.Any,
        {
            "help_string": "triplet of output voxel sizes",
            "argstr": "-vs {voxel_size[0]:.2} {voxel_size[1]:.2} {voxel_size[2]:.2}",
            "mandatory": True,
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
Resample_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Resample_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Resample(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.freesurfer.auto.preprocess.resample import Resample

    >>> task = Resample()
    >>> task.inputs.in_file = Nifti1.mock("structural.nii")
    >>> task.inputs.resampled_file = "resampled.nii"
    >>> task.inputs.voxel_size = (2.1, 2.1, 2.1)
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_convert -vs 2.10 2.10 2.10 -i structural.nii -o resampled.nii'


    """

    input_spec = Resample_input_spec
    output_spec = Resample_output_spec
    executable = "mri_convert"
