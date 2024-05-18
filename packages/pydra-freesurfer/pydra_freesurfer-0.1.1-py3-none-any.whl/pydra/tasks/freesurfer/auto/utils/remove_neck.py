from fileformats.datascience import TextMatrix
from fileformats.generic import Directory
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
            "help_string": "Input file for RemoveNeck",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -4,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Output file for RemoveNeck",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": "{in_file}_noneck",
        },
    ),
    (
        "transform",
        TextMatrix,
        {
            "help_string": "Input transform file for RemoveNeck",
            "argstr": "{transform}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "template",
        TextMatrix,
        {
            "help_string": "Input template file for RemoveNeck",
            "argstr": "{template}",
            "mandatory": True,
            "position": -2,
        },
    ),
    ("radius", int, {"help_string": "Radius", "argstr": "-radius {radius}"}),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
RemoveNeck_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
RemoveNeck_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class RemoveNeck(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage import MghGz
    >>> from pydra.tasks.freesurfer.auto.utils.remove_neck import RemoveNeck

    >>> task = RemoveNeck()
    >>> task.inputs.in_file = MghGz.mock("norm.mgz")
    >>> task.inputs.transform = TextMatrix.mock("trans.mat")
    >>> task.inputs.template = TextMatrix.mock("trans.mat")
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_remove_neck norm.mgz trans.mat trans.mat norm_noneck.mgz'


    """

    input_spec = RemoveNeck_input_spec
    output_spec = RemoveNeck_output_spec
    executable = "mri_remove_neck"
