from fileformats.datascience import TextMatrix
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        MghGz,
        {"help_string": "input volume", "argstr": "--i {in_file}", "mandatory": True},
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output xfm file",
            "argstr": "--xfm {out_file}",
            "mandatory": True,
        },
    ),
    (
        "atlas",
        ty.Any,
        {
            "help_string": "alternate target atlas (in freesurfer/average dir)",
            "argstr": "--atlas {atlas}",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
TalairachAVI_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_file", TextMatrix, {"help_string": "The output transform for TalairachAVI"}),
    ("out_log", File, {"help_string": "The output log file for TalairachAVI"}),
    ("out_txt", File, {"help_string": "The output text file for TaliarachAVI"}),
]
TalairachAVI_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class TalairachAVI(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pydra.tasks.freesurfer.auto.utils.talairach_avi import TalairachAVI

    >>> task = TalairachAVI()
    >>> task.inputs.in_file = MghGz.mock("norm.mgz")
    >>> task.inputs.out_file = "trans.mat"
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'talairach_avi --i norm.mgz --xfm trans.mat'


    """

    input_spec = TalairachAVI_input_spec
    output_spec = TalairachAVI_output_spec
    executable = "talairach_avi"
