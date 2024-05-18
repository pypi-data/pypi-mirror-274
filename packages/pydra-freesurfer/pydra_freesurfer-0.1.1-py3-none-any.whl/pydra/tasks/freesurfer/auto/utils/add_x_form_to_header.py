from fileformats.datascience import TextMatrix
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
            "help_string": "input volume",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "transform",
        TextMatrix,
        {
            "help_string": "xfm file",
            "argstr": "{transform}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "out_file",
        Path,
        "output.mgz",
        {"help_string": "output volume", "argstr": "{out_file}", "position": -1},
    ),
    (
        "copy_name",
        bool,
        {
            "help_string": "do not try to load the xfmfile, just copy name",
            "argstr": "-c",
        },
    ),
    ("verbose", bool, {"help_string": "be verbose", "argstr": "-v"}),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
AddXFormToHeader_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", File, {"help_string": "output volume"})]
AddXFormToHeader_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class AddXFormToHeader(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pydra.tasks.freesurfer.auto.utils.add_x_form_to_header import AddXFormToHeader

    >>> task = AddXFormToHeader()
    >>> task.inputs.in_file = MghGz.mock("norm.mgz")
    >>> task.inputs.transform = TextMatrix.mock("trans.mat")
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_add_xform_to_header trans.mat norm.mgz output.mgz'


    >>> task = AddXFormToHeader()
    >>> task.inputs.in_file = MghGz.mock()
    >>> task.inputs.transform = TextMatrix.mock()
    >>> task.inputs.copy_name = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_add_xform_to_header -c trans.mat norm.mgz output.mgz'


    """

    input_spec = AddXFormToHeader_input_spec
    output_spec = AddXFormToHeader_output_spec
    executable = "mri_add_xform_to_header"
