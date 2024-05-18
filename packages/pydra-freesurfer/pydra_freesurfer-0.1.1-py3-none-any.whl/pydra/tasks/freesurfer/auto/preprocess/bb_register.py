from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "init",
        ty.Any,
        {
            "help_string": "initialize registration with mri_coreg, spm, fsl, or header",
            "argstr": "--init-{init}",
            "xor": ["init_reg_file"],
        },
    ),
    (
        "init_reg_file",
        File,
        {
            "help_string": "existing registration file",
            "argstr": "--init-reg {init_reg_file}",
            "xor": ["init"],
        },
    ),
    (
        "subject_id",
        str,
        {
            "help_string": "freesurfer subject id",
            "argstr": "--s {subject_id}",
            "mandatory": True,
        },
    ),
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
        "contrast_type",
        ty.Any,
        {
            "help_string": "contrast type of image",
            "argstr": "--{contrast_type}",
            "mandatory": True,
        },
    ),
    (
        "intermediate_file",
        File,
        {
            "help_string": "Intermediate image, e.g. in case of partial FOV",
            "argstr": "--int {intermediate_file}",
        },
    ),
    (
        "reg_frame",
        int,
        {
            "help_string": "0-based frame index for 4D source file",
            "argstr": "--frame {reg_frame}",
            "xor": ["reg_middle_frame"],
        },
    ),
    (
        "reg_middle_frame",
        bool,
        {
            "help_string": "Register middle frame of 4D source file",
            "argstr": "--mid-frame",
            "xor": ["reg_frame"],
        },
    ),
    (
        "out_reg_file",
        Path,
        {
            "help_string": "output registration file",
            "argstr": "--reg {out_reg_file}",
            "output_file_template": "out_reg_file",
        },
    ),
    (
        "spm_nifti",
        bool,
        {
            "help_string": "force use of nifti rather than analyze with SPM",
            "argstr": "--spm-nii",
        },
    ),
    (
        "epi_mask",
        bool,
        {
            "help_string": "mask out B0 regions in stages 1 and 2",
            "argstr": "--epi-mask",
        },
    ),
    (
        "dof",
        ty.Any,
        {"help_string": "number of transform degrees of freedom", "argstr": "--{dof}"},
    ),
    (
        "fsldof",
        int,
        {
            "help_string": "degrees of freedom for initial registration (FSL)",
            "argstr": "--fsl-dof {fsldof}",
        },
    ),
    (
        "out_fsl_file",
        ty.Any,
        {
            "help_string": "write the transformation matrix in FSL FLIRT format",
            "argstr": "--fslmat {out_fsl_file}",
        },
    ),
    (
        "out_lta_file",
        ty.Any,
        {
            "help_string": "write the transformation matrix in LTA format",
            "argstr": "--lta {out_lta_file}",
        },
    ),
    (
        "registered_file",
        ty.Any,
        {
            "help_string": "output warped sourcefile either True or filename",
            "argstr": "--o {registered_file}",
        },
    ),
    (
        "init_cost_file",
        ty.Any,
        {
            "help_string": "output initial registration cost file",
            "argstr": "--initcost {init_cost_file}",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
BBRegister_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_fsl_file", File, {"help_string": "Output FLIRT-style registration file"}),
    ("out_lta_file", File, {"help_string": "Output LTA-style registration file"}),
    ("min_cost_file", File, {"help_string": "Output registration minimum cost file"}),
    ("init_cost_file", File, {"help_string": "Output initial registration cost file"}),
    ("registered_file", File, {"help_string": "Registered and resampled source file"}),
]
BBRegister_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class BBRegister(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.freesurfer.auto.preprocess.bb_register import BBRegister

    >>> task = BBRegister()
    >>> task.inputs.init = "header"
    >>> task.inputs.init_reg_file = File.mock()
    >>> task.inputs.subject_id = "me"
    >>> task.inputs.source_file = Nifti1.mock("structural.nii")
    >>> task.inputs.contrast_type = "t2"
    >>> task.inputs.intermediate_file = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'bbregister --t2 --init-header --reg structural_bbreg_me.dat --mov structural.nii --s me'


    """

    input_spec = BBRegister_input_spec
    output_spec = BBRegister_output_spec
    executable = "bbregister"
