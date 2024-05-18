from fileformats.generic import Directory, File
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        File,
        {
            "help_string": "Input volume to tessellate voxels from.",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "label_value",
        int,
        {
            "help_string": 'Label value which to tessellate from the input volume. (integer, if input is "filled.mgz" volume, 127 is rh, 255 is lh)',
            "argstr": "{label_value}",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "connectivity_value",
        int,
        1,
        {
            "help_string": "Alter the marching cubes connectivity: 1=6+,2=18,3=6,4=26 (default=1)",
            "argstr": "{connectivity_value}",
            "position": -1,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output filename or True to generate one",
            "argstr": "./{out_file}",
            "position": -2,
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
MRIMarchingCubes_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("surface", File, {"help_string": "binary surface of the tessellation "})
]
MRIMarchingCubes_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MRIMarchingCubes(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.auto.utils.mri_marching_cubes import MRIMarchingCubes

    """

    input_spec = MRIMarchingCubes_input_spec
    output_spec = MRIMarchingCubes_output_spec
    executable = "mri_mc"
