from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
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
            "help_string": "Subject name/ID",
            "argstr": "--s {subject_id}",
            "mandatory": True,
        },
    ),
    (
        "in_labels",
        list,
        {
            "help_string": "List of input label files",
            "argstr": "--l {in_labels}...",
            "mandatory": True,
        },
    ),
    (
        "out_annot",
        ty.Any,
        {
            "help_string": "Name of the annotation to create",
            "argstr": "--a {out_annot}",
            "mandatory": True,
        },
    ),
    ("orig", Pial, {"help_string": "implicit {hemisphere}.orig", "mandatory": True}),
    (
        "keep_max",
        bool,
        {
            "help_string": "Keep label with highest 'stat' value",
            "argstr": "--maxstatwinner",
        },
    ),
    (
        "verbose_off",
        bool,
        {
            "help_string": "Turn off overlap and stat override messages",
            "argstr": "--noverbose",
        },
    ),
    (
        "color_table",
        File,
        {
            "help_string": "File that defines the structure names, their indices, and their color",
            "argstr": "--ctab {color_table}",
        },
    ),
    (
        "copy_inputs",
        bool,
        {"help_string": "copy implicit inputs and create a temp subjects_dir"},
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
Label2Annot_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", File, {"help_string": "Output annotation file"})]
Label2Annot_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Label2Annot(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.model.label_2_annot import Label2Annot

    >>> task = Label2Annot()
    >>> task.inputs.hemisphere = "lh"
    >>> task.inputs.subject_id = "10335"
    >>> task.inputs.in_labels = ["lh.aparc.label"]
    >>> task.inputs.out_annot = "test"
    >>> task.inputs.orig = Pial.mock("lh.pial")
    >>> task.inputs.color_table = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_label2annot --hemi lh --l lh.aparc.label --a test --s 10335'


    """

    input_spec = Label2Annot_input_spec
    output_spec = Label2Annot_output_spec
    executable = "mris_label2annot"
