from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "source_file",
        Nifti1,
        {
            "help_string": "volume to be registered",
            "argstr": "--mov {source_file}",
            "mandatory": True,
        },
    ),
    (
        "target_file",
        Nifti1,
        {
            "help_string": "target volume for the registration",
            "argstr": "--dst {target_file}",
            "mandatory": True,
        },
    ),
    (
        "out_reg_file",
        ty.Any,
        True,
        {
            "help_string": "registration file; either True or filename",
            "argstr": "--lta {out_reg_file}",
        },
    ),
    (
        "registered_file",
        ty.Any,
        {
            "help_string": "registered image; either True or filename",
            "argstr": "--warp {registered_file}",
        },
    ),
    (
        "weights_file",
        ty.Any,
        {
            "help_string": "weights image to write; either True or filename",
            "argstr": "--weights {weights_file}",
        },
    ),
    (
        "est_int_scale",
        bool,
        {
            "help_string": "estimate intensity scale (recommended for unnormalized images)",
            "argstr": "--iscale",
        },
    ),
    (
        "trans_only",
        bool,
        {"help_string": "find 3 parameter translation only", "argstr": "--transonly"},
    ),
    (
        "in_xfm_file",
        File,
        {"help_string": "use initial transform on source", "argstr": "--transform"},
    ),
    (
        "half_source",
        ty.Any,
        {
            "help_string": "write source volume mapped to halfway space",
            "argstr": "--halfmov {half_source}",
        },
    ),
    (
        "half_targ",
        ty.Any,
        {
            "help_string": "write target volume mapped to halfway space",
            "argstr": "--halfdst {half_targ}",
        },
    ),
    (
        "half_weights",
        ty.Any,
        {
            "help_string": "write weights volume mapped to halfway space",
            "argstr": "--halfweights {half_weights}",
        },
    ),
    (
        "half_source_xfm",
        ty.Any,
        {
            "help_string": "write transform from source to halfway space",
            "argstr": "--halfmovlta {half_source_xfm}",
        },
    ),
    (
        "half_targ_xfm",
        ty.Any,
        {
            "help_string": "write transform from target to halfway space",
            "argstr": "--halfdstlta {half_targ_xfm}",
        },
    ),
    (
        "auto_sens",
        bool,
        {
            "help_string": "auto-detect good sensitivity",
            "argstr": "--satit",
            "mandatory": True,
            "xor": ["outlier_sens"],
        },
    ),
    (
        "outlier_sens",
        float,
        {
            "help_string": "set outlier sensitivity explicitly",
            "argstr": "--sat {outlier_sens:.4}",
            "mandatory": True,
            "xor": ["auto_sens"],
        },
    ),
    (
        "least_squares",
        bool,
        {
            "help_string": "use least squares instead of robust estimator",
            "argstr": "--leastsquares",
        },
    ),
    ("no_init", bool, {"help_string": "skip transform init", "argstr": "--noinit"}),
    (
        "init_orient",
        bool,
        {
            "help_string": "use moments for initial orient (recommended for stripped brains)",
            "argstr": "--initorient",
        },
    ),
    (
        "max_iterations",
        int,
        {
            "help_string": "maximum # of times on each resolution",
            "argstr": "--maxit {max_iterations}",
        },
    ),
    (
        "high_iterations",
        int,
        {
            "help_string": "max # of times on highest resolution",
            "argstr": "--highit {high_iterations}",
        },
    ),
    (
        "iteration_thresh",
        float,
        {
            "help_string": "stop iterations when below threshold",
            "argstr": "--epsit {iteration_thresh:.3}",
        },
    ),
    (
        "subsample_thresh",
        int,
        {
            "help_string": "subsample if dimension is above threshold size",
            "argstr": "--subsample {subsample_thresh}",
        },
    ),
    (
        "outlier_limit",
        float,
        {
            "help_string": "set maximal outlier limit in satit",
            "argstr": "--wlimit {outlier_limit:.3}",
        },
    ),
    (
        "write_vo2vox",
        bool,
        {
            "help_string": "output vox2vox matrix (default is RAS2RAS)",
            "argstr": "--vox2vox",
        },
    ),
    (
        "no_multi",
        bool,
        {"help_string": "work on highest resolution", "argstr": "--nomulti"},
    ),
    (
        "mask_source",
        File,
        {
            "help_string": "image to mask source volume with",
            "argstr": "--maskmov {mask_source}",
        },
    ),
    (
        "mask_target",
        File,
        {
            "help_string": "image to mask target volume with",
            "argstr": "--maskdst {mask_target}",
        },
    ),
    (
        "force_double",
        bool,
        {"help_string": "use double-precision intensities", "argstr": "--doubleprec"},
    ),
    (
        "force_float",
        bool,
        {"help_string": "use float intensities", "argstr": "--floattype"},
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
RobustRegister_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_reg_file", File, {"help_string": "output registration file"}),
    (
        "registered_file",
        File,
        {"help_string": "output image with registration applied"},
    ),
    ("weights_file", File, {"help_string": "image of weights used"}),
    ("half_source", File, {"help_string": "source image mapped to halfway space"}),
    ("half_targ", File, {"help_string": "target image mapped to halfway space"}),
    ("half_weights", File, {"help_string": "weights image mapped to halfway space"}),
    (
        "half_source_xfm",
        File,
        {"help_string": "transform file to map source image to halfway space"},
    ),
    (
        "half_targ_xfm",
        File,
        {"help_string": "transform file to map target image to halfway space"},
    ),
]
RobustRegister_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class RobustRegister(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.freesurfer.auto.preprocess.robust_register import RobustRegister

    >>> task = RobustRegister()
    >>> task.inputs.source_file = Nifti1.mock("structural.nii")
    >>> task.inputs.target_file = Nifti1.mock("T1.nii")
    >>> task.inputs.in_xfm_file = File.mock()
    >>> task.inputs.auto_sens = True
    >>> task.inputs.init_orient = True
    >>> task.inputs.mask_source = File.mock()
    >>> task.inputs.mask_target = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_robust_register --satit --initorient --lta .../structural_robustreg.lta --mov structural.nii --dst T1.nii'


    """

    input_spec = RobustRegister_input_spec
    output_spec = RobustRegister_output_spec
    executable = "mri_robust_register"
