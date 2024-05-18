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
            "help_string": "source file to be registered",
            "argstr": "--mov {source_file}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "reference_file",
        Nifti1,
        {
            "help_string": "reference (target) file",
            "argstr": "--ref {reference_file}",
            "copyfile": False,
            "mandatory": True,
            "xor": ["subject_id"],
        },
    ),
    (
        "out_lta_file",
        ty.Any,
        True,
        {
            "help_string": "output registration file (LTA format)",
            "argstr": "--lta {out_lta_file}",
        },
    ),
    (
        "out_reg_file",
        ty.Any,
        {
            "help_string": "output registration file (REG format)",
            "argstr": "--regdat {out_reg_file}",
        },
    ),
    (
        "out_params_file",
        ty.Any,
        {
            "help_string": "output parameters file",
            "argstr": "--params {out_params_file}",
        },
    ),
    (
        "subjects_dir",
        Directory,
        {"help_string": "FreeSurfer SUBJECTS_DIR", "argstr": "--sd {subjects_dir}"},
    ),
    (
        "subject_id",
        str,
        {
            "help_string": "freesurfer subject ID (implies ``reference_mask == aparc+aseg.mgz`` unless otherwise specified)",
            "argstr": "--s {subject_id}",
            "mandatory": True,
            "position": 1,
            "requires": ["subjects_dir"],
            "xor": ["reference_file"],
        },
    ),
    (
        "dof",
        ty.Any,
        {
            "help_string": "number of transform degrees of freedom",
            "argstr": "--dof {dof}",
        },
    ),
    (
        "reference_mask",
        ty.Any,
        {
            "help_string": "mask reference volume with given mask, or None if ``False``",
            "argstr": "--ref-mask {reference_mask}",
            "position": 2,
        },
    ),
    (
        "source_mask",
        str,
        {"help_string": "mask source file with given mask", "argstr": "--mov-mask"},
    ),
    (
        "num_threads",
        int,
        {
            "help_string": "number of OpenMP threads",
            "argstr": "--threads {num_threads}",
        },
    ),
    (
        "no_coord_dithering",
        bool,
        {"help_string": "turn off coordinate dithering", "argstr": "--no-coord-dither"},
    ),
    (
        "no_intensity_dithering",
        bool,
        {
            "help_string": "turn off intensity dithering",
            "argstr": "--no-intensity-dither",
        },
    ),
    (
        "sep",
        list,
        {
            "help_string": "set spatial scales, in voxels (default [2, 4])",
            "argstr": "--sep {sep}...",
        },
    ),
    (
        "initial_translation",
        ty.Any,
        {
            "help_string": "initial translation in mm (implies no_cras0)",
            "argstr": "--trans {initial_translation[0]} {initial_translation[1]} {initial_translation[2]}",
        },
    ),
    (
        "initial_rotation",
        ty.Any,
        {
            "help_string": "initial rotation in degrees",
            "argstr": "--rot {initial_rotation[0]} {initial_rotation[1]} {initial_rotation[2]}",
        },
    ),
    (
        "initial_scale",
        ty.Any,
        {
            "help_string": "initial scale",
            "argstr": "--scale {initial_scale[0]} {initial_scale[1]} {initial_scale[2]}",
        },
    ),
    (
        "initial_shear",
        ty.Any,
        {
            "help_string": "initial shear (Hxy, Hxz, Hyz)",
            "argstr": "--shear {initial_shear[0]} {initial_shear[1]} {initial_shear[2]}",
        },
    ),
    (
        "no_cras0",
        bool,
        {
            "help_string": "do not set translation parameters to align centers of source and reference files",
            "argstr": "--no-cras0",
        },
    ),
    (
        "max_iters",
        ty.Any,
        {
            "help_string": "maximum iterations (default: 4)",
            "argstr": "--nitersmax {max_iters}",
        },
    ),
    (
        "ftol",
        float,
        {
            "help_string": "floating-point tolerance (default=1e-7)",
            "argstr": "--ftol %e",
        },
    ),
    ("linmintol", float, {"help_string": "", "argstr": "--linmintol %e"}),
    (
        "saturation_threshold",
        ty.Any,
        {
            "help_string": "saturation threshold (default=9.999)",
            "argstr": "--sat {saturation_threshold}",
        },
    ),
    (
        "conform_reference",
        bool,
        {"help_string": "conform reference without rescaling", "argstr": "--conf-ref"},
    ),
    (
        "no_brute_force",
        bool,
        {"help_string": "do not brute force search", "argstr": "--no-bf"},
    ),
    (
        "brute_force_limit",
        float,
        {
            "help_string": "constrain brute force search to +/- lim",
            "argstr": "--bf-lim {brute_force_limit}",
            "xor": ["no_brute_force"],
        },
    ),
    (
        "brute_force_samples",
        int,
        {
            "help_string": "number of samples in brute force search",
            "argstr": "--bf-nsamp {brute_force_samples}",
            "xor": ["no_brute_force"],
        },
    ),
    (
        "no_smooth",
        bool,
        {
            "help_string": "do not apply smoothing to either reference or source file",
            "argstr": "--no-smooth",
        },
    ),
    (
        "ref_fwhm",
        float,
        {"help_string": "apply smoothing to reference file", "argstr": "--ref-fwhm"},
    ),
    (
        "source_oob",
        bool,
        {
            "help_string": "count source voxels that are out-of-bounds as 0",
            "argstr": "--mov-oob",
        },
    ),
]
MRICoreg_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_reg_file", File, {"help_string": "output registration file"}),
    ("out_lta_file", File, {"help_string": "output LTA-style registration file"}),
    ("out_params_file", File, {"help_string": "output parameters file"}),
]
MRICoreg_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MRICoreg(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.freesurfer.auto.registration.mri_coreg import MRICoreg

    >>> task = MRICoreg()
    >>> task.inputs.source_file = Nifti1.mock("moving1.nii")
    >>> task.inputs.reference_file = Nifti1.mock("fixed1.nii")
    >>> task.inputs.subjects_dir = Directory.mock(".")
    >>> task.cmdline
    'mri_coreg --lta .../registration.lta --ref fixed1.nii --mov moving1.nii --sd .'


    >>> task = MRICoreg()
    >>> task.inputs.source_file = Nifti1.mock("moving1.nii")
    >>> task.inputs.reference_file = Nifti1.mock()
    >>> task.inputs.subjects_dir = Directory.mock(".")
    >>> task.inputs.subject_id = "fsaverage"
    >>> task.inputs.reference_mask = False
    >>> task.cmdline
    'mri_coreg --s fsaverage --no-ref-mask --lta .../registration.lta --mov moving1.nii --sd .'


    >>> task = MRICoreg()
    >>> task.inputs.source_file = Nifti1.mock()
    >>> task.inputs.reference_file = Nifti1.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.inputs.sep = [4]
    >>> task.cmdline
    'mri_coreg --s fsaverage --no-ref-mask --lta .../registration.lta --sep 4 --mov moving1.nii --sd .'


    >>> task = MRICoreg()
    >>> task.inputs.source_file = Nifti1.mock()
    >>> task.inputs.reference_file = Nifti1.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.inputs.sep = [4, 5]
    >>> task.cmdline
    'mri_coreg --s fsaverage --no-ref-mask --lta .../registration.lta --sep 4 --sep 5 --mov moving1.nii --sd .'


    """

    input_spec = MRICoreg_input_spec
    output_spec = MRICoreg_output_spec
    executable = "mri_coreg"
