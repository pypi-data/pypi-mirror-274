from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Pial
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_files",
        ty.List[Pial],
        {
            "help_string": "Two surfaces to be combined.",
            "argstr": "--combinesurfs {in_files}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Output filename. Combined surfaces from in_files.",
            "argstr": "{out_file}",
            "mandatory": True,
            "position": -1,
            "output_file_template": '"bh.pial"',
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
MRIsCombine_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
MRIsCombine_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MRIsCombine(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.utils.mr_is_combine import MRIsCombine

    >>> task = MRIsCombine()
    >>> task.inputs.in_files = [Pial.mock("lh.pial"), Pial.mock("rh.pial")]
    >>> task.inputs.out_file = "bh.pial"
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_convert --combinesurfs lh.pial rh.pial bh.pial'


    """

    input_spec = MRIsCombine_input_spec
    output_spec = MRIsCombine_output_spec
    executable = "mris_convert"
