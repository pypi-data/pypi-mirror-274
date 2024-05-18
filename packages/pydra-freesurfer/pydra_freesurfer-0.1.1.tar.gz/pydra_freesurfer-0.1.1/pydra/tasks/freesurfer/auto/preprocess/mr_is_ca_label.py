from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
from fileformats.medimage_freesurfer import Pial
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "subject_id",
        ty.Any,
        {
            "help_string": "Subject name or ID",
            "argstr": "{subject_id}",
            "mandatory": True,
            "position": -5,
        },
    ),
    (
        "hemisphere",
        ty.Any,
        {
            "help_string": "Hemisphere ('lh' or 'rh')",
            "argstr": "{hemisphere}",
            "mandatory": True,
            "position": -4,
        },
    ),
    (
        "canonsurf",
        Pial,
        {
            "help_string": "Input canonical surface file",
            "argstr": "{canonsurf}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "classifier",
        Nifti1,
        {
            "help_string": "Classifier array input file",
            "argstr": "{classifier}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "smoothwm",
        Pial,
        {"help_string": "implicit input {hemisphere}.smoothwm", "mandatory": True},
    ),
    (
        "curv",
        Pial,
        {"help_string": "implicit input {hemisphere}.curv", "mandatory": True},
    ),
    (
        "sulc",
        Pial,
        {"help_string": "implicit input {hemisphere}.sulc", "mandatory": True},
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Annotated surface output file",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": "{hemisphere}.aparc.annot",
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
    ("seed", int, {"help_string": "", "argstr": "-seed {seed}"}),
    (
        "copy_inputs",
        bool,
        {
            "help_string": "Copies implicit inputs to node directory and creates a temp subjects_directory. Use this when running as a node"
        },
    ),
    ("num_threads", int, {"help_string": "allows for specifying more threads"}),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
MRIsCALabel_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
MRIsCALabel_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MRIsCALabel(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.preprocess.mr_is_ca_label import MRIsCALabel

    >>> task = MRIsCALabel()
    >>> task.inputs.subject_id = "test"
    >>> task.inputs.hemisphere = "lh"
    >>> task.inputs.canonsurf = Pial.mock("lh.pial")
    >>> task.inputs.classifier = Nifti1.mock("im1.nii" # in pracice, use .gcs extension)
    >>> task.inputs.smoothwm = Pial.mock("lh.pial")
    >>> task.inputs.curv = Pial.mock("lh.pial")
    >>> task.inputs.sulc = Pial.mock("lh.pial")
    >>> task.inputs.label = File.mock()
    >>> task.inputs.aseg = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_ca_label test lh lh.pial im1.nii lh.aparc.annot'


    """

    input_spec = MRIsCALabel_input_spec
    output_spec = MRIsCALabel_output_spec
    executable = "mris_ca_label"
