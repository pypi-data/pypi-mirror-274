from fileformats.generic import Directory
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_surf",
        Pial,
        {
            "help_string": "Surface file with grid (vertices) onto which the template data is to be sampled or 'painted'",
            "argstr": "{in_surf}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "template",
        MghGz,
        {
            "help_string": "Template file",
            "argstr": "{template}",
            "mandatory": True,
            "position": -3,
        },
    ),
    ("template_param", int, {"help_string": "Frame number of the input template"}),
    (
        "averages",
        int,
        {"help_string": "Average curvature patterns", "argstr": "-a {averages}"},
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "File containing a surface-worth of per-vertex values, saved in 'curvature' format.",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": "{in_surf}.avg_curv",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
Paint_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Paint_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Paint(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.registration.paint import Paint

    >>> task = Paint()
    >>> task.inputs.in_surf = Pial.mock("lh.pial")
    >>> task.inputs.template = MghGz.mock("aseg.mgz")
    >>> task.inputs.averages = 5
    >>> task.inputs.out_file = "lh.avg_curv"
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mrisp_paint -a 5 aseg.mgz lh.pial lh.avg_curv'


    """

    input_spec = Paint_input_spec
    output_spec = Paint_output_spec
    executable = "mrisp_paint"
