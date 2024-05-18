from fileformats.generic import Directory, File
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "dicom_dir",
        Directory,
        {
            "help_string": "dicom directory from which to convert dicom files",
            "mandatory": True,
        },
    ),
    (
        "base_output_dir",
        Directory,
        {
            "help_string": "directory in which subject directories are created",
            "mandatory": True,
        },
    ),
    (
        "subject_dir_template",
        str,
        "S.%04d",
        {"help_string": "template for subject directory name"},
    ),
    (
        "subject_id",
        ty.Any,
        {"help_string": "subject identifier to insert into template"},
    ),
    ("file_mapping", list, {"help_string": "defines the output fields of interface"}),
    (
        "out_type",
        ty.Any,
        "niigz",
        {"help_string": "defines the type of output file produced"},
    ),
    (
        "dicom_info",
        File,
        {"help_string": "File containing summary information from mri_parse_sdcmdir"},
    ),
    (
        "seq_list",
        list,
        {
            "help_string": "list of pulse sequence names to be converted.",
            "requires": ["dicom_info"],
        },
    ),
    (
        "ignore_single_slice",
        bool,
        {
            "help_string": "ignore volumes containing a single slice",
            "requires": ["dicom_info"],
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
DICOMConvert_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
DICOMConvert_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class DICOMConvert(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.auto.preprocess.dicom_convert import DICOMConvert

    """

    input_spec = DICOMConvert_input_spec
    output_spec = DICOMConvert_output_spec
    executable = "mri_convert"
