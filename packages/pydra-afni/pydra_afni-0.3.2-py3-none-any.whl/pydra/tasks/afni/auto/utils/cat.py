from fileformats.medimage_afni import OneD
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_files",
        ty.List[OneD],
        {"help_string": "", "argstr": "{in_files}", "mandatory": True, "position": -2},
    ),
    (
        "out_file",
        OneD,
        {
            "help_string": "output (concatenated) file name",
            "argstr": "> {out_file}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "omitconst",
        bool,
        {
            "help_string": "Omit columns that are identically constant from output.",
            "argstr": "-nonconst",
        },
    ),
    (
        "keepfree",
        bool,
        {
            "help_string": "Keep only columns that are marked as 'free' in the 3dAllineate header from '-1Dparam_save'. If there is no such header, all columns are kept.",
            "argstr": "-nonfixed",
        },
    ),
    (
        "out_format",
        ty.Any,
        {
            "help_string": "specify data type for output.",
            "argstr": "-form {out_format}",
            "xor": ["out_int", "out_nice", "out_double", "out_fint", "out_cint"],
        },
    ),
    (
        "stack",
        bool,
        {
            "help_string": "Stack the columns of the resultant matrix in the output.",
            "argstr": "-stack",
        },
    ),
    (
        "sel",
        str,
        {
            "help_string": "Apply the same column/row selection string to all filenames on the command line.",
            "argstr": "-sel {sel}",
        },
    ),
    (
        "out_int",
        bool,
        {
            "help_string": "specify int data type for output",
            "argstr": "-i",
            "xor": ["out_format", "out_nice", "out_double", "out_fint", "out_cint"],
        },
    ),
    (
        "out_nice",
        bool,
        {
            "help_string": "specify nice data type for output",
            "argstr": "-n",
            "xor": ["out_format", "out_int", "out_double", "out_fint", "out_cint"],
        },
    ),
    (
        "out_double",
        bool,
        {
            "help_string": "specify double data type for output",
            "argstr": "-d",
            "xor": ["out_format", "out_nice", "out_int", "out_fint", "out_cint"],
        },
    ),
    (
        "out_fint",
        bool,
        {
            "help_string": "specify int, rounded down, data type for output",
            "argstr": "-f",
            "xor": ["out_format", "out_nice", "out_double", "out_int", "out_cint"],
        },
    ),
    (
        "out_cint",
        bool,
        {
            "help_string": "specify int, rounded up, data type for output",
            "xor": ["out_format", "out_nice", "out_double", "out_fint", "out_int"],
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Cat_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", OneD, {"help_string": "output file"})]
Cat_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Cat(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage_afni import OneD
    >>> from pydra.tasks.afni.auto.utils.cat import Cat

    >>> task = Cat()
    >>> task.inputs.in_files = None
    >>> task.inputs.out_file = OneD.mock(None)
    >>> task.inputs.sel = "'[0,2]'"
    >>> task.cmdline
    '1dcat -sel "[0,2]" f1.1D f2.1D > catout.1d'


    """

    input_spec = Cat_input_spec
    output_spec = Cat_output_spec
    executable = "1dcat"
