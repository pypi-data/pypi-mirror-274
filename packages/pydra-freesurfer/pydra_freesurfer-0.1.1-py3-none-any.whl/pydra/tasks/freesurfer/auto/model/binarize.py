from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input volume",
            "argstr": "--i {in_file}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "min",
        float,
        {"help_string": "min thresh", "argstr": "--min {min}", "xor": ["wm_ven_csf"]},
    ),
    (
        "max",
        float,
        {"help_string": "max thresh", "argstr": "--max {max}", "xor": ["wm_ven_csf"]},
    ),
    (
        "rmin",
        float,
        {
            "help_string": "compute min based on rmin*globalmean",
            "argstr": "--rmin {rmin}",
        },
    ),
    (
        "rmax",
        float,
        {
            "help_string": "compute max based on rmax*globalmean",
            "argstr": "--rmax {rmax}",
        },
    ),
    (
        "match",
        list,
        {"help_string": "match instead of threshold", "argstr": "--match {match}..."},
    ),
    (
        "wm",
        bool,
        {
            "help_string": "set match vals to 2 and 41 (aseg for cerebral WM)",
            "argstr": "--wm",
        },
    ),
    (
        "ventricles",
        bool,
        {
            "help_string": "set match vals those for aseg ventricles+choroid (not 4th)",
            "argstr": "--ventricles",
        },
    ),
    (
        "wm_ven_csf",
        bool,
        {
            "help_string": "WM and ventricular CSF, including choroid (not 4th)",
            "argstr": "--wm+vcsf",
            "xor": ["min", "max"],
        },
    ),
    (
        "binary_file",
        Path,
        {
            "help_string": "binary output volume",
            "argstr": "--o {binary_file}",
            "output_file_template": '"foo_out.nii"',
        },
    ),
    ("out_type", ty.Any, {"help_string": "output file type", "argstr": ""}),
    (
        "count_file",
        ty.Any,
        {
            "help_string": "save number of hits in ascii file (hits, ntotvox, pct)",
            "argstr": "--count {count_file}",
        },
    ),
    (
        "bin_val",
        int,
        {
            "help_string": "set vox within thresh to val (default is 1)",
            "argstr": "--binval {bin_val}",
        },
    ),
    (
        "bin_val_not",
        int,
        {
            "help_string": "set vox outside range to val (default is 0)",
            "argstr": "--binvalnot {bin_val_not}",
        },
    ),
    ("invert", bool, {"help_string": "set binval=0, binvalnot=1", "argstr": "--inv"}),
    (
        "frame_no",
        int,
        {
            "help_string": "use 0-based frame of input (default is 0)",
            "argstr": "--frame {frame_no}",
        },
    ),
    (
        "merge_file",
        File,
        {"help_string": "merge with mergevol", "argstr": "--merge {merge_file}"},
    ),
    (
        "mask_file",
        File,
        {"help_string": "must be within mask", "argstr": "--mask maskvol"},
    ),
    (
        "mask_thresh",
        float,
        {"help_string": "set thresh for mask", "argstr": "--mask-thresh {mask_thresh}"},
    ),
    (
        "abs",
        bool,
        {
            "help_string": "take abs of invol first (ie, make unsigned)",
            "argstr": "--abs",
        },
    ),
    (
        "bin_col_num",
        bool,
        {
            "help_string": "set binarized voxel value to its column number",
            "argstr": "--bincol",
        },
    ),
    (
        "zero_edges",
        bool,
        {"help_string": "zero the edge voxels", "argstr": "--zero-edges"},
    ),
    (
        "zero_slice_edge",
        bool,
        {"help_string": "zero the edge slice voxels", "argstr": "--zero-slice-edges"},
    ),
    (
        "dilate",
        int,
        {
            "help_string": "niters: dilate binarization in 3D",
            "argstr": "--dilate {dilate}",
        },
    ),
    (
        "erode",
        int,
        {
            "help_string": "nerode: erode binarization in 3D (after any dilation)",
            "argstr": "--erode  {erode}",
        },
    ),
    (
        "erode2d",
        int,
        {
            "help_string": "nerode2d: erode binarization in 2D (after any 3D erosion)",
            "argstr": "--erode2d {erode2d}",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
Binarize_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("count_file", File, {"help_string": "ascii file containing number of hits"})
]
Binarize_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Binarize(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.freesurfer.auto.model.binarize import Binarize

    >>> task = Binarize()
    >>> task.inputs.in_file = Nifti1.mock("structural.nii")
    >>> task.inputs.min = 10
    >>> task.inputs.binary_file = "foo_out.nii"
    >>> task.inputs.merge_file = File.mock()
    >>> task.inputs.mask_file = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_binarize --o foo_out.nii --i structural.nii --min 10.000000'


    """

    input_spec = Binarize_input_spec
    output_spec = Binarize_output_spec
    executable = "mri_binarize"
