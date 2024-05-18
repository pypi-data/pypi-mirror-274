from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Annot, Label, Thickness, White
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "subject_id",
        ty.Any,
        {
            "help_string": "Subject being processed",
            "argstr": "--s {subject_id}",
            "mandatory": True,
        },
    ),
    (
        "hemisphere",
        ty.Any,
        {
            "help_string": "Hemisphere being processed",
            "argstr": "--{hemisphere}-only",
            "mandatory": True,
        },
    ),
    (
        "thickness",
        Thickness,
        {
            "help_string": "Input file must be <subject_id>/surf/?h.thickness",
            "mandatory": True,
        },
    ),
    (
        "white",
        White,
        {
            "help_string": "Input file must be <subject_id>/surf/<hemisphere>.white",
            "mandatory": True,
        },
    ),
    (
        "annotation",
        Annot,
        {
            "help_string": "Input annotation file must be <subject_id>/label/<hemisphere>.aparc.annot",
            "mandatory": True,
        },
    ),
    (
        "cortex",
        Label,
        {
            "help_string": "Input cortex label must be <subject_id>/label/<hemisphere>.cortex.label",
            "mandatory": True,
        },
    ),
    (
        "orig",
        MghGz,
        {"help_string": "Implicit input file mri/orig.mgz", "mandatory": True},
    ),
    (
        "rawavg",
        MghGz,
        {"help_string": "Implicit input file mri/rawavg.mgz", "mandatory": True},
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
Contrast_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_contrast", File, {"help_string": "Output contrast file from Contrast"}),
    ("out_stats", File, {"help_string": "Output stats file from Contrast"}),
    ("out_log", File, {"help_string": "Output log from Contrast"}),
]
Contrast_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Contrast(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.medimage_freesurfer import Annot, Label, Thickness, White
    >>> from pydra.tasks.freesurfer.auto.utils.contrast import Contrast

    >>> task = Contrast()
    >>> task.inputs.subject_id = "10335"
    >>> task.inputs.hemisphere = "lh"
    >>> task.inputs.thickness = Thickness.mock("lh.thickness" # doctest: +SKIP)
    >>> task.inputs.white = White.mock("lh.white" # doctest: +SKIP)
    >>> task.inputs.annotation = Annot.mock("../label/lh.aparc.annot" # doctest: +SKIP)
    >>> task.inputs.cortex = Label.mock("../label/lh.cortex.label" # doctest: +SKIP)
    >>> task.inputs.orig = MghGz.mock("../mri/orig.mgz" # doctest: +SKIP)
    >>> task.inputs.rawavg = MghGz.mock("../mri/rawavg.mgz" # doctest: +SKIP)
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'pctsurfcon --lh-only --s 10335'


    """

    input_spec = Contrast_input_spec
    output_spec = Contrast_output_spec
    executable = "pctsurfcon"
