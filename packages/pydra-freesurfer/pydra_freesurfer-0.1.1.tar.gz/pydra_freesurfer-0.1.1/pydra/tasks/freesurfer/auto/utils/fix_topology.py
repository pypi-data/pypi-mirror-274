from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Inflated, Nofix, Orig
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_orig",
        Orig,
        {"help_string": "Undocumented input file <hemisphere>.orig", "mandatory": True},
    ),
    (
        "in_inflated",
        Inflated,
        {
            "help_string": "Undocumented input file <hemisphere>.inflated",
            "mandatory": True,
        },
    ),
    ("in_brain", File, {"help_string": "Implicit input brain.mgz", "mandatory": True}),
    ("in_wm", File, {"help_string": "Implicit input wm.mgz", "mandatory": True}),
    (
        "hemisphere",
        ty.Any,
        {
            "help_string": "Hemisphere being processed",
            "argstr": "{hemisphere}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "subject_id",
        ty.Any,
        {
            "help_string": "Subject being processed",
            "argstr": "{subject_id}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "copy_inputs",
        bool,
        {
            "help_string": "If running as a node, set this to True otherwise, the topology fixing will be done in place.",
            "mandatory": True,
        },
    ),
    (
        "seed",
        int,
        {
            "help_string": "Seed for setting random number generator",
            "argstr": "-seed {seed}",
        },
    ),
    (
        "ga",
        bool,
        {
            "help_string": "No documentation. Direct questions to analysis-bugs@nmr.mgh.harvard.edu",
            "argstr": "-ga",
        },
    ),
    (
        "mgz",
        bool,
        {
            "help_string": "No documentation. Direct questions to analysis-bugs@nmr.mgh.harvard.edu",
            "argstr": "-mgz",
        },
    ),
    (
        "sphere",
        Nofix,
        {"help_string": "Sphere input file", "argstr": "-sphere {sphere}"},
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
FixTopology_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", File, {"help_string": "Output file for FixTopology"})]
FixTopology_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FixTopology(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Inflated, Nofix, Orig
    >>> from pydra.tasks.freesurfer.auto.utils.fix_topology import FixTopology

    >>> task = FixTopology()
    >>> task.inputs.in_orig = Orig.mock("lh.orig" # doctest: +SKIP)
    >>> task.inputs.in_inflated = Inflated.mock("lh.inflated" # doctest: +SKIP)
    >>> task.inputs.in_brain = File.mock()
    >>> task.inputs.in_wm = File.mock()
    >>> task.inputs.hemisphere = "lh"
    >>> task.inputs.subject_id = "10335"
    >>> task.inputs.ga = True
    >>> task.inputs.mgz = True
    >>> task.inputs.sphere = Nofix.mock("lh.qsphere.nofix" # doctest: +SKIP)
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_fix_topology -ga -mgz -sphere qsphere.nofix 10335 lh'


    """

    input_spec = FixTopology_input_spec
    output_spec = FixTopology_output_spec
    executable = "mris_fix_topology"
