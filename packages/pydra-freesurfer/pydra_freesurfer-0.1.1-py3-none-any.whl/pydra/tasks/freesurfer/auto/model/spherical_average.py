from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "out_file",
        Path,
        {
            "help_string": "Output filename",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": '"test.out"',
        },
    ),
    (
        "in_average",
        Path,
        {"help_string": "Average subject", "argstr": "{in_average}", "position": -2},
    ),
    (
        "in_surf",
        Pial,
        {
            "help_string": "Input surface file",
            "argstr": "{in_surf}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "hemisphere",
        ty.Any,
        {
            "help_string": "Input hemisphere",
            "argstr": "{hemisphere}",
            "mandatory": True,
            "position": -4,
        },
    ),
    (
        "fname",
        ty.Any,
        {
            "help_string": "Filename from the average subject directory.\nExample: to use rh.entorhinal.label as the input label filename, set fname to 'rh.entorhinal'\nand which to 'label'. The program will then search for\n``<in_average>/label/rh.entorhinal.label``",
            "argstr": "{fname}",
            "mandatory": True,
            "position": -5,
        },
    ),
    (
        "which",
        ty.Any,
        {
            "help_string": "No documentation",
            "argstr": "{which}",
            "mandatory": True,
            "position": -6,
        },
    ),
    (
        "subject_id",
        ty.Any,
        {
            "help_string": "Output subject id",
            "argstr": "-o {subject_id}",
            "mandatory": True,
        },
    ),
    ("erode", int, {"help_string": "Undocumented", "argstr": "-erode {erode}"}),
    (
        "in_orig",
        File,
        {"help_string": "Original surface filename", "argstr": "-orig {in_orig}"},
    ),
    (
        "threshold",
        float,
        {"help_string": "Undocumented", "argstr": "-t {threshold:.1}"},
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
SphericalAverage_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
SphericalAverage_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SphericalAverage(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.model.spherical_average import SphericalAverage

    >>> task = SphericalAverage()
    >>> task.inputs.out_file = "test.out"
    >>> task.inputs.in_average = "."
    >>> task.inputs.in_surf = Pial.mock("lh.pial")
    >>> task.inputs.hemisphere = "lh"
    >>> task.inputs.fname = "lh.entorhinal"
    >>> task.inputs.which = "label"
    >>> task.inputs.subject_id = "10335"
    >>> task.inputs.erode = 2
    >>> task.inputs.in_orig = File.mock()
    >>> task.inputs.threshold = 5
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_spherical_average -erode 2 -o 10335 -t 5.0 label lh.entorhinal lh pial . test.out'


    """

    input_spec = SphericalAverage_input_spec
    output_spec = SphericalAverage_output_spec
    executable = "mris_spherical_average"
