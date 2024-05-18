from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Pial
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "surface",
        Pial,
        {
            "help_string": "Specify surface file for CurvatureStats",
            "argstr": "-F {surface}",
        },
    ),
    (
        "curvfile1",
        Pial,
        {
            "help_string": "Input file for CurvatureStats",
            "argstr": "{curvfile1}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "curvfile2",
        Pial,
        {
            "help_string": "Input file for CurvatureStats",
            "argstr": "{curvfile2}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "hemisphere",
        ty.Any,
        {
            "help_string": "Hemisphere being processed",
            "argstr": "{hemisphere}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "subject_id",
        ty.Any,
        {
            "help_string": "Subject being processed",
            "argstr": "{subject_id}",
            "mandatory": True,
            "position": -4,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Output curvature stats file",
            "argstr": "-o {out_file}",
            "output_file_template": "{hemisphere}.curv.stats",
        },
    ),
    (
        "min_max",
        bool,
        {
            "help_string": "Output min / max information for the processed curvature.",
            "argstr": "-m",
        },
    ),
    (
        "values",
        bool,
        {
            "help_string": "Triggers a series of derived curvature values",
            "argstr": "-G",
        },
    ),
    (
        "write",
        bool,
        {"help_string": "Write curvature files", "argstr": "--writeCurvatureFiles"},
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
CurvatureStats_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
CurvatureStats_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class CurvatureStats(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.utils.curvature_stats import CurvatureStats

    >>> task = CurvatureStats()
    >>> task.inputs.surface = Pial.mock("lh.pial")
    >>> task.inputs.curvfile1 = Pial.mock("lh.pial")
    >>> task.inputs.curvfile2 = Pial.mock("lh.pial")
    >>> task.inputs.hemisphere = "lh"
    >>> task.inputs.out_file = "lh.curv.stats"
    >>> task.inputs.min_max = True
    >>> task.inputs.values = True
    >>> task.inputs.write = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_curvature_stats -m -o lh.curv.stats -F pial -G --writeCurvatureFiles subject_id lh pial pial'


    """

    input_spec = CurvatureStats_input_spec
    output_spec = CurvatureStats_output_spec
    executable = "mris_curvature_stats"
