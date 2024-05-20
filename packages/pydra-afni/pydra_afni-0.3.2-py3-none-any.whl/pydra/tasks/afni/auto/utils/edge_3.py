from fileformats.medimage import Nifti1
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dedge3",
            "argstr": "-input {in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_file",
        Nifti1,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "position": -1,
        },
    ),
    (
        "datum",
        ty.Any,
        {
            "help_string": "specify data type for output. Valid types are 'byte', 'short' and 'float'.",
            "argstr": "-datum {datum}",
        },
    ),
    (
        "fscale",
        bool,
        {
            "help_string": "Force scaling of the output to the maximum integer range.",
            "argstr": "-fscale",
            "xor": ["gscale", "nscale", "scale_floats"],
        },
    ),
    (
        "gscale",
        bool,
        {
            "help_string": "Same as '-fscale', but also forces each output sub-brick to to get the same scaling factor.",
            "argstr": "-gscale",
            "xor": ["fscale", "nscale", "scale_floats"],
        },
    ),
    (
        "nscale",
        bool,
        {
            "help_string": "Don't do any scaling on output to byte or short datasets.",
            "argstr": "-nscale",
            "xor": ["fscale", "gscale", "scale_floats"],
        },
    ),
    (
        "scale_floats",
        float,
        {
            "help_string": "Multiply input by VAL, but only if the input datum is float. This is needed when the input dataset has a small range, like 0 to 2.0 for instance. With such a range, very few edges are detected due to what I suspect to be truncation problems. Multiplying such a dataset by 10000 fixes the problem and the scaling is undone at the output.",
            "argstr": "-scale_floats {scale_floats}",
            "xor": ["fscale", "gscale", "nscale"],
        },
    ),
    (
        "verbose",
        bool,
        {
            "help_string": "Print out some information along the way.",
            "argstr": "-verbose",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
edge3_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", Nifti1, {"help_string": "output file"})]
edge3_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class edge3(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.edge_3 import edge3

    >>> task = edge3()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.inputs.datum = "byte"
    >>> task.cmdline
    '3dedge3 -input functional.nii -datum byte -prefix edges.nii'


    """

    input_spec = edge3_input_spec
    output_spec = edge3_output_spec
    executable = "3dedge3"


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dedge3",
            "argstr": "-input {in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_file",
        Nifti1,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "position": -1,
        },
    ),
    (
        "datum",
        ty.Any,
        {
            "help_string": "specify data type for output. Valid types are 'byte', 'short' and 'float'.",
            "argstr": "-datum {datum}",
        },
    ),
    (
        "fscale",
        bool,
        {
            "help_string": "Force scaling of the output to the maximum integer range.",
            "argstr": "-fscale",
            "xor": ["gscale", "nscale", "scale_floats"],
        },
    ),
    (
        "gscale",
        bool,
        {
            "help_string": "Same as '-fscale', but also forces each output sub-brick to to get the same scaling factor.",
            "argstr": "-gscale",
            "xor": ["fscale", "nscale", "scale_floats"],
        },
    ),
    (
        "nscale",
        bool,
        {
            "help_string": "Don't do any scaling on output to byte or short datasets.",
            "argstr": "-nscale",
            "xor": ["fscale", "gscale", "scale_floats"],
        },
    ),
    (
        "scale_floats",
        float,
        {
            "help_string": "Multiply input by VAL, but only if the input datum is float. This is needed when the input dataset has a small range, like 0 to 2.0 for instance. With such a range, very few edges are detected due to what I suspect to be truncation problems. Multiplying such a dataset by 10000 fixes the problem and the scaling is undone at the output.",
            "argstr": "-scale_floats {scale_floats}",
            "xor": ["fscale", "gscale", "nscale"],
        },
    ),
    (
        "verbose",
        bool,
        {
            "help_string": "Print out some information along the way.",
            "argstr": "-verbose",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Edge3_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", Nifti1, {"help_string": "output file"})]
Edge3_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Edge3(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.edge_3 import Edge3

    >>> task = Edge3()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.inputs.datum = "byte"
    >>> task.cmdline
    '3dedge3 -input functional.nii -datum byte -prefix edges.nii'


    """

    input_spec = Edge3_input_spec
    output_spec = Edge3_output_spec
    executable = "3dedge3"
