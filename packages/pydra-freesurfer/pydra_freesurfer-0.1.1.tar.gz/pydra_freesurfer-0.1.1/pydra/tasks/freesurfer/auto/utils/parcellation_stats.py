from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial, Thickness, White, Xfm
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
            "help_string": "Subject being processed",
            "argstr": "{subject_id}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "hemisphere",
        ty.Any,
        {
            "help_string": "Hemisphere being processed",
            "argstr": "{hemisphere}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "wm",
        MghGz,
        {
            "help_string": "Input file must be <subject_id>/mri/wm.mgz",
            "mandatory": True,
        },
    ),
    (
        "lh_white",
        White,
        {
            "help_string": "Input file must be <subject_id>/surf/lh.white",
            "mandatory": True,
        },
    ),
    (
        "rh_white",
        White,
        {
            "help_string": "Input file must be <subject_id>/surf/rh.white",
            "mandatory": True,
        },
    ),
    (
        "lh_pial",
        Pial,
        {
            "help_string": "Input file must be <subject_id>/surf/lh.pial",
            "mandatory": True,
        },
    ),
    (
        "rh_pial",
        Pial,
        {
            "help_string": "Input file must be <subject_id>/surf/rh.pial",
            "mandatory": True,
        },
    ),
    (
        "transform",
        Xfm,
        {
            "help_string": "Input file must be <subject_id>/mri/transforms/talairach.xfm",
            "mandatory": True,
        },
    ),
    (
        "thickness",
        Thickness,
        {
            "help_string": "Input file must be <subject_id>/surf/?h.thickness",
            "mandatory": True,
        },
    ),
    (
        "brainmask",
        MghGz,
        {
            "help_string": "Input file must be <subject_id>/mri/brainmask.mgz",
            "mandatory": True,
        },
    ),
    (
        "aseg",
        MghGz,
        {
            "help_string": "Input file must be <subject_id>/mri/aseg.presurf.mgz",
            "mandatory": True,
        },
    ),
    (
        "ribbon",
        MghGz,
        {
            "help_string": "Input file must be <subject_id>/mri/ribbon.mgz",
            "mandatory": True,
        },
    ),
    ("cortex_label", File, {"help_string": "implicit input file {hemi}.cortex.label"}),
    (
        "surface",
        ty.Any,
        {
            "help_string": "Input surface (e.g. 'white')",
            "argstr": "{surface}",
            "position": -1,
        },
    ),
    ("mgz", bool, {"help_string": "Look for mgz files", "argstr": "-mgz"}),
    (
        "in_cortex",
        File,
        {"help_string": "Input cortex label", "argstr": "-cortex {in_cortex}"},
    ),
    (
        "in_annotation",
        File,
        {
            "help_string": "compute properties for each label in the annotation file separately",
            "argstr": "-a {in_annotation}",
            "xor": ["in_label"],
        },
    ),
    (
        "in_label",
        File,
        {
            "help_string": "limit calculations to specified label",
            "argstr": "-l {in_label}",
            "xor": ["in_annotatoin", "out_color"],
        },
    ),
    ("tabular_output", bool, {"help_string": "Tabular output", "argstr": "-b"}),
    (
        "out_table",
        Path,
        {
            "help_string": "Table output to tablefile",
            "argstr": "-f {out_table}",
            "requires": ["tabular_output"],
            "output_file_template": '"lh.test.stats"',
        },
    ),
    (
        "out_color",
        Path,
        {
            "help_string": "Output annotation files's colortable to text file",
            "argstr": "-c {out_color}",
            "xor": ["in_label"],
            "output_file_template": '"test.ctab"',
        },
    ),
    (
        "copy_inputs",
        bool,
        {
            "help_string": "If running as a node, set this to True.This will copy the input files to the node directory."
        },
    ),
    (
        "th3",
        bool,
        {
            "help_string": "turns on new vertex-wise volume calc for mris_anat_stats",
            "argstr": "-th3",
            "requires": ["cortex_label"],
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
ParcellationStats_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ParcellationStats_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ParcellationStats(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.medimage_freesurfer import Pial, Thickness, White, Xfm
    >>> import os
    >>> from pydra.tasks.freesurfer.auto.utils.parcellation_stats import ParcellationStats

    >>> task = ParcellationStats()
    >>> task.inputs.subject_id = "10335"
    >>> task.inputs.hemisphere = "lh"
    >>> task.inputs.wm = MghGz.mock("./../mri/wm.mgz" # doctest: +SKIP)
    >>> task.inputs.lh_white = White.mock("lh.white" # doctest: +SKIP)
    >>> task.inputs.rh_white = White.mock("rh.white" # doctest: +SKIP)
    >>> task.inputs.lh_pial = Pial.mock("lh.pial" # doctest: +SKIP)
    >>> task.inputs.rh_pial = Pial.mock("lh.pial" # doctest: +SKIP)
    >>> task.inputs.transform = Xfm.mock("./../mri/transforms/talairach.xfm" # doctest: +SKIP)
    >>> task.inputs.thickness = Thickness.mock("lh.thickness" # doctest: +SKIP)
    >>> task.inputs.brainmask = MghGz.mock("./../mri/brainmask.mgz" # doctest: +SKIP)
    >>> task.inputs.aseg = MghGz.mock("./../mri/aseg.presurf.mgz" # doctest: +SKIP)
    >>> task.inputs.ribbon = MghGz.mock("./../mri/ribbon.mgz" # doctest: +SKIP)
    >>> task.inputs.cortex_label = File.mock()
    >>> task.inputs.surface = "white"
    >>> task.inputs.in_cortex = File.mock()
    >>> task.inputs.in_annotation = File.mock()
    >>> task.inputs.in_label = File.mock()
    >>> task.inputs.out_table = "lh.test.stats"
    >>> task.inputs.out_color = "test.ctab"
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_anatomical_stats -c test.ctab -f lh.test.stats 10335 lh white'


    """

    input_spec = ParcellationStats_input_spec
    output_spec = ParcellationStats_output_spec
    executable = "mris_anatomical_stats"
