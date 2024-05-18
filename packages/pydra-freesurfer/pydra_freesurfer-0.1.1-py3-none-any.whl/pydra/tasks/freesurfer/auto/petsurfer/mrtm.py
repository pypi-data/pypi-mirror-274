from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
from pydra.engine.specs import MultiOutputType
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "mrtm1",
        ty.Any,
        {
            "help_string": "RefTac TimeSec : perform MRTM1 kinetic modeling",
            "argstr": "--mrtm1 {mrtm1[0]} {mrtm1[1]}",
            "mandatory": True,
        },
    ),
    (
        "glm_dir",
        str,
        {
            "help_string": "save outputs to dir",
            "argstr": "--glmdir {glm_dir}",
            "output_file_template": '"mrtm"',
        },
    ),
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input 4D file",
            "argstr": "--y {in_file}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "fsgd",
        ty.Any,
        {
            "help_string": "freesurfer descriptor file",
            "argstr": "--fsgd {fsgd[0]} {fsgd[1]}",
            "xor": ("fsgd", "design", "one_sample"),
        },
    ),
    (
        "design",
        File,
        {
            "help_string": "design matrix file",
            "argstr": "--X {design}",
            "xor": ("fsgd", "design", "one_sample"),
        },
    ),
    (
        "contrast",
        ty.List[File],
        {"help_string": "contrast file", "argstr": "--C {contrast}..."},
    ),
    (
        "one_sample",
        bool,
        {
            "help_string": "construct X and C as a one-sample group mean",
            "argstr": "--osgm",
            "xor": ("one_sample", "fsgd", "design", "contrast"),
        },
    ),
    (
        "no_contrast_ok",
        bool,
        {
            "help_string": "do not fail if no contrasts specified",
            "argstr": "--no-contrasts-ok",
        },
    ),
    (
        "per_voxel_reg",
        ty.List[File],
        {"help_string": "per-voxel regressors", "argstr": "--pvr {per_voxel_reg}..."},
    ),
    (
        "self_reg",
        ty.Any,
        {
            "help_string": "self-regressor from index col row slice",
            "argstr": "--selfreg {self_reg[0]} {self_reg[1]} {self_reg[2]}",
        },
    ),
    (
        "weighted_ls",
        File,
        {
            "help_string": "weighted least squares",
            "argstr": "--wls {weighted_ls}",
            "xor": ("weight_file", "weight_inv", "weight_sqrt"),
        },
    ),
    (
        "fixed_fx_var",
        File,
        {
            "help_string": "for fixed effects analysis",
            "argstr": "--yffxvar {fixed_fx_var}",
        },
    ),
    (
        "fixed_fx_dof",
        int,
        {
            "help_string": "dof for fixed effects analysis",
            "argstr": "--ffxdof {fixed_fx_dof}",
            "xor": ["fixed_fx_dof_file"],
        },
    ),
    (
        "fixed_fx_dof_file",
        File,
        {
            "help_string": "text file with dof for fixed effects analysis",
            "argstr": "--ffxdofdat {fixed_fx_dof_file}",
            "xor": ["fixed_fx_dof"],
        },
    ),
    (
        "weight_file",
        File,
        {"help_string": "weight for each input at each voxel", "xor": ["weighted_ls"]},
    ),
    (
        "weight_inv",
        bool,
        {"help_string": "invert weights", "argstr": "--w-inv", "xor": ["weighted_ls"]},
    ),
    (
        "weight_sqrt",
        bool,
        {
            "help_string": "sqrt of weights",
            "argstr": "--w-sqrt",
            "xor": ["weighted_ls"],
        },
    ),
    (
        "fwhm",
        ty.Any,
        {"help_string": "smooth input by fwhm", "argstr": "--fwhm {fwhm}"},
    ),
    (
        "var_fwhm",
        ty.Any,
        {"help_string": "smooth variance by fwhm", "argstr": "--var-fwhm {var_fwhm}"},
    ),
    (
        "no_mask_smooth",
        bool,
        {"help_string": "do not mask when smoothing", "argstr": "--no-mask-smooth"},
    ),
    (
        "no_est_fwhm",
        bool,
        {"help_string": "turn off FWHM output estimation", "argstr": "--no-est-fwhm"},
    ),
    ("mask_file", Path, {"help_string": "binary mask", "argstr": "--mask {mask_file}"}),
    (
        "label_file",
        File,
        {
            "help_string": "use label as mask, surfaces only",
            "argstr": "--label {label_file}",
            "xor": ["cortex"],
        },
    ),
    (
        "cortex",
        bool,
        {
            "help_string": "use subjects ?h.cortex.label as label",
            "argstr": "--cortex",
            "xor": ["label_file"],
        },
    ),
    ("invert_mask", bool, {"help_string": "invert mask", "argstr": "--mask-inv"}),
    (
        "prune",
        bool,
        {
            "help_string": "remove voxels that do not have a non-zero value at each frame (def)",
            "argstr": "--prune",
        },
    ),
    (
        "no_prune",
        bool,
        {"help_string": "do not prune", "argstr": "--no-prune", "xor": ["prunethresh"]},
    ),
    (
        "prune_thresh",
        float,
        {
            "help_string": "prune threshold. Default is FLT_MIN",
            "argstr": "--prune_thr {prune_thresh}",
            "xor": ["noprune"],
        },
    ),
    (
        "compute_log_y",
        bool,
        {
            "help_string": "compute natural log of y prior to analysis",
            "argstr": "--logy",
        },
    ),
    (
        "save_estimate",
        bool,
        {"help_string": "save signal estimate (yhat)", "argstr": "--yhat-save"},
    ),
    (
        "save_residual",
        bool,
        {"help_string": "save residual error (eres)", "argstr": "--eres-save"},
    ),
    (
        "save_res_corr_mtx",
        bool,
        {
            "help_string": "save residual error spatial correlation matrix (eres.scm). Big!",
            "argstr": "--eres-scm",
        },
    ),
    (
        "surf",
        bool,
        {
            "help_string": "analysis is on a surface mesh",
            "argstr": "--surf {surf[0]} {surf[1]} {surf[2]}",
            "requires": ["subject_id", "hemi"],
        },
    ),
    ("subject_id", str, {"help_string": "subject id for surface geometry"}),
    ("hemi", ty.Any, {"help_string": "surface hemisphere"}),
    (
        "surf_geo",
        str,
        "white",
        {"help_string": "surface geometry name (e.g. white, pial)"},
    ),
    (
        "simulation",
        ty.Any,
        {
            "help_string": "nulltype nsim thresh csdbasename",
            "argstr": "--sim {simulation[0]} {simulation[1]} {simulation[2]} {simulation[3]}",
        },
    ),
    (
        "sim_sign",
        ty.Any,
        {"help_string": "abs, pos, or neg", "argstr": "--sim-sign {sim_sign}"},
    ),
    (
        "uniform",
        ty.Any,
        {
            "help_string": "use uniform distribution instead of gaussian",
            "argstr": "--uniform {uniform[0]} {uniform[1]}",
        },
    ),
    (
        "pca",
        bool,
        {"help_string": "perform pca/svd analysis on residual", "argstr": "--pca"},
    ),
    (
        "calc_AR1",
        bool,
        {
            "help_string": "compute and save temporal AR1 of residual",
            "argstr": "--tar1",
        },
    ),
    (
        "save_cond",
        bool,
        {
            "help_string": "flag to save design matrix condition at each voxel",
            "argstr": "--save-cond",
        },
    ),
    (
        "vox_dump",
        ty.Any,
        {
            "help_string": "dump voxel GLM and exit",
            "argstr": "--voxdump {vox_dump[0]} {vox_dump[1]} {vox_dump[2]}",
        },
    ),
    (
        "seed",
        int,
        {"help_string": "used for synthesizing noise", "argstr": "--seed {seed}"},
    ),
    (
        "synth",
        bool,
        {"help_string": "replace input with gaussian", "argstr": "--synth"},
    ),
    (
        "resynth_test",
        int,
        {
            "help_string": "test GLM by resynthsis",
            "argstr": "--resynthtest {resynth_test}",
        },
    ),
    (
        "profile",
        int,
        {"help_string": "niters : test speed", "argstr": "--profile {profile}"},
    ),
    (
        "mrtm2",
        ty.Any,
        {
            "help_string": "RefTac TimeSec k2prime : perform MRTM2 kinetic modeling",
            "argstr": "--mrtm2 {mrtm2[0]} {mrtm2[1]} {mrtm2[2]}",
        },
    ),
    (
        "logan",
        ty.Any,
        {
            "help_string": "RefTac TimeSec tstar   : perform Logan kinetic modeling",
            "argstr": "--logan {logan[0]} {logan[1]} {logan[2]}",
        },
    ),
    (
        "force_perm",
        bool,
        {
            "help_string": "force perumtation test, even when design matrix is not orthog",
            "argstr": "--perm-force",
        },
    ),
    (
        "diag",
        int,
        {"help_string": "Gdiag_no : set diagnostic level", "argstr": "--diag {diag}"},
    ),
    (
        "diag_cluster",
        bool,
        {
            "help_string": "save sig volume and exit from first sim loop",
            "argstr": "--diag-cluster",
        },
    ),
    ("debug", bool, {"help_string": "turn on debugging", "argstr": "--debug"}),
    (
        "check_opts",
        bool,
        {
            "help_string": "don't run anything, just check options and exit",
            "argstr": "--checkopts",
        },
    ),
    (
        "allow_repeated_subjects",
        bool,
        {
            "help_string": "allow subject names to repeat in the fsgd file (must appear before --fsgd",
            "argstr": "--allowsubjrep",
        },
    ),
    (
        "allow_ill_cond",
        bool,
        {"help_string": "allow ill-conditioned design matrices", "argstr": "--illcond"},
    ),
    (
        "sim_done_file",
        File,
        {
            "help_string": "create file when simulation finished",
            "argstr": "--sim-done {sim_done_file}",
        },
    ),
    (
        "nii",
        bool,
        {
            "help_string": "save outputs as nii",
            "argstr": "--nii",
            "xor": ["nii", "nii_gz"],
        },
    ),
    (
        "nii_gz",
        bool,
        {
            "help_string": "save outputs as nii.gz",
            "argstr": "--nii.gz",
            "xor": ["nii", "nii_gz"],
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
MRTM_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("beta_file", File, {"help_string": "map of regression coefficients"}),
    ("error_file", File, {"help_string": "map of residual error"}),
    ("error_var_file", File, {"help_string": "map of residual error variance"}),
    (
        "error_stddev_file",
        File,
        {"help_string": "map of residual error standard deviation"},
    ),
    ("estimate_file", File, {"help_string": "map of the estimated Y values"}),
    ("mask_file", File, {"help_string": "map of the mask used in the analysis"}),
    ("fwhm_file", File, {"help_string": "text file with estimated smoothness"}),
    (
        "dof_file",
        File,
        {"help_string": "text file with effective degrees-of-freedom for the analysis"},
    ),
    (
        "gamma_file",
        ty.Union[list, object, MultiOutputType],
        {"help_string": "map of contrast of regression coefficients"},
    ),
    (
        "gamma_var_file",
        ty.Union[list, object, MultiOutputType],
        {"help_string": "map of regression contrast variance"},
    ),
    (
        "sig_file",
        ty.Union[list, object, MultiOutputType],
        {"help_string": "map of F-test significance (in -log10p)"},
    ),
    (
        "ftest_file",
        ty.Union[list, object, MultiOutputType],
        {"help_string": "map of test statistic values"},
    ),
    (
        "spatial_eigenvectors",
        File,
        {"help_string": "map of spatial eigenvectors from residual PCA"},
    ),
    (
        "frame_eigenvectors",
        File,
        {"help_string": "matrix of frame eigenvectors from residual PCA"},
    ),
    (
        "singular_values",
        File,
        {"help_string": "matrix singular values from residual PCA"},
    ),
    ("svd_stats_file", File, {"help_string": "text file summarizing the residual PCA"}),
    ("k2p_file", File, {"help_string": "estimate of k2p parameter"}),
    ("bp_file", File, {"help_string": "Binding potential estimates"}),
]
MRTM_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MRTM(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.engine.specs import MultiOutputType
    >>> from pydra.tasks.freesurfer.auto.petsurfer.mrtm import MRTM

    >>> task = MRTM()
    >>> task.inputs.mrtm1 = ("ref_tac.dat", "timing.dat")
    >>> task.inputs.glm_dir = "mrtm"
    >>> task.inputs.in_file = Nifti1.mock("tac.nii")
    >>> task.inputs.design = File.mock()
    >>> task.inputs.weighted_ls = File.mock()
    >>> task.inputs.fixed_fx_var = File.mock()
    >>> task.inputs.fixed_fx_dof_file = File.mock()
    >>> task.inputs.weight_file = File.mock()
    >>> task.inputs.label_file = File.mock()
    >>> task.inputs.sim_done_file = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_glmfit --glmdir mrtm --y tac.nii --mrtm1 ref_tac.dat timing.dat'


    """

    input_spec = MRTM_input_spec
    output_spec = MRTM_output_spec
    executable = "mri_glmfit"
