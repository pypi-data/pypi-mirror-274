from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
from fileformats.medimage_freesurfer import Lta
from fileformats.text import TextFile
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_files",
        ty.List[Nifti1],
        {
            "help_string": "input movable volumes to be aligned to common mean/median template",
            "argstr": "--mov {in_files}",
            "mandatory": True,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output template volume (final mean/median image)",
            "argstr": "--template {out_file}",
            "mandatory": True,
        },
    ),
    (
        "auto_detect_sensitivity",
        bool,
        {
            "help_string": "auto-detect good sensitivity (recommended for head or full brain scans)",
            "argstr": "--satit",
            "mandatory": True,
            "xor": ["outlier_sensitivity"],
        },
    ),
    (
        "outlier_sensitivity",
        float,
        {
            "help_string": 'set outlier sensitivity manually (e.g. "--sat 4.685" ). Higher values mean less sensitivity.',
            "argstr": "--sat {outlier_sensitivity:.4}",
            "mandatory": True,
            "xor": ["auto_detect_sensitivity"],
        },
    ),
    (
        "transform_outputs",
        ty.Any,
        {
            "help_string": "output xforms to template (for each input)",
            "argstr": "--lta {transform_outputs}",
        },
    ),
    (
        "intensity_scaling",
        bool,
        {
            "help_string": "allow also intensity scaling (default off)",
            "argstr": "--iscale",
        },
    ),
    (
        "scaled_intensity_outputs",
        ty.Any,
        {
            "help_string": "final intensity scales (will activate --iscale)",
            "argstr": "--iscaleout {scaled_intensity_outputs}",
        },
    ),
    (
        "subsample_threshold",
        int,
        {
            "help_string": "subsample if dim > # on all axes (default no subs.)",
            "argstr": "--subsample {subsample_threshold}",
        },
    ),
    (
        "average_metric",
        ty.Any,
        {
            "help_string": "construct template from: 0 Mean, 1 Median (default)",
            "argstr": "--average {average_metric}",
        },
    ),
    (
        "initial_timepoint",
        int,
        {
            "help_string": "use TP# for spacial init (default random), 0: no init",
            "argstr": "--inittp {initial_timepoint}",
        },
    ),
    (
        "fixed_timepoint",
        bool,
        {
            "help_string": "map everything to init TP# (init TP is not resampled)",
            "argstr": "--fixtp",
        },
    ),
    (
        "no_iteration",
        bool,
        {
            "help_string": "do not iterate, just create first template",
            "argstr": "--noit",
        },
    ),
    (
        "initial_transforms",
        ty.List[File],
        {
            "help_string": "use initial transforms (lta) on source",
            "argstr": "--ixforms {initial_transforms}",
        },
    ),
    (
        "in_intensity_scales",
        ty.List[File],
        {
            "help_string": "use initial intensity scales",
            "argstr": "--iscalein {in_intensity_scales}",
        },
    ),
    ("num_threads", int, {"help_string": "allows for specifying more threads"}),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
RobustTemplate_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_file",
        Nifti1,
        {"help_string": "output template volume (final mean/median image)"},
    ),
    (
        "transform_outputs",
        ty.List[ty.Union[File, Lta]],
        {"help_string": "output xform files from moving to template"},
    ),
    (
        "scaled_intensity_outputs",
        ty.List[TextFile],
        {"help_string": "output final intensity scales"},
    ),
]
RobustTemplate_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class RobustTemplate(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from fileformats.medimage_freesurfer import Lta
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.freesurfer.auto.longitudinal.robust_template import RobustTemplate

    >>> task = RobustTemplate()
    >>> task.inputs.in_files = [Nifti1.mock("structural.nii"), Nifti1.mock("functional.nii")]
    >>> task.inputs.out_file = "T1.nii"
    >>> task.inputs.auto_detect_sensitivity = True
    >>> task.inputs.subsample_threshold = 200
    >>> task.inputs.average_metric = "mean"
    >>> task.inputs.initial_timepoint = 1
    >>> task.inputs.fixed_timepoint = True
    >>> task.inputs.no_iteration = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    >>> task = RobustTemplate()
    >>> task.inputs.transform_outputs = ["structural.lta","functional.lta"]
    >>> task.inputs.scaled_intensity_outputs = ["structural-iscale.txt","functional-iscale.txt"]
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    >>> task = RobustTemplate()
    >>> task.inputs.transform_outputs = True
    >>> task.inputs.scaled_intensity_outputs = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    input_spec = RobustTemplate_input_spec
    output_spec = RobustTemplate_output_spec
    executable = "mri_robust_template"
