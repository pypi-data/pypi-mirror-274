from fileformats.generic import Directory
from fileformats.text import TextFile
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "log_file",
        Path,
        {
            "help_string": "The log file for TalairachQC",
            "argstr": "{log_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
TalairachQC_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("log_file", TextFile, {"help_string": "The output log"})]
TalairachQC_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class TalairachQC(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.freesurfer.auto.utils.talairach_qc import TalairachQC

    >>> task = TalairachQC()
    >>> task.inputs.log_file = "dirs.txt"
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'tal_QC_AZS dirs.txt'


    """

    input_spec = TalairachQC_input_spec
    output_spec = TalairachQC_output_spec
    executable = "tal_QC_AZS"
