from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Lta
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        MghGz,
        {
            "help_string": "input volume",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output volume",
            "argstr": "{out_file}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "t1",
        bool,
        {
            "help_string": "specify T1 input volume (T1 grey value = 110)",
            "argstr": "-T1",
        },
    ),
    (
        "brain_atlas",
        File,
        {"help_string": "", "argstr": "-brain_atlas {brain_atlas}", "position": -4},
    ),
    (
        "transform",
        Lta,
        {"help_string": "undocumented", "argstr": "{transform}", "position": -3},
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
WatershedSkullStrip_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", MghGz, {"help_string": "skull stripped brain volume"})]
WatershedSkullStrip_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class WatershedSkullStrip(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.medimage_freesurfer import Lta
    >>> from pydra.tasks.freesurfer.auto.preprocess.watershed_skull_strip import WatershedSkullStrip

    >>> task = WatershedSkullStrip()
    >>> task.inputs.in_file = MghGz.mock("T1.mgz")
    >>> task.inputs.out_file = "brainmask.auto.mgz"
    >>> task.inputs.t1 = True
    >>> task.inputs.brain_atlas = File.mock()
    >>> task.inputs.transform = Lta.mock("transforms/talairach_with_skull.lta")
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_watershed -T1 transforms/talairach_with_skull.lta T1.mgz brainmask.auto.mgz'


    """

    input_spec = WatershedSkullStrip_input_spec
    output_spec = WatershedSkullStrip_output_spec
    executable = "mri_watershed"
