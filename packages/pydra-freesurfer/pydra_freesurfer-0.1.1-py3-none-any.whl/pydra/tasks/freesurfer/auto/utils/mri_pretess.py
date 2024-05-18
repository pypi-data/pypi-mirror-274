from fileformats.generic import Directory
from fileformats.medimage import MghGz
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_filled",
        MghGz,
        {
            "help_string": "filled volume, usually wm.mgz",
            "argstr": "{in_filled}",
            "mandatory": True,
            "position": -4,
        },
    ),
    (
        "label",
        ty.Any,
        {
            "help_string": "label to be picked up, can be a Freesurfer's string like 'wm' or a label value (e.g. 127 for rh or 255 for lh)",
            "argstr": "{label}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "in_norm",
        MghGz,
        {
            "help_string": "the normalized, brain-extracted T1w image. Usually norm.mgz",
            "argstr": "{in_norm}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "the output file after mri_pretess.",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": "{in_filled}_pretesswm",
        },
    ),
    (
        "nocorners",
        bool,
        {
            "help_string": "do not remove corner configurations in addition to edge ones.",
            "argstr": "-nocorners",
        },
    ),
    ("keep", bool, {"help_string": "keep WM edits", "argstr": "-keep"}),
    (
        "test",
        bool,
        {
            "help_string": "adds a voxel that should be removed by mri_pretess. The value of the voxel is set to that of an ON-edited WM, so it should be kept with -keep. The output will NOT be saved.",
            "argstr": "-test",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
MRIPretess_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
MRIPretess_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MRIPretess(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage import MghGz
    >>> from pydra.tasks.freesurfer.auto.utils.mri_pretess import MRIPretess

    >>> task = MRIPretess()
    >>> task.inputs.in_filled = MghGz.mock("wm.mgz")
    >>> task.inputs.in_norm = MghGz.mock("norm.mgz")
    >>> task.inputs.nocorners = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_pretess -nocorners wm.mgz wm norm.mgz wm_pretesswm.mgz'


    """

    input_spec = MRIPretess_input_spec
    output_spec = MRIPretess_output_spec
    executable = "mri_pretess"
