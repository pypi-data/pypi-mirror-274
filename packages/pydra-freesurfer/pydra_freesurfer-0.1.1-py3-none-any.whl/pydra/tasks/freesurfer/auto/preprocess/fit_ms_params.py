from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_files",
        ty.List[MghGz],
        {
            "help_string": "list of FLASH images (must be in mgh format)",
            "argstr": "{in_files}",
            "mandatory": True,
            "position": -2,
        },
    ),
    ("tr_list", list, {"help_string": "list of TRs of the input files (in msec)"}),
    ("te_list", list, {"help_string": "list of TEs of the input files (in msec)"}),
    ("flip_list", list, {"help_string": "list of flip angles of the input files"}),
    (
        "xfm_list",
        ty.List[File],
        {"help_string": "list of transform files to apply to each FLASH image"},
    ),
    (
        "out_dir",
        Path,
        {
            "help_string": "directory to store output in",
            "argstr": "{out_dir}",
            "position": -1,
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
FitMSParams_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("t1_image", File, {"help_string": "image of estimated T1 relaxation values"}),
    ("pd_image", File, {"help_string": "image of estimated proton density values"}),
    ("t2star_image", File, {"help_string": "image of estimated T2* values"}),
]
FitMSParams_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FitMSParams(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pydra.tasks.freesurfer.auto.preprocess.fit_ms_params import FitMSParams

    >>> task = FitMSParams()
    >>> task.inputs.in_files = [MghGz.mock("flash_05.mgz"), MghGz.mock("flash_30.mgz")]
    >>> task.inputs.out_dir = "flash_parameters"
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_ms_fitparms flash_05.mgz flash_30.mgz flash_parameters'


    """

    input_spec = FitMSParams_input_spec
    output_spec = FitMSParams_output_spec
    executable = "mri_ms_fitparms"
