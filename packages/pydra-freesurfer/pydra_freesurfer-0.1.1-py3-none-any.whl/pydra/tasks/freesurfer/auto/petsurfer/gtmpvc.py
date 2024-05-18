from fileformats.generic import Directory, File
from fileformats.medimage import MghGz, NiftiGz
from fileformats.medimage_freesurfer import Lta
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        NiftiGz,
        {
            "help_string": "input volume - source data to pvc",
            "argstr": "--i {in_file}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "frame",
        int,
        {
            "help_string": "only process 0-based frame F from inputvol",
            "argstr": "--frame {frame}",
        },
    ),
    ("psf", float, {"help_string": "scanner PSF FWHM in mm", "argstr": "--psf {psf}"}),
    (
        "segmentation",
        MghGz,
        {
            "help_string": "segfile : anatomical segmentation to define regions for GTM",
            "argstr": "--seg {segmentation}",
            "mandatory": True,
        },
    ),
    (
        "reg_file",
        Lta,
        {
            "help_string": "LTA registration file that maps PET to anatomical",
            "argstr": "--reg {reg_file}",
            "mandatory": True,
            "xor": ["reg_file", "regheader", "reg_identity"],
        },
    ),
    (
        "regheader",
        bool,
        {
            "help_string": "assume input and seg share scanner space",
            "argstr": "--regheader",
            "mandatory": True,
            "xor": ["reg_file", "regheader", "reg_identity"],
        },
    ),
    (
        "reg_identity",
        bool,
        {
            "help_string": "assume that input is in anatomical space",
            "argstr": "--reg-identity",
            "mandatory": True,
            "xor": ["reg_file", "regheader", "reg_identity"],
        },
    ),
    (
        "pvc_dir",
        str,
        {
            "help_string": "save outputs to dir",
            "argstr": "--o {pvc_dir}",
            "output_file_template": '"pvc"',
        },
    ),
    (
        "mask_file",
        File,
        {
            "help_string": "ignore areas outside of the mask (in input vol space)",
            "argstr": "--mask {mask_file}",
        },
    ),
    (
        "auto_mask",
        ty.Any,
        {
            "help_string": "FWHM thresh : automatically compute mask",
            "argstr": "--auto-mask {auto_mask[0]} {auto_mask[1]}",
        },
    ),
    (
        "no_reduce_fov",
        bool,
        {
            "help_string": "do not reduce FoV to encompass mask",
            "argstr": "--no-reduce-fov",
        },
    ),
    (
        "reduce_fox_eqodd",
        bool,
        {
            "help_string": "reduce FoV to encompass mask but force nc=nr and ns to be odd",
            "argstr": "--reduce-fox-eqodd",
        },
    ),
    (
        "contrast",
        ty.List[File],
        {"help_string": "contrast file", "argstr": "--C {contrast}..."},
    ),
    (
        "default_seg_merge",
        bool,
        {
            "help_string": "default schema for merging ROIs",
            "argstr": "--default-seg-merge",
        },
    ),
    (
        "merge_hypos",
        bool,
        {
            "help_string": "merge left and right hypointensites into to ROI",
            "argstr": "--merge-hypos",
        },
    ),
    (
        "merge_cblum_wm_gyri",
        bool,
        {
            "help_string": "cerebellum WM gyri back into cerebellum WM",
            "argstr": "--merge-cblum-wm-gyri",
        },
    ),
    (
        "tt_reduce",
        bool,
        {
            "help_string": "reduce segmentation to that of a tissue type",
            "argstr": "--tt-reduce",
        },
    ),
    (
        "replace",
        ty.Any,
        {
            "help_string": "Id1 Id2 : replace seg Id1 with seg Id2",
            "argstr": "--replace {replace[0]} {replace[1]}",
        },
    ),
    (
        "rescale",
        list,
        {
            "help_string": "Id1 <Id2...>  : specify reference region(s) used to rescale (default is pons)",
            "argstr": "--rescale {rescale}...",
        },
    ),
    (
        "no_rescale",
        bool,
        {
            "help_string": "do not global rescale such that mean of reference region is scaleref",
            "argstr": "--no-rescale",
        },
    ),
    (
        "scale_refval",
        float,
        {
            "help_string": "refval : scale such that mean in reference region is refval",
            "argstr": "--scale-refval {scale_refval}",
        },
    ),
    (
        "color_table_file",
        File,
        {
            "help_string": "color table file with seg id names",
            "argstr": "--ctab {color_table_file}",
            "xor": ("color_table_file", "default_color_table"),
        },
    ),
    (
        "default_color_table",
        bool,
        {
            "help_string": "use $FREESURFER_HOME/FreeSurferColorLUT.txt",
            "argstr": "--ctab-default",
            "xor": ("color_table_file", "default_color_table"),
        },
    ),
    (
        "tt_update",
        bool,
        {
            "help_string": "changes tissue type of VentralDC, BrainStem, and Pons to be SubcortGM",
            "argstr": "--tt-update",
        },
    ),
    ("lat", bool, {"help_string": "lateralize tissue types", "argstr": "--lat"}),
    (
        "no_tfe",
        bool,
        {
            "help_string": "do not correct for tissue fraction effect (with --psf 0 turns off PVC entirely)",
            "argstr": "--no-tfe",
        },
    ),
    (
        "no_pvc",
        bool,
        {
            "help_string": "turns off PVC entirely (both PSF and TFE)",
            "argstr": "--no-pvc",
        },
    ),
    (
        "tissue_fraction_resolution",
        float,
        {
            "help_string": "set the tissue fraction resolution parameter (def is 0.5)",
            "argstr": "--segpvfres {tissue_fraction_resolution}",
        },
    ),
    (
        "rbv",
        bool,
        {
            "help_string": "perform Region-based Voxelwise (RBV) PVC",
            "argstr": "--rbv",
            "requires": ["subjects_dir"],
        },
    ),
    (
        "rbv_res",
        float,
        {
            "help_string": "voxsize : set RBV voxel resolution (good for when standard res takes too much memory)",
            "argstr": "--rbv-res {rbv_res}",
        },
    ),
    (
        "mg",
        ty.Any,
        {
            "help_string": "gmthresh RefId1 RefId2 ...: perform Mueller-Gaertner PVC, gmthresh is min gm pvf bet 0 and 1",
            "argstr": "--mg {mg[0]} {mg[1]}",
        },
    ),
    (
        "mg_ref_cerebral_wm",
        bool,
        {"help_string": " set MG RefIds to 2 and 41", "argstr": "--mg-ref-cerebral-wm"},
    ),
    (
        "mg_ref_lobes_wm",
        bool,
        {
            "help_string": "set MG RefIds to those for lobes when using wm subseg",
            "argstr": "--mg-ref-lobes-wm",
        },
    ),
    (
        "mgx",
        float,
        {
            "help_string": "gmxthresh : GLM-based Mueller-Gaertner PVC, gmxthresh is min gm pvf bet 0 and 1",
            "argstr": "--mgx {mgx}",
        },
    ),
    (
        "km_ref",
        list,
        {
            "help_string": "RefId1 RefId2 ... : compute reference TAC for KM as mean of given RefIds",
            "argstr": "--km-ref {km_ref}...",
        },
    ),
    (
        "km_hb",
        list,
        {
            "help_string": "RefId1 RefId2 ... : compute HiBinding TAC for KM as mean of given RefIds",
            "argstr": "--km-hb {km_hb}...",
        },
    ),
    (
        "steady_state_params",
        ty.Any,
        {
            "help_string": "bpc scale dcf : steady-state analysis spec blood plasma concentration, unit scale and decay correction factor. You must also spec --km-ref. Turns off rescaling",
            "argstr": "--ss {steady_state_params[0]} {steady_state_params[1]} {steady_state_params[2]}",
        },
    ),
    (
        "X",
        bool,
        {
            "help_string": "save X matrix in matlab4 format as X.mat (it will be big)",
            "argstr": "--X",
        },
    ),
    (
        "y",
        bool,
        {"help_string": "save y matrix in matlab4 format as y.mat", "argstr": "--y"},
    ),
    (
        "beta",
        bool,
        {
            "help_string": "save beta matrix in matlab4 format as beta.mat",
            "argstr": "--beta",
        },
    ),
    (
        "X0",
        bool,
        {
            "help_string": "save X0 matrix in matlab4 format as X0.mat (it will be big)",
            "argstr": "--X0",
        },
    ),
    (
        "save_input",
        bool,
        {
            "help_string": "saves rescaled input as input.rescaled.nii.gz",
            "argstr": "--save-input",
        },
    ),
    (
        "save_eres",
        bool,
        {"help_string": "saves residual error", "argstr": "--save-eres"},
    ),
    (
        "save_yhat",
        bool,
        {
            "help_string": "save signal estimate (yhat) smoothed with the PSF",
            "argstr": "--save-yhat",
            "xor": ["save_yhat_with_noise"],
        },
    ),
    (
        "save_yhat_with_noise",
        ty.Any,
        {
            "help_string": "seed nreps : save signal estimate (yhat) with noise",
            "argstr": "--save-yhat-with-noise {save_yhat_with_noise[0]} {save_yhat_with_noise[1]}",
            "xor": ["save_yhat"],
        },
    ),
    (
        "save_yhat_full_fov",
        bool,
        {
            "help_string": "save signal estimate (yhat)",
            "argstr": "--save-yhat-full-fov",
        },
    ),
    (
        "save_yhat0",
        bool,
        {"help_string": "save signal estimate (yhat)", "argstr": "--save-yhat0"},
    ),
    (
        "optimization_schema",
        ty.Any,
        {
            "help_string": "opt : optimization schema for applying adaptive GTM",
            "argstr": "--opt {optimization_schema}",
        },
    ),
    (
        "opt_tol",
        ty.Any,
        {
            "help_string": "n_iters_max ftol lin_min_tol : optimization parameters for adaptive gtm using fminsearch",
            "argstr": "--opt-tol {opt_tol[0]} {opt_tol[1]} {opt_tol[2]}",
        },
    ),
    ("opt_brain", bool, {"help_string": "apply adaptive GTM", "argstr": "--opt-brain"}),
    (
        "opt_seg_merge",
        bool,
        {
            "help_string": "optimal schema for merging ROIs when applying adaptive GTM",
            "argstr": "--opt-seg-merge",
        },
    ),
    (
        "num_threads",
        int,
        {
            "help_string": "threads : number of threads to use",
            "argstr": "--threads {num_threads}",
        },
    ),
    (
        "psf_col",
        float,
        {
            "help_string": "xFWHM : full-width-half-maximum in the x-direction",
            "argstr": "--psf-col {psf_col}",
        },
    ),
    (
        "psf_row",
        float,
        {
            "help_string": "yFWHM : full-width-half-maximum in the y-direction",
            "argstr": "--psf-row {psf_row}",
        },
    ),
    (
        "psf_slice",
        float,
        {
            "help_string": "zFWHM : full-width-half-maximum in the z-direction",
            "argstr": "--psf-slice {psf_slice}",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
GTMPVC_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("ref_file", File, {"help_string": "Reference TAC in .dat"}),
    ("hb_nifti", File, {"help_string": "High-binding TAC in nifti"}),
    ("hb_dat", File, {"help_string": "High-binding TAC in .dat"}),
    ("nopvc_file", File, {"help_string": "TACs for all regions with no PVC"}),
    ("gtm_file", File, {"help_string": "TACs for all regions with GTM PVC"}),
    ("gtm_stats", File, {"help_string": "Statistics for the GTM PVC"}),
    ("input_file", File, {"help_string": "4D PET file in native volume space"}),
    ("reg_pet2anat", File, {"help_string": "Registration file to go from PET to anat"}),
    ("reg_anat2pet", File, {"help_string": "Registration file to go from anat to PET"}),
    (
        "reg_rbvpet2anat",
        File,
        {"help_string": "Registration file to go from RBV corrected PET to anat"},
    ),
    (
        "reg_anat2rbvpet",
        File,
        {"help_string": "Registration file to go from anat to RBV corrected PET"},
    ),
    (
        "mgx_ctxgm",
        File,
        {
            "help_string": "Cortical GM voxel-wise values corrected using the extended Muller-Gartner method"
        },
    ),
    (
        "mgx_subctxgm",
        File,
        {
            "help_string": "Subcortical GM voxel-wise values corrected using the extended Muller-Gartner method"
        },
    ),
    (
        "mgx_gm",
        File,
        {
            "help_string": "All GM voxel-wise values corrected using the extended Muller-Gartner method"
        },
    ),
    (
        "rbv",
        File,
        {"help_string": "All GM voxel-wise values corrected using the RBV method"},
    ),
    (
        "opt_params",
        File,
        {"help_string": "Optimal parameter estimates for the FWHM using adaptive GTM"},
    ),
    (
        "yhat0",
        File,
        {"help_string": "4D PET file of signal estimate (yhat) after PVC (unsmoothed)"},
    ),
    (
        "yhat",
        File,
        {
            "help_string": "4D PET file of signal estimate (yhat) after PVC (smoothed with PSF)"
        },
    ),
    (
        "yhat_full_fov",
        File,
        {
            "help_string": "4D PET file with full FOV of signal estimate (yhat) after PVC (smoothed with PSF)"
        },
    ),
    (
        "yhat_with_noise",
        File,
        {
            "help_string": "4D PET file with full FOV of signal estimate (yhat) with noise after PVC (smoothed with PSF)"
        },
    ),
]
GTMPVC_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class GTMPVC(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz, NiftiGz
    >>> from fileformats.medimage_freesurfer import Lta
    >>> from pydra.tasks.freesurfer.auto.petsurfer.gtmpvc import GTMPVC

    >>> task = GTMPVC()
    >>> task.inputs.in_file = NiftiGz.mock("sub-01_ses-baseline_pet.nii.gz")
    >>> task.inputs.psf = 4
    >>> task.inputs.segmentation = MghGz.mock("gtmseg.mgz")
    >>> task.inputs.reg_file = Lta.mock("sub-01_ses-baseline_pet_mean_reg.lta")
    >>> task.inputs.pvc_dir = "pvc"
    >>> task.inputs.mask_file = File.mock()
    >>> task.inputs.auto_mask = (1, 0.1)
    >>> task.inputs.default_seg_merge = True
    >>> task.inputs.no_rescale = True
    >>> task.inputs.color_table_file = File.mock()
    >>> task.inputs.km_ref = ["8 47"]
    >>> task.inputs.km_hb = ["11 12 50 51"]
    >>> task.inputs.save_input = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_gtmpvc --auto-mask 1.000000 0.100000 --default-seg-merge --i sub-01_ses-baseline_pet.nii.gz --km-hb 11 12 50 51 --km-ref 8 47 --no-rescale --psf 4.000000 --o pvc --reg sub-01_ses-baseline_pet_mean_reg.lta --save-input --seg gtmseg.mgz'


    >>> task = GTMPVC()
    >>> task.inputs.in_file = NiftiGz.mock("sub-01_ses-baseline_pet.nii.gz")
    >>> task.inputs.segmentation = MghGz.mock("gtmseg.mgz")
    >>> task.inputs.reg_file = Lta.mock()
    >>> task.inputs.regheader = True
    >>> task.inputs.pvc_dir = "pvc"
    >>> task.inputs.mask_file = File.mock()
    >>> task.inputs.color_table_file = File.mock()
    >>> task.inputs.mg = (0.5, ["ROI1", "ROI2"])
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_gtmpvc --i sub-01_ses-baseline_pet.nii.gz --mg 0.5 ROI1 ROI2 --o pvc --regheader --seg gtmseg.mgz'


    """

    input_spec = GTMPVC_input_spec
    output_spec = GTMPVC_output_spec
    executable = "mri_gtmpvc"
