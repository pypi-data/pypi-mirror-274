from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Lta
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_lta1",
        Lta,
        {
            "help_string": "maps some src1 to dst1",
            "argstr": "{in_lta1}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "in_lta2",
        ty.Any,
        {
            "help_string": "maps dst1(src2) to dst2",
            "argstr": "{in_lta2}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "the combined LTA maps: src1 to dst2 = LTA2*LTA1",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": "{in_lta1}_concat",
        },
    ),
    (
        "invert_1",
        bool,
        {"help_string": "invert in_lta1 before applying it", "argstr": "-invert1"},
    ),
    (
        "invert_2",
        bool,
        {"help_string": "invert in_lta2 before applying it", "argstr": "-invert2"},
    ),
    ("invert_out", bool, {"help_string": "invert output LTA", "argstr": "-invertout"}),
    (
        "out_type",
        ty.Any,
        {"help_string": "set final LTA type", "argstr": "-out_type {out_type}"},
    ),
    (
        "tal_source_file",
        File,
        {
            "help_string": "if in_lta2 is talairach.xfm, specify source for talairach",
            "argstr": "-tal {tal_source_file}",
            "position": -5,
            "requires": ["tal_template_file"],
        },
    ),
    (
        "tal_template_file",
        File,
        {
            "help_string": "if in_lta2 is talairach.xfm, specify template for talairach",
            "argstr": "{tal_template_file}",
            "position": -4,
            "requires": ["tal_source_file"],
        },
    ),
    (
        "subject",
        str,
        {"help_string": "set subject in output LTA", "argstr": "-subject {subject}"},
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
ConcatenateLTA_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ConcatenateLTA_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ConcatenateLTA(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Lta
    >>> from pydra.tasks.freesurfer.auto.preprocess.concatenate_lta import ConcatenateLTA

    >>> task = ConcatenateLTA()
    >>> task.inputs.in_lta1 = Lta.mock("lta1.lta")
    >>> task.inputs.in_lta2 = "lta2.lta"
    >>> task.inputs.tal_source_file = File.mock()
    >>> task.inputs.tal_template_file = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_concatenate_lta lta1.lta lta2.lta lta1_concat.lta'


    >>> task = ConcatenateLTA()
    >>> task.inputs.in_lta1 = Lta.mock()
    >>> task.inputs.in_lta2 = "identity.nofile"
    >>> task.inputs.out_file = "inv1.lta"
    >>> task.inputs.invert_1 = True
    >>> task.inputs.tal_source_file = File.mock()
    >>> task.inputs.tal_template_file = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_concatenate_lta -invert1 lta1.lta identity.nofile inv1.lta'


    >>> task = ConcatenateLTA()
    >>> task.inputs.in_lta1 = Lta.mock()
    >>> task.inputs.out_type = "RAS2RAS"
    >>> task.inputs.tal_source_file = File.mock()
    >>> task.inputs.tal_template_file = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_concatenate_lta -invert1 -out_type 1 lta1.lta identity.nofile inv1.lta'


    """

    input_spec = ConcatenateLTA_input_spec
    output_spec = ConcatenateLTA_output_spec
    executable = "mri_concatenate_lta"
