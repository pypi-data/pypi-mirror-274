from fileformats.datascience import DatFile
from fileformats.generic import Directory, File
from fileformats.medimage import NiftiGz
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "source_file",
        NiftiGz,
        {
            "help_string": "volume to sample values from",
            "argstr": "--mov {source_file}",
            "mandatory": True,
        },
    ),
    (
        "reference_file",
        File,
        {
            "help_string": "reference volume (default is orig.mgz)",
            "argstr": "--ref {reference_file}",
        },
    ),
    (
        "hemi",
        ty.Any,
        {
            "help_string": "target hemisphere",
            "argstr": "--hemi {hemi}",
            "mandatory": True,
        },
    ),
    (
        "surface",
        ty.Any,
        {
            "help_string": "target surface (default is white)",
            "argstr": "--surf {surface}",
        },
    ),
    (
        "reg_file",
        DatFile,
        {
            "help_string": "source-to-reference registration file",
            "argstr": "--reg {reg_file}",
            "mandatory": True,
            "xor": ["reg_file", "reg_header", "mni152reg"],
        },
    ),
    (
        "reg_header",
        bool,
        {
            "help_string": "register based on header geometry",
            "argstr": "--regheader {reg_header}",
            "mandatory": True,
            "requires": ["subject_id"],
            "xor": ["reg_file", "reg_header", "mni152reg"],
        },
    ),
    (
        "mni152reg",
        bool,
        {
            "help_string": "source volume is in MNI152 space",
            "argstr": "--mni152reg",
            "mandatory": True,
            "xor": ["reg_file", "reg_header", "mni152reg"],
        },
    ),
    (
        "apply_rot",
        ty.Any,
        {
            "help_string": "rotation angles (in degrees) to apply to reg matrix",
            "argstr": "--rot {apply_rot[0]:.3} {apply_rot[1]:.3} {apply_rot[2]:.3}",
        },
    ),
    (
        "apply_trans",
        ty.Any,
        {
            "help_string": "translation (in mm) to apply to reg matrix",
            "argstr": "--trans {apply_trans[0]:.3} {apply_trans[1]:.3} {apply_trans[2]:.3}",
        },
    ),
    (
        "override_reg_subj",
        bool,
        {
            "help_string": "override the subject in the reg file header",
            "argstr": "--srcsubject {override_reg_subj}",
            "requires": ["subject_id"],
        },
    ),
    (
        "sampling_method",
        ty.Any,
        {
            "help_string": "how to sample -- at a point or at the max or average over a range",
            "argstr": "{sampling_method}",
            "mandatory": True,
            "requires": ["sampling_range", "sampling_units"],
            "xor": ["projection_stem"],
        },
    ),
    (
        "sampling_range",
        ty.Any,
        {"help_string": "sampling range - a point or a tuple of (min, max, step)"},
    ),
    (
        "sampling_units",
        ty.Any,
        {"help_string": "sampling range type -- either 'mm' or 'frac'"},
    ),
    (
        "projection_stem",
        ty.Any,
        {
            "help_string": "stem for precomputed linear estimates and volume fractions",
            "mandatory": True,
            "xor": ["sampling_method"],
        },
    ),
    (
        "smooth_vol",
        float,
        {
            "help_string": "smooth input volume (mm fwhm)",
            "argstr": "--fwhm {smooth_vol:.3}",
        },
    ),
    (
        "smooth_surf",
        float,
        {
            "help_string": "smooth output surface (mm fwhm)",
            "argstr": "--surf-fwhm {smooth_surf:.3}",
        },
    ),
    (
        "interp_method",
        ty.Any,
        {"help_string": "interpolation method", "argstr": "--interp {interp_method}"},
    ),
    (
        "cortex_mask",
        bool,
        {
            "help_string": "mask the target surface with hemi.cortex.label",
            "argstr": "--cortex",
            "xor": ["mask_label"],
        },
    ),
    (
        "mask_label",
        File,
        {
            "help_string": "label file to mask output with",
            "argstr": "--mask {mask_label}",
            "xor": ["cortex_mask"],
        },
    ),
    (
        "float2int_method",
        ty.Any,
        {
            "help_string": "method to convert reg matrix values (default is round)",
            "argstr": "--float2int {float2int_method}",
        },
    ),
    (
        "fix_tk_reg",
        bool,
        {"help_string": "make reg matrix round-compatible", "argstr": "--fixtkreg"},
    ),
    ("subject_id", ty.Any, {"help_string": "subject id"}),
    (
        "target_subject",
        ty.Any,
        {
            "help_string": "sample to surface of different subject than source",
            "argstr": "--trgsubject {target_subject}",
        },
    ),
    (
        "surf_reg",
        ty.Any,
        {
            "help_string": "use surface registration to target subject",
            "argstr": "--surfreg {surf_reg}",
            "requires": ["target_subject"],
        },
    ),
    (
        "ico_order",
        int,
        {
            "help_string": "icosahedron order when target_subject is 'ico'",
            "argstr": "--icoorder {ico_order}",
            "requires": ["target_subject"],
        },
    ),
    (
        "reshape",
        bool,
        {
            "help_string": "reshape surface vector to fit in non-mgh format",
            "argstr": "--reshape",
            "xor": ["no_reshape"],
        },
    ),
    (
        "no_reshape",
        bool,
        {
            "help_string": "do not reshape surface vector (default)",
            "argstr": "--noreshape",
            "xor": ["reshape"],
        },
    ),
    (
        "reshape_slices",
        int,
        {
            "help_string": "number of 'slices' for reshaping",
            "argstr": "--rf {reshape_slices}",
        },
    ),
    (
        "scale_input",
        float,
        {
            "help_string": "multiple all intensities by scale factor",
            "argstr": "--scale {scale_input:.3}",
        },
    ),
    (
        "frame",
        int,
        {"help_string": "save only one frame (0-based)", "argstr": "--frame {frame}"},
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "surface file to write",
            "argstr": "--o {out_file}",
            "output_file_template": "out_file",
        },
    ),
    (
        "out_type",
        ty.Any,
        {"help_string": "output file type", "argstr": "--out_type {out_type}"},
    ),
    (
        "hits_file",
        ty.Any,
        {
            "help_string": "save image with number of hits at each voxel",
            "argstr": "--srchit {hits_file}",
        },
    ),
    ("hits_type", ty.Any, {"help_string": "hits file type", "argstr": "--srchit_type"}),
    (
        "vox_file",
        ty.Any,
        {
            "help_string": "text file with the number of voxels intersecting the surface",
            "argstr": "--nvox {vox_file}",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
SampleToSurface_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("hits_file", File, {"help_string": "image with number of hits at each voxel"}),
    (
        "vox_file",
        File,
        {"help_string": "text file with the number of voxels intersecting the surface"},
    ),
]
SampleToSurface_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SampleToSurface(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience import DatFile
    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import NiftiGz
    >>> from pydra.tasks.freesurfer.auto.utils.sample_to_surface import SampleToSurface

    >>> task = SampleToSurface()
    >>> task.inputs.source_file = NiftiGz.mock("cope1.nii.gz")
    >>> task.inputs.reference_file = File.mock()
    >>> task.inputs.hemi = "lh"
    >>> task.inputs.reg_file = DatFile.mock("register.dat")
    >>> task.inputs.sampling_method = "average"
    >>> task.inputs.sampling_range = 1
    >>> task.inputs.sampling_units = "frac"
    >>> task.inputs.mask_label = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_vol2surf --hemi lh --o ...lh.cope1.mgz --reg register.dat --projfrac-avg 1.000 --mov cope1.nii.gz'


    """

    input_spec = SampleToSurface_input_spec
    output_spec = SampleToSurface_output_spec
    executable = "mri_vol2surf"
