from fileformats.generic import Directory
from fileformats.medimage import MghGz
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "fixed_weighting",
        bool,
        {
            "help_string": "use a fixed weighting to generate optimal gray/white contrast",
            "argstr": "-w",
            "position": 1,
        },
    ),
    (
        "tr",
        float,
        {
            "help_string": "repetition time (in msec)",
            "argstr": "{tr:.2}",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "flip_angle",
        float,
        {
            "help_string": "flip angle (in degrees)",
            "argstr": "{flip_angle:.2}",
            "mandatory": True,
            "position": 3,
        },
    ),
    (
        "te",
        float,
        {
            "help_string": "echo time (in msec)",
            "argstr": "{te:.3}",
            "mandatory": True,
            "position": 4,
        },
    ),
    (
        "t1_image",
        MghGz,
        {
            "help_string": "image of T1 values",
            "argstr": "{t1_image}",
            "mandatory": True,
            "position": 5,
        },
    ),
    (
        "pd_image",
        MghGz,
        {
            "help_string": "image of proton density values",
            "argstr": "{pd_image}",
            "mandatory": True,
            "position": 6,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "image to write",
            "argstr": "{out_file}",
            "output_file_template": '"flash_30syn.mgz"',
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
SynthesizeFLASH_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
SynthesizeFLASH_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SynthesizeFLASH(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage import MghGz
    >>> from pydra.tasks.freesurfer.auto.preprocess.synthesize_flash import SynthesizeFLASH

    >>> task = SynthesizeFLASH()
    >>> task.inputs.tr = 20
    >>> task.inputs.flip_angle = 30
    >>> task.inputs.te = 3
    >>> task.inputs.t1_image = MghGz.mock("T1.mgz")
    >>> task.inputs.pd_image = MghGz.mock("PD.mgz")
    >>> task.inputs.out_file = "flash_30syn.mgz"
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_synthesize 20.00 30.00 3.000 T1.mgz PD.mgz flash_30syn.mgz'


    """

    input_spec = SynthesizeFLASH_input_spec
    output_spec = SynthesizeFLASH_output_spec
    executable = "mri_synthesize"
