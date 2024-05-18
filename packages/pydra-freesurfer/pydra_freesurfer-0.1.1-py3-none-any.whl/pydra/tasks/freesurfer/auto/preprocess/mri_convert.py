from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "read_only",
        bool,
        {"help_string": "read the input volume", "argstr": "--read_only"},
    ),
    ("no_write", bool, {"help_string": "do not write output", "argstr": "--no_write"}),
    ("in_info", bool, {"help_string": "display input info", "argstr": "--in_info"}),
    ("out_info", bool, {"help_string": "display output info", "argstr": "--out_info"}),
    ("in_stats", bool, {"help_string": "display input stats", "argstr": "--in_stats"}),
    (
        "out_stats",
        bool,
        {"help_string": "display output stats", "argstr": "--out_stats"},
    ),
    (
        "in_matrix",
        bool,
        {"help_string": "display input matrix", "argstr": "--in_matrix"},
    ),
    (
        "out_matrix",
        bool,
        {"help_string": "display output matrix", "argstr": "--out_matrix"},
    ),
    (
        "in_i_size",
        int,
        {"help_string": "input i size", "argstr": "--in_i_size {in_i_size}"},
    ),
    (
        "in_j_size",
        int,
        {"help_string": "input j size", "argstr": "--in_j_size {in_j_size}"},
    ),
    (
        "in_k_size",
        int,
        {"help_string": "input k size", "argstr": "--in_k_size {in_k_size}"},
    ),
    (
        "force_ras",
        bool,
        {
            "help_string": "use default when orientation info absent",
            "argstr": "--force_ras_good",
        },
    ),
    (
        "in_i_dir",
        ty.Any,
        {
            "help_string": "<R direction> <A direction> <S direction>",
            "argstr": "--in_i_direction {in_i_dir[0]} {in_i_dir[1]} {in_i_dir[2]}",
        },
    ),
    (
        "in_j_dir",
        ty.Any,
        {
            "help_string": "<R direction> <A direction> <S direction>",
            "argstr": "--in_j_direction {in_j_dir[0]} {in_j_dir[1]} {in_j_dir[2]}",
        },
    ),
    (
        "in_k_dir",
        ty.Any,
        {
            "help_string": "<R direction> <A direction> <S direction>",
            "argstr": "--in_k_direction {in_k_dir[0]} {in_k_dir[1]} {in_k_dir[2]}",
        },
    ),
    (
        "in_orientation",
        ty.Any,
        {
            "help_string": "specify the input orientation",
            "argstr": "--in_orientation {in_orientation}",
        },
    ),
    (
        "in_center",
        list,
        {
            "help_string": "<R coordinate> <A coordinate> <S coordinate>",
            "argstr": "--in_center {in_center}",
        },
    ),
    (
        "sphinx",
        bool,
        {"help_string": "change orientation info to sphinx", "argstr": "--sphinx"},
    ),
    (
        "out_i_count",
        int,
        {
            "help_string": "some count ?? in i direction",
            "argstr": "--out_i_count {out_i_count}",
        },
    ),
    (
        "out_j_count",
        int,
        {
            "help_string": "some count ?? in j direction",
            "argstr": "--out_j_count {out_j_count}",
        },
    ),
    (
        "out_k_count",
        int,
        {
            "help_string": "some count ?? in k direction",
            "argstr": "--out_k_count {out_k_count}",
        },
    ),
    (
        "vox_size",
        ty.Any,
        {
            "help_string": "<size_x> <size_y> <size_z> specify the size (mm) - useful for upsampling or downsampling",
            "argstr": "-voxsize {vox_size[0]} {vox_size[1]} {vox_size[2]}",
        },
    ),
    (
        "out_i_size",
        int,
        {"help_string": "output i size", "argstr": "--out_i_size {out_i_size}"},
    ),
    (
        "out_j_size",
        int,
        {"help_string": "output j size", "argstr": "--out_j_size {out_j_size}"},
    ),
    (
        "out_k_size",
        int,
        {"help_string": "output k size", "argstr": "--out_k_size {out_k_size}"},
    ),
    (
        "out_i_dir",
        ty.Any,
        {
            "help_string": "<R direction> <A direction> <S direction>",
            "argstr": "--out_i_direction {out_i_dir[0]} {out_i_dir[1]} {out_i_dir[2]}",
        },
    ),
    (
        "out_j_dir",
        ty.Any,
        {
            "help_string": "<R direction> <A direction> <S direction>",
            "argstr": "--out_j_direction {out_j_dir[0]} {out_j_dir[1]} {out_j_dir[2]}",
        },
    ),
    (
        "out_k_dir",
        ty.Any,
        {
            "help_string": "<R direction> <A direction> <S direction>",
            "argstr": "--out_k_direction {out_k_dir[0]} {out_k_dir[1]} {out_k_dir[2]}",
        },
    ),
    (
        "out_orientation",
        ty.Any,
        {
            "help_string": "specify the output orientation",
            "argstr": "--out_orientation {out_orientation}",
        },
    ),
    (
        "out_center",
        ty.Any,
        {
            "help_string": "<R coordinate> <A coordinate> <S coordinate>",
            "argstr": "--out_center {out_center[0]} {out_center[1]} {out_center[2]}",
        },
    ),
    (
        "out_datatype",
        ty.Any,
        {
            "help_string": "output data type <uchar|short|int|float>",
            "argstr": "--out_data_type {out_datatype}",
        },
    ),
    (
        "resample_type",
        ty.Any,
        {
            "help_string": "<interpolate|weighted|nearest|sinc|cubic> (default is interpolate)",
            "argstr": "--resample_type {resample_type}",
        },
    ),
    (
        "no_scale",
        bool,
        {"help_string": "dont rescale values for COR", "argstr": "--no_scale 1"},
    ),
    (
        "no_change",
        bool,
        {
            "help_string": "don't change type of input to that of template",
            "argstr": "--nochange",
        },
    ),
    ("tr", int, {"help_string": "TR in msec", "argstr": "-tr {tr}"}),
    ("te", int, {"help_string": "TE in msec", "argstr": "-te {te}"}),
    (
        "ti",
        int,
        {"help_string": "TI in msec (note upper case flag)", "argstr": "-ti {ti}"},
    ),
    (
        "autoalign_matrix",
        File,
        {
            "help_string": "text file with autoalign matrix",
            "argstr": "--autoalign {autoalign_matrix}",
        },
    ),
    (
        "unwarp_gradient",
        bool,
        {
            "help_string": "unwarp gradient nonlinearity",
            "argstr": "--unwarp_gradient_nonlinearity",
        },
    ),
    (
        "apply_transform",
        File,
        {
            "help_string": "apply xfm file",
            "argstr": "--apply_transform {apply_transform}",
        },
    ),
    (
        "apply_inv_transform",
        File,
        {
            "help_string": "apply inverse transformation xfm file",
            "argstr": "--apply_inverse_transform {apply_inv_transform}",
        },
    ),
    (
        "devolve_transform",
        str,
        {"help_string": "subject id", "argstr": "--devolvexfm {devolve_transform}"},
    ),
    (
        "crop_center",
        ty.Any,
        {
            "help_string": "<x> <y> <z> crop to 256 around center (x, y, z)",
            "argstr": "--crop {crop_center[0]} {crop_center[1]} {crop_center[2]}",
        },
    ),
    (
        "crop_size",
        ty.Any,
        {
            "help_string": "<dx> <dy> <dz> crop to size <dx, dy, dz>",
            "argstr": "--cropsize {crop_size[0]} {crop_size[1]} {crop_size[2]}",
        },
    ),
    (
        "cut_ends",
        int,
        {
            "help_string": "remove ncut slices from the ends",
            "argstr": "--cutends {cut_ends}",
        },
    ),
    (
        "slice_crop",
        ty.Any,
        {
            "help_string": "s_start s_end : keep slices s_start to s_end",
            "argstr": "--slice-crop {slice_crop[0]} {slice_crop[1]}",
        },
    ),
    (
        "slice_reverse",
        bool,
        {
            "help_string": "reverse order of slices, update vox2ras",
            "argstr": "--slice-reverse",
        },
    ),
    (
        "slice_bias",
        float,
        {
            "help_string": "apply half-cosine bias field",
            "argstr": "--slice-bias {slice_bias}",
        },
    ),
    (
        "fwhm",
        float,
        {"help_string": "smooth input volume by fwhm mm", "argstr": "--fwhm {fwhm}"},
    ),
    (
        "in_type",
        ty.Any,
        {"help_string": "input file type", "argstr": "--in_type {in_type}"},
    ),
    (
        "out_type",
        ty.Any,
        {"help_string": "output file type", "argstr": "--out_type {out_type}"},
    ),
    (
        "ascii",
        bool,
        {
            "help_string": "save output as ascii col>row>slice>frame",
            "argstr": "--ascii",
        },
    ),
    (
        "reorder",
        ty.Any,
        {
            "help_string": "olddim1 olddim2 olddim3",
            "argstr": "--reorder {reorder[0]} {reorder[1]} {reorder[2]}",
        },
    ),
    (
        "invert_contrast",
        float,
        {
            "help_string": "threshold for inversting contrast",
            "argstr": "--invert_contrast {invert_contrast}",
        },
    ),
    (
        "in_file",
        Nifti1,
        {
            "help_string": "File to read/convert",
            "argstr": "--input_volume {in_file}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output filename or True to generate one",
            "argstr": "--output_volume {out_file}",
            "position": -1,
            "output_file_template": '"outfile.mgz"',
        },
    ),
    (
        "conform",
        bool,
        {
            "help_string": "conform to 1mm voxel size in coronal slice direction with 256^3 or more",
            "argstr": "--conform",
        },
    ),
    (
        "conform_min",
        bool,
        {"help_string": "conform to smallest size", "argstr": "--conform_min"},
    ),
    (
        "conform_size",
        float,
        {
            "help_string": "conform to size_in_mm",
            "argstr": "--conform_size {conform_size}",
        },
    ),
    (
        "cw256",
        bool,
        {"help_string": "confrom to dimensions of 256^3", "argstr": "--cw256"},
    ),
    ("parse_only", bool, {"help_string": "parse input only", "argstr": "--parse_only"}),
    (
        "subject_name",
        str,
        {"help_string": "subject name ???", "argstr": "--subject_name {subject_name}"},
    ),
    (
        "reslice_like",
        File,
        {
            "help_string": "reslice output to match file",
            "argstr": "--reslice_like {reslice_like}",
        },
    ),
    (
        "template_type",
        ty.Any,
        {
            "help_string": "template file type",
            "argstr": "--template_type {template_type}",
        },
    ),
    (
        "split",
        bool,
        {
            "help_string": "split output frames into separate output files.",
            "argstr": "--split",
        },
    ),
    (
        "frame",
        int,
        {"help_string": "keep only 0-based frame number", "argstr": "--frame {frame}"},
    ),
    (
        "midframe",
        bool,
        {"help_string": "keep only the middle frame", "argstr": "--mid-frame"},
    ),
    (
        "skip_n",
        int,
        {"help_string": "skip the first n frames", "argstr": "--nskip {skip_n}"},
    ),
    (
        "drop_n",
        int,
        {"help_string": "drop the last n frames", "argstr": "--ndrop {drop_n}"},
    ),
    (
        "frame_subsample",
        ty.Any,
        {
            "help_string": "start delta end : frame subsampling (end = -1 for end)",
            "argstr": "--fsubsample {frame_subsample[0]} {frame_subsample[1]} {frame_subsample[2]}",
        },
    ),
    (
        "in_scale",
        float,
        {"help_string": "input intensity scale factor", "argstr": "--scale {in_scale}"},
    ),
    (
        "out_scale",
        float,
        {
            "help_string": "output intensity scale factor",
            "argstr": "--out-scale {out_scale}",
        },
    ),
    (
        "in_like",
        File,
        {"help_string": "input looks like", "argstr": "--in_like {in_like}"},
    ),
    (
        "fill_parcellation",
        bool,
        {"help_string": "fill parcellation", "argstr": "--fill_parcellation"},
    ),
    (
        "smooth_parcellation",
        bool,
        {"help_string": "smooth parcellation", "argstr": "--smooth_parcellation"},
    ),
    (
        "zero_outlines",
        bool,
        {"help_string": "zero outlines", "argstr": "--zero_outlines"},
    ),
    (
        "color_file",
        File,
        {"help_string": "color file", "argstr": "--color_file {color_file}"},
    ),
    ("no_translate", bool, {"help_string": "???", "argstr": "--no_translate"}),
    (
        "status_file",
        File,
        {
            "help_string": "status file for DICOM conversion",
            "argstr": "--status {status_file}",
        },
    ),
    (
        "sdcm_list",
        File,
        {
            "help_string": "list of DICOM files for conversion",
            "argstr": "--sdcmlist {sdcm_list}",
        },
    ),
    (
        "template_info",
        bool,
        {"help_string": "dump info about template", "argstr": "--template_info"},
    ),
    ("crop_gdf", bool, {"help_string": "apply GDF cropping", "argstr": "--crop_gdf"}),
    (
        "zero_ge_z_offset",
        bool,
        {"help_string": "zero ge z offset ???", "argstr": "--zero_ge_z_offset"},
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
MRIConvert_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
MRIConvert_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MRIConvert(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.freesurfer.auto.preprocess.mri_convert import MRIConvert

    >>> task = MRIConvert()
    >>> task.inputs.autoalign_matrix = File.mock()
    >>> task.inputs.apply_transform = File.mock()
    >>> task.inputs.apply_inv_transform = File.mock()
    >>> task.inputs.out_type = "mgz"
    >>> task.inputs.in_file = Nifti1.mock("structural.nii")
    >>> task.inputs.out_file = "outfile.mgz"
    >>> task.inputs.reslice_like = File.mock()
    >>> task.inputs.in_like = File.mock()
    >>> task.inputs.color_file = File.mock()
    >>> task.inputs.status_file = File.mock()
    >>> task.inputs.sdcm_list = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_convert --out_type mgz --input_volume structural.nii --output_volume outfile.mgz'


    """

    input_spec = MRIConvert_input_spec
    output_spec = MRIConvert_output_spec
    executable = "mri_convert"
