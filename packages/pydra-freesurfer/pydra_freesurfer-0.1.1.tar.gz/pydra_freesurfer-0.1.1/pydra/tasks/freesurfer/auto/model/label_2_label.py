from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Pial
from fileformats.model import Stl
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "hemisphere",
        ty.Any,
        {
            "help_string": "Input hemisphere",
            "argstr": "--hemi {hemisphere}",
            "mandatory": True,
        },
    ),
    (
        "subject_id",
        ty.Any,
        {
            "help_string": "Target subject",
            "argstr": "--trgsubject {subject_id}",
            "mandatory": True,
        },
    ),
    (
        "sphere_reg",
        Pial,
        {"help_string": "Implicit input <hemisphere>.sphere.reg", "mandatory": True},
    ),
    (
        "white",
        Pial,
        {"help_string": "Implicit input <hemisphere>.white", "mandatory": True},
    ),
    (
        "source_sphere_reg",
        Pial,
        {"help_string": "Implicit input <hemisphere>.sphere.reg", "mandatory": True},
    ),
    (
        "source_white",
        Pial,
        {"help_string": "Implicit input <hemisphere>.white", "mandatory": True},
    ),
    (
        "source_label",
        Stl,
        {
            "help_string": "Source label",
            "argstr": "--srclabel {source_label}",
            "mandatory": True,
        },
    ),
    (
        "source_subject",
        ty.Any,
        {
            "help_string": "Source subject name",
            "argstr": "--srcsubject {source_subject}",
            "mandatory": True,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Target label",
            "argstr": "--trglabel {out_file}",
            "output_file_template": "{source_label}_converted",
        },
    ),
    (
        "registration_method",
        ty.Any,
        "surface",
        {
            "help_string": "Registration method",
            "argstr": "--regmethod {registration_method}",
        },
    ),
    (
        "copy_inputs",
        bool,
        {
            "help_string": "If running as a node, set this to True.This will copy the input files to the node directory."
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
Label2Label_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Label2Label_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Label2Label(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from fileformats.model import Stl
    >>> from pydra.tasks.freesurfer.auto.model.label_2_label import Label2Label

    >>> task = Label2Label()
    >>> task.inputs.hemisphere = "lh"
    >>> task.inputs.subject_id = "10335"
    >>> task.inputs.sphere_reg = Pial.mock("lh.pial")
    >>> task.inputs.white = Pial.mock("lh.pial")
    >>> task.inputs.source_sphere_reg = Pial.mock("lh.pial")
    >>> task.inputs.source_white = Pial.mock("lh.pial")
    >>> task.inputs.source_label = Stl.mock("lh-pial.stl")
    >>> task.inputs.source_subject = "fsaverage"
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_label2label --hemi lh --trglabel lh-pial_converted.stl --regmethod surface --srclabel lh-pial.stl --srcsubject fsaverage --trgsubject 10335'


    """

    input_spec = Label2Label_input_spec
    output_spec = Label2Label_output_spec
    executable = "mri_label2label"
