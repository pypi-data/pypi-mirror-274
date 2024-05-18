from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Pial
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_origsurf",
        Pial,
        {
            "help_string": "Original surface",
            "argstr": "{in_origsurf}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "in_mappedsurf",
        Pial,
        {
            "help_string": "Mapped surface",
            "argstr": "{in_mappedsurf}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Output Jacobian of the surface mapping",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": "{in_origsurf}.jacobian",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
Jacobian_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Jacobian_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Jacobian(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.utils.jacobian import Jacobian

    >>> task = Jacobian()
    >>> task.inputs.in_origsurf = Pial.mock("lh.pial")
    >>> task.inputs.in_mappedsurf = Pial.mock("lh.pial")
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_jacobian lh.pial lh.pial lh.jacobian'


    """

    input_spec = Jacobian_input_spec
    output_spec = Jacobian_output_spec
    executable = "mris_jacobian"
