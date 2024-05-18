from fileformats.generic import Directory, File
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
            "help_string": "in brain volume",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "template",
        MghGz,
        {
            "help_string": "template gca",
            "argstr": "{template}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output transform",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": "{in_file}_transform.lta",
        },
    ),
    (
        "skull",
        bool,
        {"help_string": "align to atlas containing skull (uns=5)", "argstr": "-skull"},
    ),
    ("mask", File, {"help_string": "use volume as a mask", "argstr": "-mask {mask}"}),
    (
        "nbrspacing",
        int,
        {
            "help_string": "align to atlas containing skull setting unknown_nbr_spacing = nbrspacing",
            "argstr": "-uns {nbrspacing}",
        },
    ),
    (
        "transform",
        File,
        {"help_string": "Previously computed transform", "argstr": "-t {transform}"},
    ),
    ("num_threads", int, {"help_string": "allows for specifying more threads"}),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
EMRegister_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
EMRegister_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class EMRegister(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pydra.tasks.freesurfer.auto.registration.em_register import EMRegister

    >>> task = EMRegister()
    >>> task.inputs.in_file = MghGz.mock("norm.mgz")
    >>> task.inputs.template = MghGz.mock("aseg.mgz")
    >>> task.inputs.out_file = "norm_transform.lta"
    >>> task.inputs.skull = True
    >>> task.inputs.mask = File.mock()
    >>> task.inputs.nbrspacing = 9
    >>> task.inputs.transform = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_em_register -uns 9 -skull norm.mgz aseg.mgz norm_transform.lta'


    """

    input_spec = EMRegister_input_spec
    output_spec = EMRegister_output_spec
    executable = "mri_em_register"
