from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        MghGz,
        {
            "help_string": "input volume. Input can be any format accepted by mri_convert.",
            "argstr": "--i {in_file}",
            "mandatory": True,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output volume. Output can be any format accepted by mri_convert. If the output format is COR, then the directory must exist.",
            "argstr": "--o {out_file}",
            "output_file_template": "{in_file}_output",
        },
    ),
    (
        "iterations",
        int,
        4,
        {
            "help_string": "Number of iterations to run nu_correct. Default is 4. This is the number of times that nu_correct is repeated (ie, using the output from the previous run as the input for the next). This is different than the -iterations option to nu_correct.",
            "argstr": "--n {iterations}",
        },
    ),
    (
        "protocol_iterations",
        int,
        {
            "help_string": "Passes Np as argument of the -iterations flag of nu_correct. This is different than the --n flag above. Default is not to pass nu_correct the -iterations flag.",
            "argstr": "--proto-iters {protocol_iterations}",
        },
    ),
    (
        "distance",
        int,
        {"help_string": "N3 -distance option", "argstr": "--distance {distance}"},
    ),
    (
        "no_rescale",
        bool,
        {
            "help_string": "do not rescale so that global mean of output == input global mean",
            "argstr": "--no-rescale",
        },
    ),
    (
        "mask",
        File,
        {
            "help_string": "brainmask volume. Input can be any format accepted by mri_convert.",
            "argstr": "--mask {mask}",
        },
    ),
    (
        "transform",
        File,
        {
            "help_string": "tal.xfm. Use mri_make_uchar instead of conforming",
            "argstr": "--uchar {transform}",
        },
    ),
    (
        "stop",
        float,
        {
            "help_string": "Convergence threshold below which iteration stops (suggest 0.01 to 0.0001)",
            "argstr": "--stop {stop}",
        },
    ),
    (
        "shrink",
        int,
        {
            "help_string": "Shrink parameter for finer sampling (default is 4)",
            "argstr": "--shrink {shrink}",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
MNIBiasCorrection_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
MNIBiasCorrection_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MNIBiasCorrection(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pydra.tasks.freesurfer.auto.preprocess.mni_bias_correction import MNIBiasCorrection

    >>> task = MNIBiasCorrection()
    >>> task.inputs.in_file = MghGz.mock("norm.mgz")
    >>> task.inputs.iterations = 6
    >>> task.inputs.protocol_iterations = 1000
    >>> task.inputs.distance = 50
    >>> task.inputs.mask = File.mock()
    >>> task.inputs.transform = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_nu_correct.mni --distance 50 --i norm.mgz --n 6 --o norm_output.mgz --proto-iters 1000'


    """

    input_spec = MNIBiasCorrection_input_spec
    output_spec = MNIBiasCorrection_output_spec
    executable = "mri_nu_correct.mni"
