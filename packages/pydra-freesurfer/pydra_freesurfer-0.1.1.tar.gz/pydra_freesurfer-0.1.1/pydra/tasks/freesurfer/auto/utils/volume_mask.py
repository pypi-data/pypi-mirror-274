from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "left_whitelabel",
        int,
        {
            "help_string": "Left white matter label",
            "argstr": "--label_left_white {left_whitelabel}",
            "mandatory": True,
        },
    ),
    (
        "left_ribbonlabel",
        int,
        {
            "help_string": "Left cortical ribbon label",
            "argstr": "--label_left_ribbon {left_ribbonlabel}",
            "mandatory": True,
        },
    ),
    (
        "right_whitelabel",
        int,
        {
            "help_string": "Right white matter label",
            "argstr": "--label_right_white {right_whitelabel}",
            "mandatory": True,
        },
    ),
    (
        "right_ribbonlabel",
        int,
        {
            "help_string": "Right cortical ribbon label",
            "argstr": "--label_right_ribbon {right_ribbonlabel}",
            "mandatory": True,
        },
    ),
    (
        "lh_pial",
        Pial,
        {"help_string": "Implicit input left pial surface", "mandatory": True},
    ),
    (
        "rh_pial",
        Pial,
        {"help_string": "Implicit input right pial surface", "mandatory": True},
    ),
    (
        "lh_white",
        Pial,
        {"help_string": "Implicit input left white matter surface", "mandatory": True},
    ),
    (
        "rh_white",
        Pial,
        {"help_string": "Implicit input right white matter surface", "mandatory": True},
    ),
    (
        "aseg",
        File,
        {
            "help_string": "Implicit aseg.mgz segmentation. Specify a different aseg by using the 'in_aseg' input.",
            "xor": ["in_aseg"],
        },
    ),
    (
        "subject_id",
        ty.Any,
        {
            "help_string": "Subject being processed",
            "argstr": "{subject_id}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "in_aseg",
        File,
        {
            "help_string": "Input aseg file for VolumeMask",
            "argstr": "--aseg_name {in_aseg}",
            "xor": ["aseg"],
        },
    ),
    (
        "save_ribbon",
        bool,
        {
            "help_string": "option to save just the ribbon for the hemispheres in the format ?h.ribbon.mgz",
            "argstr": "--save_ribbon",
        },
    ),
    (
        "copy_inputs",
        bool,
        {
            "help_string": "If running as a node, set this to True.This will copy the implicit input files to the node directory."
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
VolumeMask_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_ribbon", File, {"help_string": "Output cortical ribbon mask"}),
    ("lh_ribbon", File, {"help_string": "Output left cortical ribbon mask"}),
    ("rh_ribbon", File, {"help_string": "Output right cortical ribbon mask"}),
]
VolumeMask_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class VolumeMask(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.utils.volume_mask import VolumeMask

    >>> task = VolumeMask()
    >>> task.inputs.left_whitelabel = 2
    >>> task.inputs.left_ribbonlabel = 3
    >>> task.inputs.right_whitelabel = 41
    >>> task.inputs.right_ribbonlabel = 42
    >>> task.inputs.lh_pial = Pial.mock("lh.pial")
    >>> task.inputs.rh_pial = Pial.mock("lh.pial")
    >>> task.inputs.lh_white = Pial.mock("lh.pial")
    >>> task.inputs.rh_white = Pial.mock("lh.pial")
    >>> task.inputs.aseg = File.mock()
    >>> task.inputs.subject_id = "10335"
    >>> task.inputs.in_aseg = File.mock()
    >>> task.inputs.save_ribbon = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_volmask --label_left_ribbon 3 --label_left_white 2 --label_right_ribbon 42 --label_right_white 41 --save_ribbon 10335'


    """

    input_spec = VolumeMask_input_spec
    output_spec = VolumeMask_output_spec
    executable = "mris_volmask"
