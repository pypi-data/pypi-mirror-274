from fileformats.generic import File
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_lta",
        ty.Any,
        {
            "help_string": "input transform of LTA type",
            "argstr": "--inlta {in_lta}",
            "mandatory": True,
            "xor": ("in_lta", "in_fsl", "in_mni", "in_reg", "in_niftyreg", "in_itk"),
        },
    ),
    (
        "in_fsl",
        File,
        {
            "help_string": "input transform of FSL type",
            "argstr": "--infsl {in_fsl}",
            "mandatory": True,
            "xor": ("in_lta", "in_fsl", "in_mni", "in_reg", "in_niftyreg", "in_itk"),
        },
    ),
    (
        "in_mni",
        File,
        {
            "help_string": "input transform of MNI/XFM type",
            "argstr": "--inmni {in_mni}",
            "mandatory": True,
            "xor": ("in_lta", "in_fsl", "in_mni", "in_reg", "in_niftyreg", "in_itk"),
        },
    ),
    (
        "in_reg",
        File,
        {
            "help_string": "input transform of TK REG type (deprecated format)",
            "argstr": "--inreg {in_reg}",
            "mandatory": True,
            "xor": ("in_lta", "in_fsl", "in_mni", "in_reg", "in_niftyreg", "in_itk"),
        },
    ),
    (
        "in_niftyreg",
        File,
        {
            "help_string": "input transform of Nifty Reg type (inverse RAS2RAS)",
            "argstr": "--inniftyreg {in_niftyreg}",
            "mandatory": True,
            "xor": ("in_lta", "in_fsl", "in_mni", "in_reg", "in_niftyreg", "in_itk"),
        },
    ),
    (
        "in_itk",
        File,
        {
            "help_string": "input transform of ITK type",
            "argstr": "--initk {in_itk}",
            "mandatory": True,
            "xor": ("in_lta", "in_fsl", "in_mni", "in_reg", "in_niftyreg", "in_itk"),
        },
    ),
    (
        "out_lta",
        ty.Any,
        {
            "help_string": "output linear transform (LTA Freesurfer format)",
            "argstr": "--outlta {out_lta}",
        },
    ),
    (
        "out_fsl",
        ty.Any,
        {
            "help_string": "output transform in FSL format",
            "argstr": "--outfsl {out_fsl}",
        },
    ),
    (
        "out_mni",
        ty.Any,
        {
            "help_string": "output transform in MNI/XFM format",
            "argstr": "--outmni {out_mni}",
        },
    ),
    (
        "out_reg",
        ty.Any,
        {
            "help_string": "output transform in reg dat format",
            "argstr": "--outreg {out_reg}",
        },
    ),
    (
        "out_itk",
        ty.Any,
        {
            "help_string": "output transform in ITK format",
            "argstr": "--outitk {out_itk}",
        },
    ),
    ("invert", bool, {"help_string": "", "argstr": "--invert"}),
    (
        "ltavox2vox",
        bool,
        {"help_string": "", "argstr": "--ltavox2vox", "requires": ["out_lta"]},
    ),
    ("source_file", File, {"help_string": "", "argstr": "--src {source_file}"}),
    ("target_file", File, {"help_string": "", "argstr": "--trg {target_file}"}),
    ("target_conform", bool, {"help_string": "", "argstr": "--trgconform"}),
]
LTAConvert_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_lta",
        File,
        {"help_string": "output linear transform (LTA Freesurfer format)"},
    ),
    ("out_fsl", File, {"help_string": "output transform in FSL format"}),
    ("out_mni", File, {"help_string": "output transform in MNI/XFM format"}),
    ("out_reg", File, {"help_string": "output transform in reg dat format"}),
    ("out_itk", File, {"help_string": "output transform in ITK format"}),
]
LTAConvert_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class LTAConvert(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.freesurfer.auto.utils.lta_convert import LTAConvert

    """

    input_spec = LTAConvert_input_spec
    output_spec = LTAConvert_output_spec
    executable = "lta_convert"
