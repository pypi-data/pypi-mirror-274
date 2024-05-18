from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.text import TextFile
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        MghGz,
        {
            "help_string": "The input file",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "target",
        MghGz,
        {
            "help_string": "The target file",
            "argstr": "{target}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "vox2vox",
        TextFile,
        {
            "help_string": "The vox2vox file",
            "argstr": "{vox2vox}",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "out_file",
        Path,
        "talairach.auto.xfm",
        {"help_string": "The transform output", "argstr": "{out_file}", "position": 3},
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
RegisterAVItoTalairach_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_file", File, {"help_string": "The output file for RegisterAVItoTalairach"}),
    ("log_file", File, {"help_string": "The output log"}),
]
RegisterAVItoTalairach_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class RegisterAVItoTalairach(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.freesurfer.auto.registration.register_av_ito_talairach import RegisterAVItoTalairach

    >>> task = RegisterAVItoTalairach()
    >>> task.inputs.in_file = MghGz.mock("structural.mgz"                         # doctest: +SKIP)
    >>> task.inputs.target = MghGz.mock("mni305.cor.mgz"                          # doctest: +SKIP)
    >>> task.inputs.vox2vox = TextFile.mock("talsrcimg_to_structural_t4_vox2vox.txt" # doctest: +SKIP)
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'avi2talxfm structural.mgz mni305.cor.mgz talsrcimg_to_structural_t4_vox2vox.txt talairach.auto.xfm'


    """

    input_spec = RegisterAVItoTalairach_input_spec
    output_spec = RegisterAVItoTalairach_output_spec
    executable = "avi2talxfm"
