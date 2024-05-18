from fileformats.generic import Directory, File
from fileformats.medimage import MghGz, Nifti1
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
            "help_string": "Hemisphere being processed",
            "argstr": "{hemisphere}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "subject_id",
        ty.Any,
        {
            "help_string": "Subject being processed",
            "argstr": "{subject_id}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "in_orig",
        Pial,
        {
            "help_string": "Implicit input file <hemisphere>.orig",
            "argstr": "-orig {in_orig}",
            "mandatory": True,
        },
    ),
    ("in_wm", MghGz, {"help_string": "Implicit input file wm.mgz", "mandatory": True}),
    (
        "in_filled",
        MghGz,
        {"help_string": "Implicit input file filled.mgz", "mandatory": True},
    ),
    ("in_white", File, {"help_string": "Implicit input that is sometimes used"}),
    (
        "in_label",
        Nifti1,
        {
            "help_string": "Implicit input label/<hemisphere>.aparc.annot",
            "xor": ["noaparc"],
        },
    ),
    (
        "orig_white",
        File,
        {
            "help_string": "Specify a white surface to start with",
            "argstr": "-orig_white {orig_white}",
        },
    ),
    (
        "orig_pial",
        Pial,
        {
            "help_string": "Specify a pial surface to start with",
            "argstr": "-orig_pial {orig_pial}",
            "requires": ["in_label"],
        },
    ),
    ("fix_mtl", bool, {"help_string": "Undocumented flag", "argstr": "-fix_mtl"}),
    ("no_white", bool, {"help_string": "Undocumented flag", "argstr": "-nowhite"}),
    ("white_only", bool, {"help_string": "Undocumented flag", "argstr": "-whiteonly"}),
    (
        "in_aseg",
        File,
        {"help_string": "Input segmentation file", "argstr": "-aseg {in_aseg}"},
    ),
    (
        "in_T1",
        MghGz,
        {"help_string": "Input brain or T1 file", "argstr": "-T1 {in_T1}"},
    ),
    (
        "mgz",
        bool,
        {
            "help_string": "No documentation. Direct questions to analysis-bugs@nmr.mgh.harvard.edu",
            "argstr": "-mgz",
        },
    ),
    (
        "noaparc",
        bool,
        {
            "help_string": "No documentation. Direct questions to analysis-bugs@nmr.mgh.harvard.edu",
            "argstr": "-noaparc",
            "xor": ["in_label"],
        },
    ),
    (
        "maximum",
        float,
        {
            "help_string": "No documentation (used for longitudinal processing)",
            "argstr": "-max {maximum:.1}",
        },
    ),
    (
        "longitudinal",
        bool,
        {
            "help_string": "No documentation (used for longitudinal processing)",
            "argstr": "-long",
        },
    ),
    (
        "white",
        ty.Any,
        {"help_string": "White surface name", "argstr": "-white {white}"},
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
MakeSurfaces_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_white", File, {"help_string": "Output white matter hemisphere surface"}),
    ("out_curv", File, {"help_string": "Output curv file for MakeSurfaces"}),
    ("out_area", File, {"help_string": "Output area file for MakeSurfaces"}),
    ("out_cortex", File, {"help_string": "Output cortex file for MakeSurfaces"}),
    ("out_pial", File, {"help_string": "Output pial surface for MakeSurfaces"}),
    ("out_thickness", File, {"help_string": "Output thickness file for MakeSurfaces"}),
]
MakeSurfaces_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MakeSurfaces(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz, Nifti1
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.utils.make_surfaces import MakeSurfaces

    >>> task = MakeSurfaces()
    >>> task.inputs.hemisphere = "lh"
    >>> task.inputs.subject_id = "10335"
    >>> task.inputs.in_orig = Pial.mock("lh.pial")
    >>> task.inputs.in_wm = MghGz.mock("wm.mgz")
    >>> task.inputs.in_filled = MghGz.mock("norm.mgz")
    >>> task.inputs.in_white = File.mock()
    >>> task.inputs.in_label = Nifti1.mock("aparc+aseg.nii")
    >>> task.inputs.orig_white = File.mock()
    >>> task.inputs.orig_pial = Pial.mock("lh.pial")
    >>> task.inputs.in_aseg = File.mock()
    >>> task.inputs.in_T1 = MghGz.mock("T1.mgz")
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_make_surfaces -T1 T1.mgz -orig pial -orig_pial pial 10335 lh'


    """

    input_spec = MakeSurfaces_input_spec
    output_spec = MakeSurfaces_output_spec
    executable = "mris_make_surfaces"
