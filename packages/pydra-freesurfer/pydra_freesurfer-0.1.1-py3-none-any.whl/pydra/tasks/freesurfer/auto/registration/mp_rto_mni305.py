from fileformats.generic import Directory, File
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    ("reference_dir", Directory, {"help_string": "TODO", "mandatory": True}),
    ("target", ty.Any, {"help_string": "input atlas file", "mandatory": True}),
    (
        "in_file",
        File,
        {"help_string": "the input file prefix for MPRtoMNI305", "argstr": "{in_file}"},
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
MPRtoMNI305_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_file",
        File,
        {"help_string": "The output file '<in_file>_to_<target>_t4_vox2vox.txt'"},
    ),
    ("log_file", File, {"help_string": "The output log"}),
]
MPRtoMNI305_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MPRtoMNI305(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.auto.registration.mp_rto_mni305 import MPRtoMNI305

    >>> task = MPRtoMNI305()
    >>> task.inputs.reference_dir = Directory.mock("." # doctest: +SKIP)
    >>> task.inputs.target = "structural.nii"
    >>> task.inputs.in_file = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'structural'


    """

    input_spec = MPRtoMNI305_input_spec
    output_spec = MPRtoMNI305_output_spec
    executable = "mpr2mni305"
