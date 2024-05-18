from fileformats.generic import Directory
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_surf",
        Pial,
        {
            "help_string": "Surface to register, often {hemi}.sphere",
            "argstr": "{in_surf}",
            "copyfile": True,
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "target",
        MghGz,
        {
            "help_string": "The data to register to. In normal recon-all usage, this is a template file for average surface.",
            "argstr": "{target}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "in_sulc",
        Pial,
        {
            "help_string": "Undocumented mandatory input file ${SUBJECTS_DIR}/surf/{hemisphere}.sulc ",
            "copyfile": True,
            "mandatory": True,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Output surface file to capture registration",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": '"lh.pial.reg"',
        },
    ),
    (
        "curv",
        bool,
        {
            "help_string": "Use smoothwm curvature for final alignment",
            "argstr": "-curv",
            "requires": ["in_smoothwm"],
        },
    ),
    (
        "in_smoothwm",
        Pial,
        {
            "help_string": "Undocumented input file ${SUBJECTS_DIR}/surf/{hemisphere}.smoothwm ",
            "copyfile": True,
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
Register_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Register_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Register(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.registration.register import Register

    >>> task = Register()
    >>> task.inputs.in_surf = Pial.mock("lh.pial")
    >>> task.inputs.target = MghGz.mock("aseg.mgz")
    >>> task.inputs.in_sulc = Pial.mock("lh.pial")
    >>> task.inputs.out_file = "lh.pial.reg"
    >>> task.inputs.curv = True
    >>> task.inputs.in_smoothwm = Pial.mock("lh.pial")
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_register -curv lh.pial aseg.mgz lh.pial.reg'


    """

    input_spec = Register_input_spec
    output_spec = Register_output_spec
    executable = "mris_register"
