from fileformats.datascience import DatFile, TextMatrix
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz, Nifti1
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "target_image",
        Nifti1,
        {
            "help_string": "target volume",
            "argstr": "--targ {target_image}",
            "xor": ["fstarg"],
        },
    ),
    (
        "fstarg",
        bool,
        {
            "help_string": "use subject's T1 as reference",
            "argstr": "--fstarg",
            "xor": ["target_image"],
        },
    ),
    (
        "moving_image",
        ty.Union[Nifti1, MghGz],
        {
            "help_string": "moving volume",
            "argstr": "--mov {moving_image}",
            "mandatory": True,
        },
    ),
    (
        "fsl_in_matrix",
        TextMatrix,
        {
            "help_string": "fsl-style registration input matrix",
            "argstr": "--fsl {fsl_in_matrix}",
        },
    ),
    (
        "xfm",
        File,
        {
            "help_string": "use a matrix in MNI coordinates as initial registration",
            "argstr": "--xfm {xfm}",
        },
    ),
    (
        "lta_in",
        File,
        {
            "help_string": "use a matrix in MNI coordinates as initial registration",
            "argstr": "--lta {lta_in}",
        },
    ),
    (
        "invert_lta_in",
        bool,
        {"help_string": "Invert input LTA before applying", "requires": ["lta_in"]},
    ),
    (
        "fsl_out",
        ty.Any,
        {
            "help_string": "compute an FSL-compatible resgitration matrix",
            "argstr": "--fslregout {fsl_out}",
        },
    ),
    (
        "lta_out",
        ty.Any,
        {
            "help_string": "output registration file (LTA format)",
            "argstr": "--ltaout {lta_out}",
        },
    ),
    (
        "invert_lta_out",
        bool,
        {
            "help_string": "Invert input LTA before applying",
            "argstr": "--ltaout-inv",
            "requires": ["lta_in"],
        },
    ),
    (
        "subject_id",
        ty.Any,
        {"help_string": "freesurfer subject ID", "argstr": "--s {subject_id}"},
    ),
    (
        "noedit",
        bool,
        True,
        {"help_string": "do not open edit window (exit)", "argstr": "--noedit"},
    ),
    (
        "reg_file",
        Path,
        {
            "help_string": "freesurfer-style registration file",
            "argstr": "--reg {reg_file}",
            "mandatory": True,
        },
    ),
    (
        "reg_header",
        bool,
        {"help_string": "compute regstration from headers", "argstr": "--regheader"},
    ),
    (
        "fstal",
        bool,
        {
            "help_string": "set mov to be tal and reg to be tal xfm",
            "argstr": "--fstal",
            "xor": ["target_image", "moving_image", "reg_file"],
        },
    ),
    (
        "movscale",
        float,
        {
            "help_string": "adjust registration matrix to scale mov",
            "argstr": "--movscale {movscale}",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
Tkregister2_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("reg_file", DatFile, {"help_string": "freesurfer-style registration file"}),
    ("fsl_file", File, {"help_string": "FSL-style registration file"}),
    ("lta_file", File, {"help_string": "LTA-style registration file"}),
]
Tkregister2_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Tkregister2(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience import DatFile, TextMatrix
    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz, Nifti1
    >>> from pydra.tasks.freesurfer.auto.utils.tkregister_2 import Tkregister2

    >>> task = Tkregister2()
    >>> task.inputs.target_image = Nifti1.mock("structural.nii")
    >>> task.inputs.moving_image = "T1.mgz"
    >>> task.inputs.fsl_in_matrix = TextMatrix.mock()
    >>> task.inputs.xfm = File.mock()
    >>> task.inputs.lta_in = File.mock()
    >>> task.inputs.reg_file = "T1_to_native.dat"
    >>> task.inputs.reg_header = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'tkregister2 --mov T1.mgz --noedit --reg T1_to_native.dat --regheader --targ structural.nii'


    >>> task = Tkregister2()
    >>> task.inputs.target_image = Nifti1.mock()
    >>> task.inputs.moving_image = "epi.nii"
    >>> task.inputs.fsl_in_matrix = TextMatrix.mock("flirt.mat")
    >>> task.inputs.xfm = File.mock()
    >>> task.inputs.lta_in = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'tkregister2 --fsl flirt.mat --mov epi.nii --noedit --reg register.dat'


    """

    input_spec = Tkregister2_input_spec
    output_spec = Tkregister2_output_spec
    executable = "tkregister2"
