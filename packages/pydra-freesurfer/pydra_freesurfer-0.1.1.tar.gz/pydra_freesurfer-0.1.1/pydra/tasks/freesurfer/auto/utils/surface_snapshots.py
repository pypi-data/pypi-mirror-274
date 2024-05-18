from fileformats.generic import Directory, File
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
            "help_string": "subject to visualize",
            "argstr": "{subject_id}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "hemi",
        ty.Any,
        {
            "help_string": "hemisphere to visualize",
            "argstr": "{hemi}",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "surface",
        ty.Any,
        {
            "help_string": "surface to visualize",
            "argstr": "{surface}",
            "mandatory": True,
            "position": 3,
        },
    ),
    (
        "show_curv",
        bool,
        {"help_string": "show curvature", "argstr": "-curv", "xor": ["show_gray_curv"]},
    ),
    (
        "show_gray_curv",
        bool,
        {
            "help_string": "show curvature in gray",
            "argstr": "-gray",
            "xor": ["show_curv"],
        },
    ),
    (
        "overlay",
        File,
        {
            "help_string": "load an overlay volume/surface",
            "argstr": "-overlay {overlay}",
            "requires": ["overlay_range"],
        },
    ),
    (
        "overlay_reg",
        File,
        {
            "help_string": "registration matrix file to register overlay to surface",
            "argstr": "-overlay-reg {overlay_reg}",
            "xor": ["overlay_reg", "identity_reg", "mni152_reg"],
        },
    ),
    (
        "identity_reg",
        bool,
        {
            "help_string": "use the identity matrix to register the overlay to the surface",
            "argstr": "-overlay-reg-identity",
            "xor": ["overlay_reg", "identity_reg", "mni152_reg"],
        },
    ),
    (
        "mni152_reg",
        bool,
        {
            "help_string": "use to display a volume in MNI152 space on the average subject",
            "argstr": "-mni152reg",
            "xor": ["overlay_reg", "identity_reg", "mni152_reg"],
        },
    ),
    (
        "overlay_range",
        ty.Any,
        {
            "help_string": "overlay range--either min, (min, max) or (min, mid, max)",
            "argstr": "{overlay_range}",
        },
    ),
    (
        "overlay_range_offset",
        float,
        {
            "help_string": "overlay range will be symmetric around offset value",
            "argstr": "-foffset {overlay_range_offset:.3}",
        },
    ),
    (
        "truncate_overlay",
        bool,
        {"help_string": "truncate the overlay display", "argstr": "-truncphaseflag 1"},
    ),
    (
        "reverse_overlay",
        bool,
        {"help_string": "reverse the overlay display", "argstr": "-revphaseflag 1"},
    ),
    (
        "invert_overlay",
        bool,
        {"help_string": "invert the overlay display", "argstr": "-invphaseflag 1"},
    ),
    (
        "demean_overlay",
        bool,
        {"help_string": "remove mean from overlay", "argstr": "-zm"},
    ),
    (
        "annot_file",
        File,
        {
            "help_string": "path to annotation file to display",
            "argstr": "-annotation {annot_file}",
            "xor": ["annot_name"],
        },
    ),
    (
        "annot_name",
        ty.Any,
        {
            "help_string": "name of annotation to display (must be in $subject/label directory",
            "argstr": "-annotation {annot_name}",
            "xor": ["annot_file"],
        },
    ),
    (
        "label_file",
        File,
        {
            "help_string": "path to label file to display",
            "argstr": "-label {label_file}",
            "xor": ["label_name"],
        },
    ),
    (
        "label_name",
        ty.Any,
        {
            "help_string": "name of label to display (must be in $subject/label directory",
            "argstr": "-label {label_name}",
            "xor": ["label_file"],
        },
    ),
    (
        "colortable",
        File,
        {"help_string": "load colortable file", "argstr": "-colortable {colortable}"},
    ),
    (
        "label_under",
        bool,
        {
            "help_string": "draw label/annotation under overlay",
            "argstr": "-labels-under",
        },
    ),
    (
        "label_outline",
        bool,
        {"help_string": "draw label/annotation as outline", "argstr": "-label-outline"},
    ),
    (
        "patch_file",
        File,
        {"help_string": "load a patch", "argstr": "-patch {patch_file}"},
    ),
    (
        "orig_suffix",
        ty.Any,
        {
            "help_string": "set the orig surface suffix string",
            "argstr": "-orig {orig_suffix}",
        },
    ),
    (
        "sphere_suffix",
        ty.Any,
        {
            "help_string": "set the sphere.reg suffix string",
            "argstr": "-sphere {sphere_suffix}",
        },
    ),
    (
        "show_color_scale",
        bool,
        {"help_string": "display the color scale bar", "argstr": "-colscalebarflag 1"},
    ),
    (
        "show_color_text",
        bool,
        {
            "help_string": "display text in the color scale bar",
            "argstr": "-colscaletext 1",
        },
    ),
    ("six_images", bool, {"help_string": "also take anterior and posterior snapshots"}),
    (
        "screenshot_stem",
        ty.Any,
        {"help_string": "stem to use for screenshot file names"},
    ),
    (
        "stem_template_args",
        list,
        {
            "help_string": "input names to use as arguments for a string-formated stem template",
            "requires": ["screenshot_stem"],
        },
    ),
    (
        "tcl_script",
        Path,
        {"help_string": "override default screenshot script", "argstr": "{tcl_script}"},
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
SurfaceSnapshots_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "snapshots",
        ty.List[File],
        {"help_string": "tiff images of the surface from different perspectives"},
    )
]
SurfaceSnapshots_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SurfaceSnapshots(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.auto.utils.surface_snapshots import SurfaceSnapshots

    """

    input_spec = SurfaceSnapshots_input_spec
    output_spec = SurfaceSnapshots_output_spec
    executable = "tksurfer"
