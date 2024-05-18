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
            "help_string": "Input white matter file",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Output filled volume file name for MRIFill",
            "argstr": "{out_file}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "segmentation",
        File,
        {
            "help_string": "Input segmentation file for MRIFill",
            "argstr": "-segmentation {segmentation}",
        },
    ),
    (
        "transform",
        File,
        {
            "help_string": "Input transform file for MRIFill",
            "argstr": "-xform {transform}",
        },
    ),
    (
        "log_file",
        Path,
        {"help_string": "Output log file for MRIFill", "argstr": "-a {log_file}"},
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
MRIFill_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_file", MghGz, {"help_string": "Output file from MRIFill"}),
    ("log_file", File, {"help_string": "Output log file from MRIFill"}),
]
MRIFill_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MRIFill(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pydra.tasks.freesurfer.auto.utils.mri_fill import MRIFill

    >>> task = MRIFill()
    >>> task.inputs.in_file = MghGz.mock("wm.mgz" # doctest: +SKIP)
    >>> task.inputs.out_file = "filled.mgz" # doctest: +SKIP
    >>> task.inputs.segmentation = File.mock()
    >>> task.inputs.transform = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_fill wm.mgz filled.mgz'


    """

    input_spec = MRIFill_input_spec
    output_spec = MRIFill_output_spec
    executable = "mri_fill"
