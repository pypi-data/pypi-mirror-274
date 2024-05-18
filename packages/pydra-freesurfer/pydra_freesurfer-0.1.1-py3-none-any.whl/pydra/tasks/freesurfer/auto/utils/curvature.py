from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Pial,
        {
            "help_string": "Input file for Curvature",
            "argstr": "{in_file}",
            "copyfile": True,
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "threshold",
        float,
        {
            "help_string": "Undocumented input threshold",
            "argstr": "-thresh {threshold:.3}",
        },
    ),
    ("n", bool, {"help_string": "Undocumented boolean flag", "argstr": "-n"}),
    (
        "averages",
        int,
        {
            "help_string": "Perform this number iterative averages of curvature measure before saving",
            "argstr": "-a {averages}",
        },
    ),
    (
        "save",
        bool,
        {
            "help_string": "Save curvature files (will only generate screen output without this option)",
            "argstr": "-w",
        },
    ),
    (
        "distances",
        ty.Any,
        {
            "help_string": "Undocumented input integer distances",
            "argstr": "-distances {distances[0]} {distances[1]}",
        },
    ),
    ("copy_input", bool, {"help_string": "Copy input file to current directory"}),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
Curvature_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_mean", File, {"help_string": "Mean curvature output file"}),
    ("out_gauss", File, {"help_string": "Gaussian curvature output file"}),
]
Curvature_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Curvature(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.utils.curvature import Curvature

    >>> task = Curvature()
    >>> task.inputs.in_file = Pial.mock("lh.pial")
    >>> task.inputs.save = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_curvature -w lh.pial'


    """

    input_spec = Curvature_input_spec
    output_spec = Curvature_output_spec
    executable = "mris_curvature"
