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
            "position": -3,
        },
    ),
    (
        "label_value",
        int,
        {
            "help_string": 'Label value which to tessellate from the input volume. (integer, if input is "filled.mgz" volume, 127 is rh, 255 is lh)',
            "argstr": "{label_value}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output filename or True to generate one",
            "argstr": "{out_file}",
            "position": -1,
        },
    ),
    (
        "tesselate_all_voxels",
        bool,
        {
            "help_string": "Tessellate the surface of all voxels with different labels",
            "argstr": "-a",
        },
    ),
    (
        "use_real_RAS_coordinates",
        bool,
        {
            "help_string": "Saves surface with real RAS coordinates where c_(r,a,s) != 0",
            "argstr": "-n",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
MRITessellate_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("surface", File, {"help_string": "binary surface of the tessellation "})
]
MRITessellate_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MRITessellate(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.auto.utils.mri_tessellate import MRITessellate

    """

    input_spec = MRITessellate_input_spec
    output_spec = MRITessellate_output_spec
    executable = "mri_tessellate"
