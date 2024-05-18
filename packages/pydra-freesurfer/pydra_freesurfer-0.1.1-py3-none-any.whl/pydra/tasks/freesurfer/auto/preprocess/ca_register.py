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
        {
            "help_string": "The input volume for CARegister",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "The output volume for CARegister",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": '"talairach.m3z"',
        },
    ),
    (
        "template",
        File,
        {
            "help_string": "The template file in gca format",
            "argstr": "{template}",
            "position": -2,
        },
    ),
    (
        "mask",
        File,
        {"help_string": "Specifies volume to use as mask", "argstr": "-mask {mask}"},
    ),
    (
        "invert_and_save",
        bool,
        {
            "help_string": "Invert and save the .m3z multi-dimensional talaraich transform to x, y, and z .mgz files",
            "argstr": "-invert-and-save",
            "position": -4,
        },
    ),
    (
        "no_big_ventricles",
        bool,
        {"help_string": "No big ventricles", "argstr": "-nobigventricles"},
    ),
    (
        "transform",
        File,
        {
            "help_string": "Specifies transform in lta format",
            "argstr": "-T {transform}",
        },
    ),
    (
        "align",
        ty.Any,
        {
            "help_string": "Specifies when to perform alignment",
            "argstr": "-align-{align}",
        },
    ),
    (
        "levels",
        int,
        {
            "help_string": "defines how many surrounding voxels will be used in interpolations, default is 6",
            "argstr": "-levels {levels}",
        },
    ),
    (
        "A",
        int,
        {
            "help_string": "undocumented flag used in longitudinal processing",
            "argstr": "-A {A}",
        },
    ),
    (
        "l_files",
        ty.List[File],
        {
            "help_string": "undocumented flag used in longitudinal processing",
            "argstr": "-l {l_files}",
        },
    ),
    ("num_threads", int, {"help_string": "allows for specifying more threads"}),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
CARegister_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
CARegister_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class CARegister(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pydra.tasks.freesurfer.auto.preprocess.ca_register import CARegister

    >>> task = CARegister()
    >>> task.inputs.in_file = MghGz.mock("norm.mgz")
    >>> task.inputs.out_file = "talairach.m3z"
    >>> task.inputs.template = File.mock()
    >>> task.inputs.mask = File.mock()
    >>> task.inputs.transform = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_ca_register norm.mgz talairach.m3z'


    """

    input_spec = CARegister_input_spec
    output_spec = CARegister_output_spec
    executable = "mri_ca_register"
