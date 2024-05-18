from fileformats.datascience import TextMatrix
from fileformats.medimage import MghGz, NiftiGz
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "source_file",
        MghGz,
        {
            "help_string": "This is the source of the surface values",
            "argstr": "--surfval {source_file}",
            "copyfile": False,
            "mandatory": True,
            "xor": ["mkmask"],
        },
    ),
    (
        "hemi",
        str,
        {
            "help_string": "hemisphere of data",
            "argstr": "--hemi {hemi}",
            "mandatory": True,
        },
    ),
    (
        "transformed_file",
        Path,
        {
            "help_string": "Output volume",
            "argstr": "--outvol {transformed_file}",
            "output_file_template": "{source_file}_asVol.nii",
        },
    ),
    (
        "reg_file",
        TextMatrix,
        {
            "help_string": "tkRAS-to-tkRAS matrix   (tkregister2 format)",
            "argstr": "--volreg {reg_file}",
            "mandatory": True,
            "xor": ["subject_id"],
        },
    ),
    (
        "template_file",
        NiftiGz,
        {
            "help_string": "Output template volume",
            "argstr": "--template {template_file}",
        },
    ),
    (
        "mkmask",
        bool,
        {
            "help_string": "make a mask instead of loading surface values",
            "argstr": "--mkmask",
            "xor": ["source_file"],
        },
    ),
    (
        "vertexvol_file",
        Path,
        {
            "help_string": "Path name of the vertex output volume, which is the same as output volume except that the value of each voxel is the vertex-id that is mapped to that voxel.",
            "argstr": "--vtxvol {vertexvol_file}",
            "output_file_template": "{source_file}_asVol_vertex.nii",
        },
    ),
    (
        "surf_name",
        str,
        {"help_string": "surfname (default is white)", "argstr": "--surf {surf_name}"},
    ),
    (
        "projfrac",
        float,
        {"help_string": "thickness fraction", "argstr": "--projfrac {projfrac}"},
    ),
    (
        "subjects_dir",
        str,
        {
            "help_string": "freesurfer subjects directory defaults to $SUBJECTS_DIR",
            "argstr": "--sd {subjects_dir}",
        },
    ),
    (
        "subject_id",
        str,
        {
            "help_string": "subject id",
            "argstr": "--identity {subject_id}",
            "xor": ["reg_file"],
        },
    ),
]
Surface2VolTransform_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Surface2VolTransform_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Surface2VolTransform(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.medimage import MghGz, NiftiGz
    >>> from pydra.tasks.freesurfer.auto.utils.surface_2_vol_transform import Surface2VolTransform

    >>> task = Surface2VolTransform()
    >>> task.inputs.source_file = MghGz.mock("lh.cope1.mgz")
    >>> task.inputs.hemi = "lh"
    >>> task.inputs.reg_file = TextMatrix.mock("register.mat")
    >>> task.inputs.template_file = NiftiGz.mock("cope1.nii.gz")
    >>> task.inputs.subjects_dir = "."
    >>> task.cmdline
    'mri_surf2vol --hemi lh --volreg register.mat --surfval lh.cope1.mgz --sd . --template cope1.nii.gz --outvol lh.cope1_asVol.nii --vtxvol lh.cope1_asVol_vertex.nii'


    """

    input_spec = Surface2VolTransform_input_spec
    output_spec = Surface2VolTransform_output_spec
    executable = "mri_surf2vol"
