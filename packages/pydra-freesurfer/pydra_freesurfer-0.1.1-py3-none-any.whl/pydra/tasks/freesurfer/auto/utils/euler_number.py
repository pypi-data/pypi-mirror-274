from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Pial
import logging
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


def defects_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["defects"]


def euler_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["euler"]


input_fields = [
    (
        "in_file",
        Pial,
        {
            "help_string": "Input file for EulerNumber",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -1,
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
EulerNumber_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "euler",
        int,
        {
            "help_string": "Euler number of cortical surface. A value of 2 signals a topologically correct surface model with no holes",
            "callable": "euler_callable",
        },
    ),
    (
        "defects",
        int,
        {"help_string": "Number of defects", "callable": "defects_callable"},
    ),
]
EulerNumber_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class EulerNumber(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.utils.euler_number import EulerNumber

    >>> task = EulerNumber()
    >>> task.inputs.in_file = Pial.mock("lh.pial")
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_euler_number lh.pial'


    """

    input_spec = EulerNumber_input_spec
    output_spec = EulerNumber_output_spec
    executable = "mris_euler_number"
