from fileformats.datascience import DatFile
from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
from fileformats.medimage_freesurfer import Label
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "label_file",
        ty.List[Label],
        {
            "help_string": "list of label files",
            "argstr": "--label {label_file}...",
            "copyfile": False,
            "mandatory": True,
            "xor": ("label_file", "annot_file", "seg_file", "aparc_aseg"),
        },
    ),
    (
        "annot_file",
        File,
        {
            "help_string": "surface annotation file",
            "argstr": "--annot {annot_file}",
            "copyfile": False,
            "mandatory": True,
            "requires": ("subject_id", "hemi"),
            "xor": ("label_file", "annot_file", "seg_file", "aparc_aseg"),
        },
    ),
    (
        "seg_file",
        File,
        {
            "help_string": "segmentation file",
            "argstr": "--seg {seg_file}",
            "copyfile": False,
            "mandatory": True,
            "xor": ("label_file", "annot_file", "seg_file", "aparc_aseg"),
        },
    ),
    (
        "aparc_aseg",
        bool,
        {
            "help_string": "use aparc+aseg.mgz in subjectdir as seg",
            "argstr": "--aparc+aseg",
            "mandatory": True,
            "xor": ("label_file", "annot_file", "seg_file", "aparc_aseg"),
        },
    ),
    (
        "template_file",
        Nifti1,
        {
            "help_string": "output template volume",
            "argstr": "--temp {template_file}",
            "mandatory": True,
        },
    ),
    (
        "reg_file",
        DatFile,
        {
            "help_string": "tkregister style matrix VolXYZ = R*LabelXYZ",
            "argstr": "--reg {reg_file}",
            "xor": ("reg_file", "reg_header", "identity"),
        },
    ),
    (
        "reg_header",
        File,
        {
            "help_string": "label template volume",
            "argstr": "--regheader {reg_header}",
            "xor": ("reg_file", "reg_header", "identity"),
        },
    ),
    (
        "identity",
        bool,
        {
            "help_string": "set R=I",
            "argstr": "--identity",
            "xor": ("reg_file", "reg_header", "identity"),
        },
    ),
    (
        "invert_mtx",
        bool,
        {"help_string": "Invert the registration matrix", "argstr": "--invertmtx"},
    ),
    (
        "fill_thresh",
        ty.Any,
        {
            "help_string": "thresh : between 0 and 1",
            "argstr": "--fillthresh {fill_thresh}",
        },
    ),
    (
        "label_voxel_volume",
        float,
        {
            "help_string": "volume of each label point (def 1mm3)",
            "argstr": "--labvoxvol {label_voxel_volume}",
        },
    ),
    (
        "proj",
        ty.Any,
        {
            "help_string": "project along surface normal",
            "argstr": "--proj {proj[0]} {proj[1]} {proj[2]} {proj[3]}",
            "requires": ("subject_id", "hemi"),
        },
    ),
    (
        "subject_id",
        str,
        {"help_string": "subject id", "argstr": "--subject {subject_id}"},
    ),
    (
        "hemi",
        ty.Any,
        {"help_string": "hemisphere to use lh or rh", "argstr": "--hemi {hemi}"},
    ),
    (
        "surface",
        str,
        {"help_string": "use surface instead of white", "argstr": "--surf {surface}"},
    ),
    (
        "vol_label_file",
        Path,
        {
            "help_string": "output volume",
            "argstr": "--o {vol_label_file}",
            "output_file_template": '"foo_out.nii"',
        },
    ),
    (
        "label_hit_file",
        File,
        {
            "help_string": "file with each frame is nhits for a label",
            "argstr": "--hits {label_hit_file}",
        },
    ),
    (
        "map_label_stat",
        File,
        {
            "help_string": "map the label stats field into the vol",
            "argstr": "--label-stat {map_label_stat}",
        },
    ),
    (
        "native_vox2ras",
        bool,
        {
            "help_string": "use native vox2ras xform instead of  tkregister-style",
            "argstr": "--native-vox2ras",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
Label2Vol_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Label2Vol_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Label2Vol(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience import DatFile
    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from fileformats.medimage_freesurfer import Label
    >>> from pydra.tasks.freesurfer.auto.model.label_2_vol import Label2Vol

    >>> task = Label2Vol()
    >>> task.inputs.label_file = [Label.mock("c"), Label.mock("o"), Label.mock("r"), Label.mock("t"), Label.mock("e"), Label.mock("x"), Label.mock("."), Label.mock("l"), Label.mock("a"), Label.mock("b"), Label.mock("e"), Label.mock("l")]
    >>> task.inputs.annot_file = File.mock()
    >>> task.inputs.seg_file = File.mock()
    >>> task.inputs.template_file = Nifti1.mock("structural.nii")
    >>> task.inputs.reg_file = DatFile.mock("register.dat")
    >>> task.inputs.reg_header = File.mock()
    >>> task.inputs.fill_thresh = 0.5
    >>> task.inputs.vol_label_file = "foo_out.nii"
    >>> task.inputs.label_hit_file = File.mock()
    >>> task.inputs.map_label_stat = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_label2vol --fillthresh 0.5 --label cortex.label --reg register.dat --temp structural.nii --o foo_out.nii'


    """

    input_spec = Label2Vol_input_spec
    output_spec = Label2Vol_output_spec
    executable = "mri_label2vol"
