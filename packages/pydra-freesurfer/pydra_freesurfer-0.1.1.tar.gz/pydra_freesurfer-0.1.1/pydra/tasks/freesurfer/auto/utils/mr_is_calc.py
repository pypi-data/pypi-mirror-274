from fileformats.audio import SpMidi
from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Area, Pial
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file1",
        Area,
        {
            "help_string": "Input file 1",
            "argstr": "{in_file1}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "action",
        ty.Any,
        {
            "help_string": "Action to perform on input file(s)",
            "argstr": "{action}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Output file after calculation",
            "argstr": "-o {out_file}",
            "mandatory": True,
        },
    ),
    (
        "in_file2",
        Pial,
        {
            "help_string": "Input file 2",
            "argstr": "{in_file2}",
            "position": -1,
            "xor": ["in_float", "in_int"],
        },
    ),
    (
        "in_float",
        float,
        {
            "help_string": "Input float",
            "argstr": "{in_float}",
            "position": -1,
            "xor": ["in_file2", "in_int"],
        },
    ),
    (
        "in_int",
        int,
        {
            "help_string": "Input integer",
            "argstr": "{in_int}",
            "position": -1,
            "xor": ["in_file2", "in_float"],
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
MRIsCalc_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", SpMidi, {"help_string": "Output file after calculation"})]
MRIsCalc_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MRIsCalc(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.audio import SpMidi
    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage_freesurfer import Area, Pial
    >>> from pydra.tasks.freesurfer.auto.utils.mr_is_calc import MRIsCalc

    >>> task = MRIsCalc()
    >>> task.inputs.in_file1 = Area.mock("lh.area" # doctest: +SKIP)
    >>> task.inputs.action = "add"
    >>> task.inputs.out_file = "area.mid"
    >>> task.inputs.in_file2 = Pial.mock("lh.area.pial" # doctest: +SKIP)
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_calc -o lh.area.mid lh.area add lh.area.pial'


    """

    input_spec = MRIsCalc_input_spec
    output_spec = MRIsCalc_output_spec
    executable = "mris_calc"
