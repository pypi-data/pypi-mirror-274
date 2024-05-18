from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Pial,
        {
            "help_string": "Input file for Sphere",
            "argstr": "{in_file}",
            "copyfile": True,
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Output file for Sphere",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": "{in_file}.sphere",
        },
    ),
    (
        "seed",
        int,
        {
            "help_string": "Seed for setting random number generator",
            "argstr": "-seed {seed}",
        },
    ),
    (
        "magic",
        bool,
        {
            "help_string": "No documentation. Direct questions to analysis-bugs@nmr.mgh.harvard.edu",
            "argstr": "-q",
        },
    ),
    (
        "in_smoothwm",
        File,
        {
            "help_string": "Input surface required when -q flag is not selected",
            "copyfile": True,
        },
    ),
    ("num_threads", int, {"help_string": "allows for specifying more threads"}),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
Sphere_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Sphere_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Sphere(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.utils.sphere import Sphere

    >>> task = Sphere()
    >>> task.inputs.in_file = Pial.mock("lh.pial")
    >>> task.inputs.in_smoothwm = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_sphere lh.pial lh.sphere'


    """

    input_spec = Sphere_input_spec
    output_spec = Sphere_output_spec
    executable = "mris_sphere"
