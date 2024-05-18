from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        MghGz,
        {
            "help_string": "The input file for Normalize",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "The output file for Normalize",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": "{in_file}_norm",
        },
    ),
    (
        "gradient",
        int,
        {
            "help_string": "use max intensity/mm gradient g (default=1)",
            "argstr": "-g {gradient}",
        },
    ),
    (
        "mask",
        File,
        {"help_string": "The input mask file for Normalize", "argstr": "-mask {mask}"},
    ),
    (
        "segmentation",
        File,
        {
            "help_string": "The input segmentation for Normalize",
            "argstr": "-aseg {segmentation}",
        },
    ),
    (
        "transform",
        File,
        {"help_string": "Transform file from the header of the input file"},
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
Normalize_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Normalize_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Normalize(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pydra.tasks.freesurfer.auto.preprocess.normalize import Normalize

    >>> task = Normalize()
    >>> task.inputs.in_file = MghGz.mock("T1.mgz")
    >>> task.inputs.gradient = 1
    >>> task.inputs.mask = File.mock()
    >>> task.inputs.segmentation = File.mock()
    >>> task.inputs.transform = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_normalize -g 1 T1.mgz T1_norm.mgz'


    """

    input_spec = Normalize_input_spec
    output_spec = Normalize_output_spec
    executable = "mri_normalize"
