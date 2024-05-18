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
            "help_string": "Input aparc+aseg.mgz",
            "argstr": "--i {in_file}",
            "mandatory": True,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Output aseg file",
            "argstr": "--o {out_file}",
            "mandatory": True,
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
Apas2Aseg_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", MghGz, {"help_string": "Output aseg file"})]
Apas2Aseg_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Apas2Aseg(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage import MghGz
    >>> from pydra.tasks.freesurfer.auto.utils.apas_2_aseg import Apas2Aseg

    >>> task = Apas2Aseg()
    >>> task.inputs.in_file = MghGz.mock("aseg.mgz")
    >>> task.inputs.out_file = "output.mgz"
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'apas2aseg --i aseg.mgz --o output.mgz'


    """

    input_spec = Apas2Aseg_input_spec
    output_spec = Apas2Aseg_output_spec
    executable = "apas2aseg"
