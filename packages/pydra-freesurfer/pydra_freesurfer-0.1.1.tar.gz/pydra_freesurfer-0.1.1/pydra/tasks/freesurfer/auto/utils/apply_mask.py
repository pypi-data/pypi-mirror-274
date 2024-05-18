from fileformats.generic import Directory, File
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        File,
        {
            "help_string": "input image (will be masked)",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "mask_file",
        File,
        {
            "help_string": "image defining mask space",
            "argstr": "{mask_file}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "final image to write",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": "{in_file}_masked",
        },
    ),
    (
        "xfm_file",
        File,
        {
            "help_string": "LTA-format transformation matrix to align mask with input",
            "argstr": "-xform {xfm_file}",
        },
    ),
    ("invert_xfm", bool, {"help_string": "invert transformation", "argstr": "-invert"}),
    (
        "xfm_source",
        File,
        {
            "help_string": "image defining transform source space",
            "argstr": "-lta_src {xfm_source}",
        },
    ),
    (
        "xfm_target",
        File,
        {
            "help_string": "image defining transform target space",
            "argstr": "-lta_dst {xfm_target}",
        },
    ),
    (
        "use_abs",
        bool,
        {
            "help_string": "take absolute value of mask before applying",
            "argstr": "-abs",
        },
    ),
    (
        "mask_thresh",
        float,
        {
            "help_string": "threshold mask before applying",
            "argstr": "-T {mask_thresh:.4}",
        },
    ),
    (
        "keep_mask_deletion_edits",
        bool,
        {
            "help_string": "transfer voxel-deletion edits (voxels=1) from mask to out vol",
            "argstr": "-keep_mask_deletion_edits",
        },
    ),
    (
        "transfer",
        int,
        {
            "help_string": "transfer only voxel value # from mask to out",
            "argstr": "-transfer {transfer}",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
ApplyMask_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ApplyMask_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ApplyMask(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.auto.utils.apply_mask import ApplyMask

    """

    input_spec = ApplyMask_input_spec
    output_spec = ApplyMask_output_spec
    executable = "mri_mask"
