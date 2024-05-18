from fileformats.datascience import TextMatrix
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz, NiftiGz
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        MghGz,
        {
            "help_string": "The input file for CANormalize",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -4,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "The output file for CANormalize",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": "{in_file}_norm",
        },
    ),
    (
        "atlas",
        NiftiGz,
        {
            "help_string": "The atlas file in gca format",
            "argstr": "{atlas}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "transform",
        TextMatrix,
        {
            "help_string": "The transform file in lta format",
            "argstr": "{transform}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "mask",
        File,
        {"help_string": "Specifies volume to use as mask", "argstr": "-mask {mask}"},
    ),
    (
        "control_points",
        Path,
        {
            "help_string": "File name for the output control points",
            "argstr": "-c {control_points}",
        },
    ),
    (
        "long_file",
        File,
        {
            "help_string": "undocumented flag used in longitudinal processing",
            "argstr": "-long {long_file}",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
CANormalize_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("control_points", File, {"help_string": "The output control points for Normalize"})
]
CANormalize_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class CANormalize(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz, NiftiGz
    >>> from pydra.tasks.freesurfer.auto.preprocess.ca_normalize import CANormalize

    >>> task = CANormalize()
    >>> task.inputs.in_file = MghGz.mock("T1.mgz")
    >>> task.inputs.atlas = NiftiGz.mock("atlas.nii.gz" # in practice use .gca atlases)
    >>> task.inputs.transform = TextMatrix.mock("trans.mat" # in practice use .lta transforms)
    >>> task.inputs.mask = File.mock()
    >>> task.inputs.long_file = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_ca_normalize T1.mgz atlas.nii.gz trans.mat T1_norm.mgz'


    """

    input_spec = CANormalize_input_spec
    output_spec = CANormalize_output_spec
    executable = "mri_ca_normalize"
