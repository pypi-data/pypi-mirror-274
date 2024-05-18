from fileformats.generic import Directory
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "lh_white",
        Pial,
        {
            "help_string": "Implicit input file must be lh.white",
            "copyfile": True,
            "mandatory": True,
        },
    ),
    (
        "rh_white",
        Pial,
        {
            "help_string": "Implicit input file must be rh.white",
            "copyfile": True,
            "mandatory": True,
        },
    ),
    (
        "aseg",
        MghGz,
        {
            "help_string": "Input aseg file",
            "argstr": "{aseg}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "surf_directory",
        Directory,
        ".",
        {
            "help_string": "Directory containing lh.white and rh.white",
            "argstr": "{surf_directory}",
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Output aseg file",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": "{aseg}.hypos.mgz",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
RelabelHypointensities_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
RelabelHypointensities_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class RelabelHypointensities(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.auto.utils.relabel_hypointensities import RelabelHypointensities

    >>> task = RelabelHypointensities()
    >>> task.inputs.lh_white = Pial.mock("lh.pial")
    >>> task.inputs.rh_white = Pial.mock("lh.pial")
    >>> task.inputs.aseg = MghGz.mock("aseg.mgz")
    >>> task.inputs.surf_directory = Directory.mock(".")
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_relabel_hypointensities aseg.mgz . aseg.hypos.mgz'


    """

    input_spec = RelabelHypointensities_input_spec
    output_spec = RelabelHypointensities_output_spec
    executable = "mri_relabel_hypointensities"
