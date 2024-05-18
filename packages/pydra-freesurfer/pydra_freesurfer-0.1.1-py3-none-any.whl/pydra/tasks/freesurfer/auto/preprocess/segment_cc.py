from fileformats.generic import Directory
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Lta
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
            "help_string": "Input aseg file to read from subjects directory",
            "argstr": "-aseg {in_file}",
            "mandatory": True,
        },
    ),
    (
        "in_norm",
        MghGz,
        {
            "help_string": "Required undocumented input {subject}/mri/norm.mgz",
            "mandatory": True,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Filename to write aseg including CC",
            "argstr": "-o {out_file}",
            "output_file_template": "{in_file}.auto.mgz",
        },
    ),
    (
        "out_rotation",
        Path,
        {
            "help_string": "Global filepath for writing rotation lta",
            "argstr": "-lta {out_rotation}",
            "mandatory": True,
        },
    ),
    (
        "subject_id",
        ty.Any,
        {
            "help_string": "Subject name",
            "argstr": "{subject_id}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "copy_inputs",
        bool,
        {
            "help_string": "If running as a node, set this to True.This will copy the input files to the node directory."
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
SegmentCC_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_rotation", Lta, {"help_string": "Output lta rotation file"})]
SegmentCC_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SegmentCC(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.medimage_freesurfer import Lta
    >>> from pydra.tasks.freesurfer.auto.preprocess.segment_cc import SegmentCC

    >>> task = SegmentCC()
    >>> task.inputs.in_file = MghGz.mock("aseg.mgz")
    >>> task.inputs.in_norm = MghGz.mock("norm.mgz")
    >>> task.inputs.out_rotation = "cc.lta"
    >>> task.inputs.subject_id = "test"
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_cc -aseg aseg.mgz -o aseg.auto.mgz -lta cc.lta test'


    """

    input_spec = SegmentCC_input_spec
    output_spec = SegmentCC_output_spec
    executable = "mri_cc"
