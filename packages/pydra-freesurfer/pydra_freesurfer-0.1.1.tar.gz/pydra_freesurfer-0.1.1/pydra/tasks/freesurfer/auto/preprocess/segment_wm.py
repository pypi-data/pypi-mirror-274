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
            "help_string": "Input file for SegmentWM",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "File to be written as output for SegmentWM",
            "argstr": "{out_file}",
            "mandatory": True,
            "position": -1,
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
SegmentWM_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_file", MghGz, {"help_string": "Output white matter segmentation"})
]
SegmentWM_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SegmentWM(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage import MghGz
    >>> from pydra.tasks.freesurfer.auto.preprocess.segment_wm import SegmentWM

    >>> task = SegmentWM()
    >>> task.inputs.in_file = MghGz.mock("norm.mgz")
    >>> task.inputs.out_file = "wm.seg.mgz"
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_segment norm.mgz wm.seg.mgz'


    """

    input_spec = SegmentWM_input_spec
    output_spec = SegmentWM_output_spec
    executable = "mri_segment"
