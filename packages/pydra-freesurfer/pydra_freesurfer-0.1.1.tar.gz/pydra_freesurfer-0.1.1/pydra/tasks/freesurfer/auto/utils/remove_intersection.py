from fileformats.generic import Directory
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
            "help_string": "Input file for RemoveIntersection",
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
            "help_string": "Output file for RemoveIntersection",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": "{in_file}",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
RemoveIntersection_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
RemoveIntersection_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class RemoveIntersection(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.utils.remove_intersection import RemoveIntersection

    >>> task = RemoveIntersection()
    >>> task.inputs.in_file = Pial.mock("lh.pial")
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_remove_intersection lh.pial lh.pial'


    """

    input_spec = RemoveIntersection_input_spec
    output_spec = RemoveIntersection_output_spec
    executable = "mris_remove_intersection"
