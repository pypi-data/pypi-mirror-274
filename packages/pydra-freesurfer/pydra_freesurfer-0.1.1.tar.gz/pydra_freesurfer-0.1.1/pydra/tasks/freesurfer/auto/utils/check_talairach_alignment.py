from fileformats.datascience import TextMatrix
from fileformats.generic import Directory, File
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        TextMatrix,
        {
            "help_string": "specify the talairach.xfm file to check",
            "argstr": "-xfm {in_file}",
            "mandatory": True,
            "position": -1,
            "xor": ["subject"],
        },
    ),
    (
        "subject",
        ty.Any,
        {
            "help_string": "specify subject's name",
            "argstr": "-subj {subject}",
            "mandatory": True,
            "position": -1,
            "xor": ["in_file"],
        },
    ),
    (
        "threshold",
        float,
        0.01,
        {
            "help_string": "Talairach transforms for subjects with p-values <= T are considered as very unlikely default=0.010",
            "argstr": "-T {threshold:.3}",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
CheckTalairachAlignment_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_file", File, {"help_string": "The input file for CheckTalairachAlignment"})
]
CheckTalairachAlignment_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class CheckTalairachAlignment(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.auto.utils.check_talairach_alignment import CheckTalairachAlignment

    >>> task = CheckTalairachAlignment()
    >>> task.inputs.in_file = TextMatrix.mock("trans.mat")
    >>> task.inputs.threshold = 0.005
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'talairach_afd -T 0.005 -xfm trans.mat'


    """

    input_spec = CheckTalairachAlignment_input_spec
    output_spec = CheckTalairachAlignment_output_spec
    executable = "talairach_afd"
