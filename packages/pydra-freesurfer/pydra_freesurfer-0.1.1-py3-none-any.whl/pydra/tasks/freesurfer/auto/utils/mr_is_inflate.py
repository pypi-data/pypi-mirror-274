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
            "help_string": "Input file for MRIsInflate",
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
            "help_string": "Output file for MRIsInflate",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": "{in_file}.inflated",
        },
    ),
    ("out_sulc", Path, {"help_string": "Output sulc file", "xor": ["no_save_sulc"]}),
    (
        "no_save_sulc",
        bool,
        {
            "help_string": "Do not save sulc file as output",
            "argstr": "-no-save-sulc",
            "xor": ["out_sulc"],
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
MRIsInflate_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_sulc", File, {"help_string": "Output sulc file"})]
MRIsInflate_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MRIsInflate(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.utils.mr_is_inflate import MRIsInflate

    >>> task = MRIsInflate()
    >>> task.inputs.in_file = Pial.mock("lh.pial")
    >>> task.inputs.no_save_sulc = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_inflate -no-save-sulc lh.pial lh.inflated'


    """

    input_spec = MRIsInflate_input_spec
    output_spec = MRIsInflate_output_spec
    executable = "mris_inflate"
