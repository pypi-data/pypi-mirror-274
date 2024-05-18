from fileformats.datascience import TextMatrix
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz, Nifti1
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        MghGz,
        {
            "help_string": "Input volume for CALabel",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -4,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Output file for CALabel",
            "argstr": "{out_file}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "transform",
        TextMatrix,
        {
            "help_string": "Input transform for CALabel",
            "argstr": "{transform}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "template",
        Nifti1,
        {
            "help_string": "Input template for CALabel",
            "argstr": "{template}",
            "mandatory": True,
            "position": -2,
        },
    ),
    ("in_vol", File, {"help_string": "set input volume", "argstr": "-r {in_vol}"}),
    (
        "intensities",
        File,
        {
            "help_string": "input label intensities file(used in longitudinal processing)",
            "argstr": "-r {intensities}",
        },
    ),
    (
        "no_big_ventricles",
        bool,
        {"help_string": "No big ventricles", "argstr": "-nobigventricles"},
    ),
    ("align", bool, {"help_string": "Align CALabel", "argstr": "-align"}),
    (
        "prior",
        float,
        {"help_string": "Prior for CALabel", "argstr": "-prior {prior:.1}"},
    ),
    (
        "relabel_unlikely",
        ty.Any,
        {
            "help_string": "Reclassify voxels at least some std devs from the mean using some size Gaussian window",
            "argstr": "-relabel_unlikely {relabel_unlikely[0]} {relabel_unlikely[1]:.1}",
        },
    ),
    (
        "label",
        File,
        {
            "help_string": "Undocumented flag. Autorecon3 uses ../label/{hemisphere}.cortex.label as input file",
            "argstr": "-l {label}",
        },
    ),
    (
        "aseg",
        File,
        {
            "help_string": "Undocumented flag. Autorecon3 uses ../mri/aseg.presurf.mgz as input file",
            "argstr": "-aseg {aseg}",
        },
    ),
    ("num_threads", int, {"help_string": "allows for specifying more threads"}),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
CALabel_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", MghGz, {"help_string": "Output volume from CALabel"})]
CALabel_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class CALabel(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz, Nifti1
    >>> from pydra.tasks.freesurfer.auto.preprocess.ca_label import CALabel

    >>> task = CALabel()
    >>> task.inputs.in_file = MghGz.mock("norm.mgz")
    >>> task.inputs.out_file = "out.mgz"
    >>> task.inputs.transform = TextMatrix.mock("trans.mat")
    >>> task.inputs.template = Nifti1.mock("Template_6.nii" # in practice use .gcs extension)
    >>> task.inputs.in_vol = File.mock()
    >>> task.inputs.intensities = File.mock()
    >>> task.inputs.label = File.mock()
    >>> task.inputs.aseg = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_ca_label norm.mgz trans.mat Template_6.nii out.mgz'


    """

    input_spec = CALabel_input_spec
    output_spec = CALabel_output_spec
    executable = "mri_ca_label"
