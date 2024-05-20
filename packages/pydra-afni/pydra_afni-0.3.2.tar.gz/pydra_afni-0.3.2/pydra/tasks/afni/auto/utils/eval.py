from fileformats.generic import File
from fileformats.medimage_afni import OneD
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file_a",
        OneD,
        {
            "help_string": "input file to 1deval",
            "argstr": "-a {in_file_a}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "in_file_b",
        OneD,
        {
            "help_string": "operand file to 1deval",
            "argstr": "-b {in_file_b}",
            "position": 1,
        },
    ),
    (
        "in_file_c",
        File,
        {
            "help_string": "operand file to 1deval",
            "argstr": "-c {in_file_c}",
            "position": 2,
        },
    ),
    (
        "out_file",
        OneD,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file_a}_calc",
        },
    ),
    ("out1D", bool, {"help_string": "output in 1D", "argstr": "-1D"}),
    (
        "expr",
        str,
        {
            "help_string": "expr",
            "argstr": '-expr "{expr}"',
            "mandatory": True,
            "position": 3,
        },
    ),
    (
        "start_idx",
        int,
        {"help_string": "start index for in_file_a", "requires": ["stop_idx"]},
    ),
    (
        "stop_idx",
        int,
        {"help_string": "stop index for in_file_a", "requires": ["start_idx"]},
    ),
    ("single_idx", int, {"help_string": "volume index for in_file_a"}),
    ("other", File, {"help_string": "other options", "argstr": ""}),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Eval_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Eval_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Eval(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage_afni import OneD
    >>> from pydra.tasks.afni.auto.utils.eval import Eval

    >>> task = Eval()
    >>> task.inputs.in_file_a = OneD.mock(None)
    >>> task.inputs.in_file_b = OneD.mock(None)
    >>> task.inputs.in_file_c = File.mock()
    >>> task.inputs.out_file = OneD.mock(None)
    >>> task.inputs.out1D = True
    >>> task.inputs.expr = "a*b"
    >>> task.inputs.other = File.mock()
    >>> task.cmdline
    '1deval -a seed.1D -b resp.1D -expr "a*b" -1D -prefix data_calc.1D'


    """

    input_spec = Eval_input_spec
    output_spec = Eval_output_spec
    executable = "1deval"
