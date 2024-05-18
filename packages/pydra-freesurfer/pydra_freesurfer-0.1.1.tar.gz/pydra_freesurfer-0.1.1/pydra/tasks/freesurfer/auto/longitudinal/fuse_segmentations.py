from fileformats.generic import Directory
from fileformats.medimage import MghGz
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
from pydra.engine.specs import MultiInputObj
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "subject_id",
        ty.Any,
        {
            "help_string": "subject_id being processed",
            "argstr": "{subject_id}",
            "position": -3,
        },
    ),
    (
        "timepoints",
        MultiInputObj,
        {
            "help_string": "subject_ids or timepoints to be processed",
            "argstr": "{timepoints}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output fused segmentation file",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "in_segmentations",
        ty.List[MghGz],
        {
            "help_string": "name of aseg file to use (default: aseg.mgz)         must include the aseg files for all the given timepoints",
            "argstr": "-a {in_segmentations}",
            "mandatory": True,
        },
    ),
    (
        "in_segmentations_noCC",
        ty.List[MghGz],
        {
            "help_string": "name of aseg file w/o CC labels (default: aseg.auto_noCCseg.mgz)         must include the corresponding file for all the given timepoints",
            "argstr": "-c {in_segmentations_noCC}",
            "mandatory": True,
        },
    ),
    (
        "in_norms",
        ty.List[MghGz],
        {
            "help_string": "-n <filename>  - name of norm file to use (default: norm.mgs)         must include the corresponding norm file for all given timepoints         as well as for the current subject",
            "argstr": "-n {in_norms}",
            "mandatory": True,
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
FuseSegmentations_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", MghGz, {"help_string": "output fused segmentation file"})]
FuseSegmentations_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FuseSegmentations(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage import MghGz
    >>> from pydra.engine.specs import MultiInputObj
    >>> from pydra.tasks.freesurfer.auto.longitudinal.fuse_segmentations import FuseSegmentations

    >>> task = FuseSegmentations()
    >>> task.inputs.subject_id = "tp.long.A.template"
    >>> task.inputs.timepoints = ["tp1", "tp2"]
    >>> task.inputs.out_file = "aseg.fused.mgz"
    >>> task.inputs.in_segmentations = [MghGz.mock("aseg.mgz"), MghGz.mock("aseg.mgz")]
    >>> task.inputs.in_segmentations_noCC = [MghGz.mock("aseg.mgz"), MghGz.mock("aseg.mgz")]
    >>> task.inputs.in_norms = [MghGz.mock("norm.mgz"), MghGz.mock("norm.mgz"), MghGz.mock("norm.mgz")]
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_fuse_segmentations -n norm.mgz -a aseg.mgz -c aseg.mgz tp.long.A.template tp1 tp2'


    """

    input_spec = FuseSegmentations_input_spec
    output_spec = FuseSegmentations_output_spec
    executable = "mri_fuse_segmentations"
