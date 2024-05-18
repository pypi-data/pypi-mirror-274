from fileformats.generic import Directory, File
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
from pydra.engine.specs import MultiInputObj
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "surf_measure_file",
        File,
        {
            "help_string": "file necessary for surfmeas",
            "argstr": "--meas {surf_measure_file}",
            "xor": ("surf_measure", "surf_measure_file", "surf_area"),
        },
    ),
    (
        "surfreg_files",
        ty.List[File],
        {
            "help_string": "lh and rh input surface registration files",
            "argstr": "--surfreg {surfreg_files}",
            "requires": ["lh_surfreg_target", "rh_surfreg_target"],
        },
    ),
    (
        "lh_surfreg_target",
        File,
        {
            "help_string": "Implicit target surface registration file",
            "requires": ["surfreg_files"],
        },
    ),
    (
        "rh_surfreg_target",
        File,
        {
            "help_string": "Implicit target surface registration file",
            "requires": ["surfreg_files"],
        },
    ),
    (
        "subject_id",
        ty.Any,
        "subject_id",
        {
            "help_string": "subject from whom measures are calculated",
            "argstr": "--s {subject_id}",
            "xor": ("subjects", "fsgd_file", "subject_file", "subject_id"),
        },
    ),
    (
        "copy_inputs",
        bool,
        {
            "help_string": "If running as a node, set this to True this will copy some implicit inputs to the node directory."
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output filename",
            "argstr": "--out {out_file}",
            "output_file_template": '"concatenated_file.mgz"',
        },
    ),
    (
        "target",
        str,
        {
            "help_string": "target subject name",
            "argstr": "--target {target}",
            "mandatory": True,
        },
    ),
    (
        "hemi",
        ty.Any,
        {
            "help_string": "hemisphere for source and target",
            "argstr": "--hemi {hemi}",
            "mandatory": True,
        },
    ),
    (
        "surf_measure",
        str,
        {
            "help_string": "Use subject/surf/hemi.surf_measure as input",
            "argstr": "--meas {surf_measure}",
            "xor": ("surf_measure", "surf_measure_file", "surf_area"),
        },
    ),
    (
        "surf_area",
        str,
        {
            "help_string": "Extract vertex area from subject/surf/hemi.surfname to use as input.",
            "argstr": "--area {surf_area}",
            "xor": ("surf_measure", "surf_measure_file", "surf_area"),
        },
    ),
    (
        "subjects",
        list,
        {
            "help_string": "subjects from who measures are calculated",
            "argstr": "--s {subjects}...",
            "xor": ("subjects", "fsgd_file", "subject_file"),
        },
    ),
    (
        "fsgd_file",
        File,
        {
            "help_string": "specify subjects using fsgd file",
            "argstr": "--fsgd {fsgd_file}",
            "xor": ("subjects", "fsgd_file", "subject_file"),
        },
    ),
    (
        "subject_file",
        File,
        {
            "help_string": "file specifying subjects separated by white space",
            "argstr": "--f {subject_file}",
            "xor": ("subjects", "fsgd_file", "subject_file"),
        },
    ),
    (
        "source_format",
        str,
        {"help_string": "source format", "argstr": "--srcfmt {source_format}"},
    ),
    (
        "surf_dir",
        str,
        {
            "help_string": "alternative directory (instead of surf)",
            "argstr": "--surfdir {surf_dir}",
        },
    ),
    (
        "vol_measure_file",
        MultiInputObj,
        {
            "help_string": "list of volume measure and reg file tuples",
            "argstr": "--iv {vol_measure_file[0]} {vol_measure_file[1]}...",
        },
    ),
    (
        "proj_frac",
        float,
        {
            "help_string": "projection fraction for vol2surf",
            "argstr": "--projfrac {proj_frac}",
        },
    ),
    (
        "fwhm",
        float,
        {
            "help_string": "smooth by fwhm mm on the target surface",
            "argstr": "--fwhm {fwhm}",
            "xor": ["num_iters"],
        },
    ),
    (
        "num_iters",
        int,
        {
            "help_string": "niters : smooth by niters on the target surface",
            "argstr": "--niters {num_iters}",
            "xor": ["fwhm"],
        },
    ),
    (
        "fwhm_source",
        float,
        {
            "help_string": "smooth by fwhm mm on the source surface",
            "argstr": "--fwhm-src {fwhm_source}",
            "xor": ["num_iters_source"],
        },
    ),
    (
        "num_iters_source",
        int,
        {
            "help_string": "niters : smooth by niters on the source surface",
            "argstr": "--niterssrc {num_iters_source}",
            "xor": ["fwhm_source"],
        },
    ),
    (
        "smooth_cortex_only",
        bool,
        {
            "help_string": "only smooth cortex (ie, exclude medial wall)",
            "argstr": "--smooth-cortex-only",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
MRISPreprocReconAll_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
MRISPreprocReconAll_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MRISPreprocReconAll(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.engine.specs import MultiInputObj
    >>> from pydra.tasks.freesurfer.auto.model.mris_preproc_recon_all import MRISPreprocReconAll

    >>> task = MRISPreprocReconAll()
    >>> task.inputs.surf_measure_file = File.mock()
    >>> task.inputs.lh_surfreg_target = File.mock()
    >>> task.inputs.rh_surfreg_target = File.mock()
    >>> task.inputs.out_file = "concatenated_file.mgz"
    >>> task.inputs.target = "fsaverage"
    >>> task.inputs.hemi = "lh"
    >>> task.inputs.fsgd_file = File.mock()
    >>> task.inputs.subject_file = File.mock()
    >>> task.inputs.vol_measure_file = [("cont1.nii", "register.dat"),                                            ("cont1a.nii", "register.dat")]
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_preproc --hemi lh --out concatenated_file.mgz --s subject_id --target fsaverage --iv cont1.nii register.dat --iv cont1a.nii register.dat'


    """

    input_spec = MRISPreprocReconAll_input_spec
    output_spec = MRISPreprocReconAll_output_spec
    executable = "mris_preproc"
