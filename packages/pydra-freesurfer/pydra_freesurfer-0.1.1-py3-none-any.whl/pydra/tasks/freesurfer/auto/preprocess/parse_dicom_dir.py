from fileformats.generic import Directory, File
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "dicom_dir",
        Directory,
        {
            "help_string": "path to siemens dicom directory",
            "argstr": "--d {dicom_dir}",
            "mandatory": True,
        },
    ),
    (
        "dicom_info_file",
        Path,
        "dicominfo.txt",
        {
            "help_string": "file to which results are written",
            "argstr": "--o {dicom_info_file}",
        },
    ),
    ("sortbyrun", bool, {"help_string": "assign run numbers", "argstr": "--sortbyrun"}),
    (
        "summarize",
        bool,
        {"help_string": "only print out info for run leaders", "argstr": "--summarize"},
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
ParseDICOMDir_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("dicom_info_file", File, {"help_string": "text file containing dicom information"})
]
ParseDICOMDir_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ParseDICOMDir(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.auto.preprocess.parse_dicom_dir import ParseDICOMDir

    >>> task = ParseDICOMDir()
    >>> task.inputs.dicom_dir = Directory.mock(".")
    >>> task.inputs.sortbyrun = True
    >>> task.inputs.summarize = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_parse_sdcmdir --d . --o dicominfo.txt --sortbyrun --summarize'


    """

    input_spec = ParseDICOMDir_input_spec
    output_spec = ParseDICOMDir_output_spec
    executable = "mri_parse_sdcmdir"
