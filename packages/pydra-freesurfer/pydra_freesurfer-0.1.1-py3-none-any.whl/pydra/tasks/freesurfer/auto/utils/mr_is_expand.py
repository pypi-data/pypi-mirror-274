from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import White
import logging
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        White,
        {
            "help_string": "Surface to expand",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "distance",
        float,
        {
            "help_string": "Distance in mm or fraction of cortical thickness",
            "argstr": "{distance}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_name",
        str,
        "expanded",
        {
            "help_string": 'Output surface file. If no path, uses directory of ``in_file``. If no path AND missing "lh." or "rh.", derive from ``in_file``',
            "argstr": "{out_name}",
            "position": -1,
        },
    ),
    (
        "thickness",
        bool,
        {
            "help_string": "Expand by fraction of cortical thickness, not mm",
            "argstr": "-thickness",
        },
    ),
    (
        "thickness_name",
        str,
        {
            "help_string": 'Name of thickness file (implicit: "thickness")\nIf no path, uses directory of ``in_file``\nIf no path AND missing "lh." or "rh.", derive from `in_file`',
            "argstr": "-thickness_name {thickness_name}",
            "copyfile": False,
        },
    ),
    (
        "pial",
        str,
        {
            "help_string": 'Name of pial file (implicit: "pial")\nIf no path, uses directory of ``in_file``\nIf no path AND missing "lh." or "rh.", derive from ``in_file``',
            "argstr": "-pial {pial}",
            "copyfile": False,
        },
    ),
    (
        "sphere",
        str,
        "sphere",
        {"help_string": "WARNING: Do not change this trait", "copyfile": False},
    ),
    (
        "spring",
        float,
        {"help_string": "Spring term (implicit: 0.05)", "argstr": "-S {spring}"},
    ),
    ("dt", float, {"help_string": "dt (implicit: 0.25)", "argstr": "-T {dt}"}),
    (
        "write_iterations",
        int,
        {
            "help_string": "Write snapshots of expansion every N iterations",
            "argstr": "-W {write_iterations}",
        },
    ),
    (
        "smooth_averages",
        int,
        {
            "help_string": "Smooth surface with N iterations after expansion",
            "argstr": "-A {smooth_averages}",
        },
    ),
    (
        "nsurfaces",
        int,
        {
            "help_string": "Number of surfacces to write during expansion",
            "argstr": "-N {nsurfaces}",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
MRIsExpand_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", File, {"help_string": "Output surface file"})]
MRIsExpand_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MRIsExpand(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import White
    >>> from pydra.tasks.freesurfer.auto.utils.mr_is_expand import MRIsExpand

    >>> task = MRIsExpand()
    >>> task.inputs.in_file = White.mock("lh.white")
    >>> task.inputs.distance = 0.5
    >>> task.inputs.out_name = "graymid"
    >>> task.inputs.thickness = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_expand -thickness lh.white 0.5 graymid'


    """

    input_spec = MRIsExpand_input_spec
    output_spec = MRIsExpand_output_spec
    executable = "mris_expand"
