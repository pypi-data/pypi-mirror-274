from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
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
            "help_string": "Individual volumes to be concatenated",
            "argstr": "--i {in_files}...",
            "mandatory": True,
        },
    ),
    (
        "concatenated_file",
        Path,
        {
            "help_string": "Output volume",
            "argstr": "--o {concatenated_file}",
            "output_file_template": '"bar.nii"',
        },
    ),
    (
        "sign",
        ty.Any,
        {
            "help_string": "Take only pos or neg voxles from input, or take abs",
            "argstr": "--{sign}",
        },
    ),
    (
        "stats",
        ty.Any,
        {
            "help_string": "Compute the sum, var, std, max, min or mean of the input volumes",
            "argstr": "--{stats}",
        },
    ),
    (
        "paired_stats",
        ty.Any,
        {
            "help_string": "Compute paired sum, avg, or diff",
            "argstr": "--paired-{paired_stats}",
        },
    ),
    (
        "gmean",
        int,
        {
            "help_string": "create matrix to average Ng groups, Nper=Ntot/Ng",
            "argstr": "--gmean {gmean}",
        },
    ),
    (
        "mean_div_n",
        bool,
        {
            "help_string": "compute mean/nframes (good for var)",
            "argstr": "--mean-div-n",
        },
    ),
    (
        "multiply_by",
        float,
        {
            "help_string": "Multiply input volume by some amount",
            "argstr": "--mul {multiply_by}",
        },
    ),
    (
        "add_val",
        float,
        {
            "help_string": "Add some amount to the input volume",
            "argstr": "--add {add_val}",
        },
    ),
    (
        "multiply_matrix_file",
        File,
        {
            "help_string": "Multiply input by an ascii matrix in file",
            "argstr": "--mtx {multiply_matrix_file}",
        },
    ),
    (
        "combine",
        bool,
        {
            "help_string": "Combine non-zero values into single frame volume",
            "argstr": "--combine",
        },
    ),
    (
        "keep_dtype",
        bool,
        {
            "help_string": "Keep voxelwise precision type (default is float",
            "argstr": "--keep-datatype",
        },
    ),
    (
        "max_bonfcor",
        bool,
        {
            "help_string": "Compute max and bonferroni correct (assumes -log10(ps))",
            "argstr": "--max-bonfcor",
        },
    ),
    (
        "max_index",
        bool,
        {
            "help_string": "Compute the index of max voxel in concatenated volumes",
            "argstr": "--max-index",
        },
    ),
    (
        "mask_file",
        File,
        {"help_string": "Mask input with a volume", "argstr": "--mask {mask_file}"},
    ),
    (
        "vote",
        bool,
        {
            "help_string": "Most frequent value at each voxel and fraction of occurrences",
            "argstr": "--vote",
        },
    ),
    (
        "sort",
        bool,
        {"help_string": "Sort each voxel by ascending frame value", "argstr": "--sort"},
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
Concatenate_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Concatenate_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Concatenate(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.freesurfer.auto.model.concatenate import Concatenate

    >>> task = Concatenate()
    >>> task.inputs.in_files = [Nifti1.mock("cont1.nii"), Nifti1.mock("cont2.nii")]
    >>> task.inputs.concatenated_file = "bar.nii"
    >>> task.inputs.multiply_matrix_file = File.mock()
    >>> task.inputs.mask_file = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_concat --o bar.nii --i cont1.nii --i cont2.nii'


    """

    input_spec = Concatenate_input_spec
    output_spec = Concatenate_output_spec
    executable = "mri_concat"
