from fileformats.generic import Directory, File
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "source_dir",
        Directory,
        {
            "help_string": "directory with the DICOM files",
            "argstr": "-src {source_dir}",
            "mandatory": True,
        },
    ),
    (
        "output_dir",
        Directory,
        {
            "help_string": "top directory into which the files will be unpacked",
            "argstr": "-targ {output_dir}",
        },
    ),
    (
        "run_info",
        ty.Any,
        {
            "help_string": "runno subdir format name : spec unpacking rules on cmdline",
            "argstr": "-run {run_info[0]} {run_info[1]} {run_info[2]} {run_info[3]}",
            "mandatory": True,
            "xor": ("run_info", "config", "seq_config"),
        },
    ),
    (
        "config",
        File,
        {
            "help_string": "specify unpacking rules in file",
            "argstr": "-cfg {config}",
            "mandatory": True,
            "xor": ("run_info", "config", "seq_config"),
        },
    ),
    (
        "seq_config",
        File,
        {
            "help_string": "specify unpacking rules based on sequence",
            "argstr": "-seqcfg {seq_config}",
            "mandatory": True,
            "xor": ("run_info", "config", "seq_config"),
        },
    ),
    (
        "dir_structure",
        ty.Any,
        {
            "help_string": "unpack to specified directory structures",
            "argstr": "-{dir_structure}",
        },
    ),
    (
        "no_info_dump",
        bool,
        {"help_string": "do not create infodump file", "argstr": "-noinfodump"},
    ),
    (
        "scan_only",
        File,
        {
            "help_string": "only scan the directory and put result in file",
            "argstr": "-scanonly {scan_only}",
        },
    ),
    (
        "log_file",
        File,
        {"help_string": "explicitly set log file", "argstr": "-log {log_file}"},
    ),
    (
        "spm_zeropad",
        int,
        {
            "help_string": "set frame number zero padding width for SPM",
            "argstr": "-nspmzeropad {spm_zeropad}",
        },
    ),
    (
        "no_unpack_err",
        bool,
        {
            "help_string": "do not try to unpack runs with errors",
            "argstr": "-no-unpackerr",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
UnpackSDICOMDir_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
UnpackSDICOMDir_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class UnpackSDICOMDir(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.auto.preprocess.unpack_sdicom_dir import UnpackSDICOMDir

    >>> task = UnpackSDICOMDir()
    >>> task.inputs.source_dir = Directory.mock(".")
    >>> task.inputs.output_dir = Directory.mock(".")
    >>> task.inputs.run_info = (5, "mprage", "nii", "struct")
    >>> task.inputs.config = File.mock()
    >>> task.inputs.seq_config = File.mock()
    >>> task.inputs.dir_structure = "generic"
    >>> task.inputs.scan_only = File.mock()
    >>> task.inputs.log_file = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'unpacksdcmdir -generic -targ . -run 5 mprage nii struct -src .'


    """

    input_spec = UnpackSDICOMDir_input_spec
    output_spec = UnpackSDICOMDir_output_spec
    executable = "unpacksdcmdir"
