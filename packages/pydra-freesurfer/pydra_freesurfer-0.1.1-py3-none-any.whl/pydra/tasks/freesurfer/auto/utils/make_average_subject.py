from fileformats.generic import Directory
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


def average_subject_name_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["average_subject_name"]


input_fields = [
    (
        "subjects_ids",
        list,
        {
            "help_string": "freesurfer subjects ids to average",
            "argstr": "--subjects {subjects_ids}",
            "mandatory": True,
            "sep": " ",
        },
    ),
    (
        "out_name",
        Path,
        "average",
        {"help_string": "name for the average subject", "argstr": "--out {out_name}"},
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
MakeAverageSubject_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "average_subject_name",
        str,
        {
            "help_string": "Output registration file",
            "callable": "average_subject_name_callable",
        },
    )
]
MakeAverageSubject_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MakeAverageSubject(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from pydra.tasks.freesurfer.auto.utils.make_average_subject import MakeAverageSubject

    >>> task = MakeAverageSubject()
    >>> task.inputs.subjects_ids = ["s1", "s2"]
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'make_average_subject --out average --subjects s1 s2'


    """

    input_spec = MakeAverageSubject_input_spec
    output_spec = MakeAverageSubject_output_spec
    executable = "make_average_subject"
