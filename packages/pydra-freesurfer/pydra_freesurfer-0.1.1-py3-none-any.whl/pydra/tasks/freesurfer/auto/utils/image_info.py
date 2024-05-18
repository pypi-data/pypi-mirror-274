from fileformats.generic import Directory, File
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


def TE_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["TE"]


def TI_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["TI"]


def TR_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["TR"]


def data_type_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["data_type"]


def dimensions_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["dimensions"]


def file_format_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["file_format"]


def info_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["info"]


def orientation_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["orientation"]


def ph_enc_dir_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["ph_enc_dir"]


def vox_sizes_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["vox_sizes"]


input_fields = [
    (
        "in_file",
        File,
        {"help_string": "image to query", "argstr": "{in_file}", "position": 1},
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
ImageInfo_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "info",
        ty.Any,
        {"help_string": "output of mri_info", "callable": "info_callable"},
    ),
    ("out_file", File, {"help_string": "text file with image information"}),
    (
        "data_type",
        ty.Any,
        {"help_string": "image data type", "callable": "data_type_callable"},
    ),
    (
        "file_format",
        ty.Any,
        {"help_string": "file format", "callable": "file_format_callable"},
    ),
    ("TE", ty.Any, {"help_string": "echo time (msec)", "callable": "TE_callable"}),
    ("TR", ty.Any, {"help_string": "repetition time(msec)", "callable": "TR_callable"}),
    ("TI", ty.Any, {"help_string": "inversion time (msec)", "callable": "TI_callable"}),
    (
        "dimensions",
        ty.Any,
        {"help_string": "image dimensions (voxels)", "callable": "dimensions_callable"},
    ),
    (
        "vox_sizes",
        ty.Any,
        {"help_string": "voxel sizes (mm)", "callable": "vox_sizes_callable"},
    ),
    (
        "orientation",
        ty.Any,
        {"help_string": "image orientation", "callable": "orientation_callable"},
    ),
    (
        "ph_enc_dir",
        ty.Any,
        {"help_string": "phase encode direction", "callable": "ph_enc_dir_callable"},
    ),
]
ImageInfo_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ImageInfo(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.auto.utils.image_info import ImageInfo

    """

    input_spec = ImageInfo_input_spec
    output_spec = ImageInfo_output_spec
    executable = "mri_info"
