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
            "help_string": "input surface file",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "surface containing main component",
            "argstr": "{out_file}",
            "position": 2,
            "output_file_template": "{in_file}.maincmp",
        },
    ),
]
ExtractMainComponent_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ExtractMainComponent_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ExtractMainComponent(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.utils.extract_main_component import ExtractMainComponent

    >>> task = ExtractMainComponent()
    >>> task.inputs.in_file = Pial.mock("lh.pial")
    >>> task.cmdline
    'mris_extract_main_component lh.pial lh.maincmp'


    """

    input_spec = ExtractMainComponent_input_spec
    output_spec = ExtractMainComponent_output_spec
    executable = "mris_extract_main_component"
