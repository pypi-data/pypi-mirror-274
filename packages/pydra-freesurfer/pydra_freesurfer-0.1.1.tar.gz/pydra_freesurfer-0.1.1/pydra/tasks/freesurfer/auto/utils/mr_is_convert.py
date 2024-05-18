from fileformats.generic import Directory, File
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "annot_file",
        File,
        {
            "help_string": "input is annotation or gifti label data",
            "argstr": "--annot {annot_file}",
        },
    ),
    (
        "parcstats_file",
        File,
        {
            "help_string": "infile is name of text file containing label/val pairs",
            "argstr": "--parcstats {parcstats_file}",
        },
    ),
    (
        "label_file",
        File,
        {
            "help_string": "infile is .label file, label is name of this label",
            "argstr": "--label {label_file}",
        },
    ),
    (
        "scalarcurv_file",
        File,
        {
            "help_string": "input is scalar curv overlay file (must still specify surface)",
            "argstr": "-c {scalarcurv_file}",
        },
    ),
    (
        "functional_file",
        File,
        {
            "help_string": "input is functional time-series or other multi-frame data (must specify surface)",
            "argstr": "-f {functional_file}",
        },
    ),
    (
        "labelstats_outfile",
        File,
        {
            "help_string": "outfile is name of gifti file to which label stats will be written",
            "argstr": "--labelstats {labelstats_outfile}",
        },
    ),
    (
        "patch",
        bool,
        {"help_string": "input is a patch, not a full surface", "argstr": "-p"},
    ),
    (
        "rescale",
        bool,
        {
            "help_string": "rescale vertex xyz so total area is same as group average",
            "argstr": "-r",
        },
    ),
    (
        "normal",
        bool,
        {"help_string": "output is an ascii file where vertex data", "argstr": "-n"},
    ),
    (
        "xyz_ascii",
        bool,
        {"help_string": "Print only surface xyz to ascii file", "argstr": "-a"},
    ),
    (
        "vertex",
        bool,
        {"help_string": "Writes out neighbors of a vertex in each row", "argstr": "-v"},
    ),
    (
        "scale",
        float,
        {"help_string": "scale vertex xyz by scale", "argstr": "-s {scale:.3}"},
    ),
    (
        "dataarray_num",
        int,
        {
            "help_string": "if input is gifti, 'num' specifies which data array to use",
            "argstr": "--da_num {dataarray_num}",
        },
    ),
    (
        "talairachxfm_subjid",
        ty.Any,
        {
            "help_string": "apply talairach xfm of subject to vertex xyz",
            "argstr": "-t {talairachxfm_subjid}",
        },
    ),
    (
        "origname",
        ty.Any,
        {"help_string": "read orig positions", "argstr": "-o {origname}"},
    ),
    (
        "in_file",
        File,
        {
            "help_string": "File to read/convert",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output filename or True to generate one",
            "argstr": "{out_file}",
            "mandatory": True,
            "position": -1,
            "xor": ["out_datatype"],
        },
    ),
    (
        "out_datatype",
        ty.Any,
        {
            "help_string": "These file formats are supported:  ASCII:       .ascICO: .ico, .tri GEO: .geo STL: .stl VTK: .vtk GIFTI: .gii MGH surface-encoded 'volume': .mgh, .mgz",
            "mandatory": True,
            "xor": ["out_file"],
        },
    ),
    (
        "to_scanner",
        bool,
        {
            "help_string": "convert coordinates from native FS (tkr) coords to scanner coords",
            "argstr": "--to-scanner",
        },
    ),
    (
        "to_tkr",
        bool,
        {
            "help_string": "convert coordinates from scanner coords to native FS (tkr) coords",
            "argstr": "--to-tkr",
        },
    ),
    ("subjects_dir", Directory, {"help_string": "subjects directory"}),
]
MRIsConvert_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("converted", File, {"help_string": "converted output surface"})]
MRIsConvert_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MRIsConvert(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.auto.utils.mr_is_convert import MRIsConvert

    """

    input_spec = MRIsConvert_input_spec
    output_spec = MRIsConvert_output_spec
    executable = "mris_convert"
