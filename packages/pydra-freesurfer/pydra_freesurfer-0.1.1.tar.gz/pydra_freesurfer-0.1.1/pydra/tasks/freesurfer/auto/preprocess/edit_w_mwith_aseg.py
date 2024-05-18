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
            "help_string": "Input white matter segmentation file",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -4,
        },
    ),
    (
        "brain_file",
        MghGz,
        {
            "help_string": "Input brain/T1 file",
            "argstr": "{brain_file}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "seg_file",
        MghGz,
        {
            "help_string": "Input presurf segmentation file",
            "argstr": "{seg_file}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "File to be written as output",
            "argstr": "{out_file}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "keep_in",
        bool,
        {"help_string": "Keep edits as found in input volume", "argstr": "-keep-in"},
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
EditWMwithAseg_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", MghGz, {"help_string": "Output edited WM file"})]
EditWMwithAseg_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class EditWMwithAseg(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage import MghGz
    >>> from pydra.tasks.freesurfer.auto.preprocess.edit_w_mwith_aseg import EditWMwithAseg

    >>> task = EditWMwithAseg()
    >>> task.inputs.in_file = MghGz.mock("T1.mgz")
    >>> task.inputs.brain_file = MghGz.mock("norm.mgz")
    >>> task.inputs.seg_file = MghGz.mock("aseg.mgz")
    >>> task.inputs.out_file = "wm.asegedit.mgz"
    >>> task.inputs.keep_in = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_edit_wm_with_aseg -keep-in T1.mgz norm.mgz aseg.mgz wm.asegedit.mgz'


    """

    input_spec = EditWMwithAseg_input_spec
    output_spec = EditWMwithAseg_output_spec
    executable = "mri_edit_wm_with_aseg"
