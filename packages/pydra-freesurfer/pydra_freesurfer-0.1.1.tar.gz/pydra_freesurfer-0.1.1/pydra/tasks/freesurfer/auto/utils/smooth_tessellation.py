from fileformats.generic import Directory, File
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        File,
        {
            "help_string": "Input volume to tessellate voxels from.",
            "argstr": "{in_file}",
            "copyfile": True,
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "curvature_averaging_iterations",
        int,
        {
            "help_string": "Number of curvature averaging iterations (default=10)",
            "argstr": "-a {curvature_averaging_iterations}",
        },
    ),
    (
        "smoothing_iterations",
        int,
        {
            "help_string": "Number of smoothing iterations (default=10)",
            "argstr": "-n {smoothing_iterations}",
        },
    ),
    (
        "snapshot_writing_iterations",
        int,
        {
            "help_string": "Write snapshot every *n* iterations",
            "argstr": "-w {snapshot_writing_iterations}",
        },
    ),
    (
        "use_gaussian_curvature_smoothing",
        bool,
        {"help_string": "Use Gaussian curvature smoothing", "argstr": "-g"},
    ),
    (
        "gaussian_curvature_norm_steps",
        int,
        {
            "help_string": "Use Gaussian curvature smoothing",
            "argstr": "{gaussian_curvature_norm_steps}",
        },
    ),
    (
        "gaussian_curvature_smoothing_steps",
        int,
        {
            "help_string": "Use Gaussian curvature smoothing",
            "argstr": " {gaussian_curvature_smoothing_steps}",
        },
    ),
    (
        "disable_estimates",
        bool,
        {
            "help_string": "Disables the writing of curvature and area estimates",
            "argstr": "-nw",
        },
    ),
    (
        "normalize_area",
        bool,
        {"help_string": "Normalizes the area after smoothing", "argstr": "-area"},
    ),
    ("use_momentum", bool, {"help_string": "Uses momentum", "argstr": "-m"}),
    (
        "out_file",
        Path,
        {
            "help_string": "output filename or True to generate one",
            "argstr": "{out_file}",
            "position": -1,
        },
    ),
    (
        "out_curvature_file",
        Path,
        {
            "help_string": 'Write curvature to ``?h.curvname`` (default "curv")',
            "argstr": "-c {out_curvature_file}",
        },
    ),
    (
        "out_area_file",
        Path,
        {
            "help_string": 'Write area to ``?h.areaname`` (default "area")',
            "argstr": "-b {out_area_file}",
        },
    ),
    (
        "seed",
        int,
        {
            "help_string": "Seed for setting random number generator",
            "argstr": "-seed {seed}",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
SmoothTessellation_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("surface", File, {"help_string": "Smoothed surface file."})]
SmoothTessellation_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SmoothTessellation(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.auto.utils.smooth_tessellation import SmoothTessellation

    """

    input_spec = SmoothTessellation_input_spec
    output_spec = SmoothTessellation_output_spec
    executable = "mris_smooth"
