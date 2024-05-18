from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
from pydra.engine.specs import MultiInputObj
import typing as ty


logger = logging.getLogger(__name__)


def subject_id_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["subject_id"]


input_fields = [
    (
        "subject_id",
        str,
        "recon_all",
        {"help_string": "subject name", "argstr": "-subjid {subject_id}"},
    ),
    (
        "directive",
        ty.Any,
        "all",
        {"help_string": "process directive", "argstr": "-{directive}", "position": 0},
    ),
    (
        "hemi",
        ty.Any,
        {"help_string": "hemisphere to process", "argstr": "-hemi {hemi}"},
    ),
    (
        "T1_files",
        ty.List[Nifti1],
        {"help_string": "name of T1 file to process", "argstr": "-i {T1_files}..."},
    ),
    (
        "T2_file",
        File,
        {
            "help_string": "Convert T2 image to orig directory",
            "argstr": "-T2 {T2_file}",
        },
    ),
    (
        "FLAIR_file",
        File,
        {
            "help_string": "Convert FLAIR image to orig directory",
            "argstr": "-FLAIR {FLAIR_file}",
        },
    ),
    (
        "use_T2",
        bool,
        {
            "help_string": "Use T2 image to refine the pial surface",
            "argstr": "-T2pial",
            "xor": ["use_FLAIR"],
        },
    ),
    (
        "use_FLAIR",
        bool,
        {
            "help_string": "Use FLAIR image to refine the pial surface",
            "argstr": "-FLAIRpial",
            "xor": ["use_T2"],
        },
    ),
    (
        "openmp",
        int,
        {
            "help_string": "Number of processors to use in parallel",
            "argstr": "-openmp {openmp}",
        },
    ),
    (
        "parallel",
        bool,
        {"help_string": "Enable parallel execution", "argstr": "-parallel"},
    ),
    (
        "hires",
        bool,
        {
            "help_string": "Conform to minimum voxel size (for voxels < 1mm)",
            "argstr": "-hires",
        },
    ),
    (
        "mprage",
        bool,
        {
            "help_string": "Assume scan parameters are MGH MP-RAGE protocol, which produces darker gray matter",
            "argstr": "-mprage",
        },
    ),
    (
        "big_ventricles",
        bool,
        {
            "help_string": "For use in subjects with enlarged ventricles",
            "argstr": "-bigventricles",
        },
    ),
    (
        "brainstem",
        bool,
        {
            "help_string": "Segment brainstem structures",
            "argstr": "-brainstem-structures",
        },
    ),
    (
        "hippocampal_subfields_T1",
        bool,
        {
            "help_string": "segment hippocampal subfields using input T1 scan",
            "argstr": "-hippocampal-subfields-T1",
        },
    ),
    (
        "hippocampal_subfields_T2",
        ty.Any,
        {
            "help_string": "segment hippocampal subfields using T2 scan, identified by ID (may be combined with hippocampal_subfields_T1)",
            "argstr": "-hippocampal-subfields-T2 {hippocampal_subfields_T2[0]} {hippocampal_subfields_T2[1]}",
        },
    ),
    (
        "expert",
        File,
        {
            "help_string": "Set parameters using expert file",
            "argstr": "-expert {expert}",
        },
    ),
    (
        "xopts",
        ty.Any,
        {
            "help_string": "Use, delete or overwrite existing expert options file",
            "argstr": "-xopts-{xopts}",
        },
    ),
    (
        "subjects_dir",
        Path,
        {
            "help_string": "path to subjects directory",
            "argstr": "-sd {subjects_dir}",
            "output_file_template": '"."',
        },
    ),
    (
        "flags",
        MultiInputObj,
        {"help_string": "additional parameters", "argstr": "{flags}"},
    ),
    (
        "talairach",
        str,
        {"help_string": "Flags to pass to talairach commands", "xor": ["expert"]},
    ),
    (
        "mri_normalize",
        str,
        {"help_string": "Flags to pass to mri_normalize commands", "xor": ["expert"]},
    ),
    (
        "mri_watershed",
        str,
        {"help_string": "Flags to pass to mri_watershed commands", "xor": ["expert"]},
    ),
    (
        "mri_em_register",
        str,
        {"help_string": "Flags to pass to mri_em_register commands", "xor": ["expert"]},
    ),
    (
        "mri_ca_normalize",
        str,
        {
            "help_string": "Flags to pass to mri_ca_normalize commands",
            "xor": ["expert"],
        },
    ),
    (
        "mri_ca_register",
        str,
        {"help_string": "Flags to pass to mri_ca_register commands", "xor": ["expert"]},
    ),
    (
        "mri_remove_neck",
        str,
        {"help_string": "Flags to pass to mri_remove_neck commands", "xor": ["expert"]},
    ),
    (
        "mri_ca_label",
        str,
        {"help_string": "Flags to pass to mri_ca_label commands", "xor": ["expert"]},
    ),
    (
        "mri_segstats",
        str,
        {"help_string": "Flags to pass to mri_segstats commands", "xor": ["expert"]},
    ),
    (
        "mri_mask",
        str,
        {"help_string": "Flags to pass to mri_mask commands", "xor": ["expert"]},
    ),
    (
        "mri_segment",
        str,
        {"help_string": "Flags to pass to mri_segment commands", "xor": ["expert"]},
    ),
    (
        "mri_edit_wm_with_aseg",
        str,
        {
            "help_string": "Flags to pass to mri_edit_wm_with_aseg commands",
            "xor": ["expert"],
        },
    ),
    (
        "mri_pretess",
        str,
        {"help_string": "Flags to pass to mri_pretess commands", "xor": ["expert"]},
    ),
    (
        "mri_fill",
        str,
        {"help_string": "Flags to pass to mri_fill commands", "xor": ["expert"]},
    ),
    (
        "mri_tessellate",
        str,
        {"help_string": "Flags to pass to mri_tessellate commands", "xor": ["expert"]},
    ),
    (
        "mris_smooth",
        str,
        {"help_string": "Flags to pass to mri_smooth commands", "xor": ["expert"]},
    ),
    (
        "mris_inflate",
        str,
        {"help_string": "Flags to pass to mri_inflate commands", "xor": ["expert"]},
    ),
    (
        "mris_sphere",
        str,
        {"help_string": "Flags to pass to mris_sphere commands", "xor": ["expert"]},
    ),
    (
        "mris_fix_topology",
        str,
        {
            "help_string": "Flags to pass to mris_fix_topology commands",
            "xor": ["expert"],
        },
    ),
    (
        "mris_make_surfaces",
        str,
        {
            "help_string": "Flags to pass to mris_make_surfaces commands",
            "xor": ["expert"],
        },
    ),
    (
        "mris_surf2vol",
        str,
        {"help_string": "Flags to pass to mris_surf2vol commands", "xor": ["expert"]},
    ),
    (
        "mris_register",
        str,
        {"help_string": "Flags to pass to mris_register commands", "xor": ["expert"]},
    ),
    (
        "mrisp_paint",
        str,
        {"help_string": "Flags to pass to mrisp_paint commands", "xor": ["expert"]},
    ),
    (
        "mris_ca_label",
        str,
        {"help_string": "Flags to pass to mris_ca_label commands", "xor": ["expert"]},
    ),
    (
        "mris_anatomical_stats",
        str,
        {
            "help_string": "Flags to pass to mris_anatomical_stats commands",
            "xor": ["expert"],
        },
    ),
    (
        "mri_aparc2aseg",
        str,
        {"help_string": "Flags to pass to mri_aparc2aseg commands", "xor": ["expert"]},
    ),
]
ReconAll_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "subject_id",
        str,
        {
            "help_string": "Subject name for whom to retrieve data",
            "callable": "subject_id_callable",
        },
    ),
    ("T1", File, {"help_string": "Intensity normalized whole-head volume"}),
    (
        "aseg",
        File,
        {"help_string": "Volumetric map of regions from automatic segmentation"},
    ),
    ("brain", File, {"help_string": "Intensity normalized brain-only volume"}),
    ("brainmask", File, {"help_string": "Skull-stripped (brain-only) volume"}),
    ("filled", File, {"help_string": "Subcortical mass volume"}),
    ("norm", File, {"help_string": "Normalized skull-stripped volume"}),
    ("nu", File, {"help_string": "Non-uniformity corrected whole-head volume"}),
    ("orig", File, {"help_string": "Base image conformed to Freesurfer space"}),
    ("rawavg", File, {"help_string": "Volume formed by averaging input images"}),
    ("ribbon", ty.List[File], {"help_string": "Volumetric maps of cortical ribbons"}),
    ("wm", File, {"help_string": "Segmented white-matter volume"}),
    (
        "wmparc",
        File,
        {"help_string": "Aparc parcellation projected into subcortical white matter"},
    ),
    ("curv", ty.List[File], {"help_string": "Maps of surface curvature"}),
    (
        "avg_curv",
        ty.List[File],
        {"help_string": "Average atlas curvature, sampled to subject"},
    ),
    ("inflated", ty.List[File], {"help_string": "Inflated surface meshes"}),
    ("pial", ty.List[File], {"help_string": "Gray matter/pia mater surface meshes"}),
    (
        "area_pial",
        ty.List[File],
        {
            "help_string": "Mean area of triangles each vertex on the pial surface is associated with"
        },
    ),
    ("curv_pial", ty.List[File], {"help_string": "Curvature of pial surface"}),
    ("smoothwm", ty.List[File], {"help_string": "Smoothed original surface meshes"}),
    ("sphere", ty.List[File], {"help_string": "Spherical surface meshes"}),
    ("sulc", ty.List[File], {"help_string": "Surface maps of sulcal depth"}),
    ("thickness", ty.List[File], {"help_string": "Surface maps of cortical thickness"}),
    ("volume", ty.List[File], {"help_string": "Surface maps of cortical volume"}),
    ("white", ty.List[File], {"help_string": "White/gray matter surface meshes"}),
    (
        "jacobian_white",
        ty.List[File],
        {"help_string": "Distortion required to register to spherical atlas"},
    ),
    ("graymid", ty.List[File], {"help_string": "Graymid/midthickness surface meshes"}),
    ("label", ty.List[File], {"help_string": "Volume and surface label files"}),
    ("annot", ty.List[File], {"help_string": "Surface annotation files"}),
    (
        "aparc_aseg",
        ty.List[File],
        {"help_string": "Aparc parcellation projected into aseg volume"},
    ),
    ("sphere_reg", ty.List[File], {"help_string": "Spherical registration file"}),
    (
        "aseg_stats",
        ty.List[File],
        {"help_string": "Automated segmentation statistics file"},
    ),
    (
        "wmparc_stats",
        ty.List[File],
        {"help_string": "White matter parcellation statistics file"},
    ),
    (
        "aparc_stats",
        ty.List[File],
        {"help_string": "Aparc parcellation statistics files"},
    ),
    ("BA_stats", ty.List[File], {"help_string": "Brodmann Area statistics files"}),
    (
        "aparc_a2009s_stats",
        ty.List[File],
        {"help_string": "Aparc a2009s parcellation statistics files"},
    ),
    ("curv_stats", ty.List[File], {"help_string": "Curvature statistics files"}),
    (
        "entorhinal_exvivo_stats",
        ty.List[File],
        {"help_string": "Entorhinal exvivo statistics files"},
    ),
]
ReconAll_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ReconAll(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.engine.specs import MultiInputObj
    >>> from pydra.tasks.freesurfer.auto.preprocess.recon_all import ReconAll

    >>> task = ReconAll()
    >>> task.inputs.subject_id = "foo"
    >>> task.inputs.directive = "all"
    >>> task.inputs.T1_files = [Nifti1.mock("s"), Nifti1.mock("t"), Nifti1.mock("r"), Nifti1.mock("u"), Nifti1.mock("c"), Nifti1.mock("t"), Nifti1.mock("u"), Nifti1.mock("r"), Nifti1.mock("a"), Nifti1.mock("l"), Nifti1.mock("."), Nifti1.mock("n"), Nifti1.mock("i"), Nifti1.mock("i")]
    >>> task.inputs.T2_file = File.mock()
    >>> task.inputs.FLAIR_file = File.mock()
    >>> task.inputs.expert = File.mock()
    >>> task.inputs.subjects_dir = "."
    >>> task.inputs.flags = ["-cw256", "-qcache"]
    >>> task.cmdline
    'recon-all -all -i structural.nii -cw256 -qcache -subjid foo -sd .'


    >>> task = ReconAll()
    >>> task.inputs.hemi = "lh"
    >>> task.inputs.T2_file = File.mock()
    >>> task.inputs.FLAIR_file = File.mock()
    >>> task.inputs.expert = File.mock()
    >>> task.inputs.flags = []
    >>> task.cmdline
    'recon-all -all -i structural.nii -hemi lh -subjid foo -sd .'


    >>> task = ReconAll()
    >>> task.inputs.directive = "autorecon-hemi"
    >>> task.inputs.T2_file = File.mock()
    >>> task.inputs.FLAIR_file = File.mock()
    >>> task.inputs.expert = File.mock()
    >>> task.cmdline
    'recon-all -autorecon-hemi lh -i structural.nii -subjid foo -sd .'


    >>> task = ReconAll()
    >>> task.inputs.subject_id = "foo"
    >>> task.inputs.directive = "all"
    >>> task.inputs.T1_files = [Nifti1.mock("s"), Nifti1.mock("t"), Nifti1.mock("r"), Nifti1.mock("u"), Nifti1.mock("c"), Nifti1.mock("t"), Nifti1.mock("u"), Nifti1.mock("r"), Nifti1.mock("a"), Nifti1.mock("l"), Nifti1.mock("."), Nifti1.mock("n"), Nifti1.mock("i"), Nifti1.mock("i")]
    >>> task.inputs.T2_file = File.mock()
    >>> task.inputs.FLAIR_file = File.mock()
    >>> task.inputs.hippocampal_subfields_T1 = False
    >>> task.inputs.hippocampal_subfields_T2 = ("structural.nii", "test")
    >>> task.inputs.expert = File.mock()
    >>> task.inputs.subjects_dir = "."
    >>> task.cmdline
    'recon-all -all -i structural.nii -hippocampal-subfields-T2 structural.nii test -subjid foo -sd .'


    """

    input_spec = ReconAll_input_spec
    output_spec = ReconAll_output_spec
    executable = "recon-all"
