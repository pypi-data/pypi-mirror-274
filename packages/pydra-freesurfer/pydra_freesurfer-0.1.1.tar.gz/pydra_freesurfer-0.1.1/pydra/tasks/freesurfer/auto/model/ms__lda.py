from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.text import TextFile
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "lda_labels",
        list,
        {
            "help_string": "pair of class labels to optimize",
            "argstr": "-lda {lda_labels}",
            "mandatory": True,
            "sep": " ",
        },
    ),
    (
        "weight_file",
        Path,
        {
            "help_string": "filename for the LDA weights (input or output)",
            "argstr": "-weight {weight_file}",
            "mandatory": True,
        },
    ),
    (
        "vol_synth_file",
        Path,
        {
            "help_string": "filename for the synthesized output volume",
            "argstr": "-synth {vol_synth_file}",
            "mandatory": True,
        },
    ),
    (
        "label_file",
        MghGz,
        {
            "help_string": "filename of the label volume",
            "argstr": "-label {label_file}",
        },
    ),
    (
        "mask_file",
        File,
        {
            "help_string": "filename of the brain mask volume",
            "argstr": "-mask {mask_file}",
        },
    ),
    (
        "shift",
        int,
        {
            "help_string": "shift all values equal to the given value to zero",
            "argstr": "-shift {shift}",
        },
    ),
    (
        "conform",
        bool,
        {
            "help_string": "Conform the input volumes (brain mask typically already conformed)",
            "argstr": "-conform",
        },
    ),
    (
        "use_weights",
        bool,
        {
            "help_string": "Use the weights from a previously generated weight file",
            "argstr": "-W",
        },
    ),
    (
        "images",
        ty.List[MghGz],
        {
            "help_string": "list of input FLASH images",
            "argstr": "{images}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
MS_LDA_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("weight_file", TextFile, {}), ("vol_synth_file", MghGz, {})]
MS_LDA_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MS_LDA(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.freesurfer.auto.model.ms__lda import MS_LDA

    >>> task = MS_LDA()
    >>> task.inputs.lda_labels = [grey_label, white_label]
    >>> task.inputs.weight_file = "weights.txt"
    >>> task.inputs.vol_synth_file = "synth_out.mgz"
    >>> task.inputs.label_file = MghGz.mock("label.mgz")
    >>> task.inputs.mask_file = File.mock()
    >>> task.inputs.shift = zero_value
    >>> task.inputs.conform = True
    >>> task.inputs.use_weights = True
    >>> task.inputs.images = [MghGz.mock("FLASH1.mgz"), MghGz.mock("FLASH2.mgz"), MghGz.mock("FLASH3.mgz")]
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_ms_LDA -conform -label label.mgz -lda 2 3 -shift 1 -W -synth synth_out.mgz -weight weights.txt FLASH1.mgz FLASH2.mgz FLASH3.mgz'


    """

    input_spec = MS_LDA_input_spec
    output_spec = MS_LDA_output_spec
    executable = "mri_ms_LDA"
