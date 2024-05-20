from fileformats.medimage import Nifti1
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_files",
        ty.List[Nifti1],
        {
            "help_string": "",
            "argstr": "{in_files}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_file",
        Nifti1,
        {
            "help_string": "output dataset prefix name (default 'zcat')",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_files}_zcat",
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
        "verb",
        bool,
        {
            "help_string": "print out some verbositiness as the program proceeds.",
            "argstr": "-verb",
        },
    ),
    (
        "fscale",
        bool,
        {
            "help_string": "Force scaling of the output to the maximum integer range.  This only has effect if the output datum is byte or short (either forced or defaulted). This option is sometimes necessary to eliminate unpleasant truncation artifacts.",
            "argstr": "-fscale",
            "xor": ["nscale"],
        },
    ),
    (
        "nscale",
        bool,
        {
            "help_string": "Don't do any scaling on output to byte or short datasets. This may be especially useful when operating on mask datasets whose output values are only 0's and 1's.",
            "argstr": "-nscale",
            "xor": ["fscale"],
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Zcat_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Zcat_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Zcat(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.zcat import Zcat

    >>> task = Zcat()
    >>> task.inputs.in_files = None
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.cmdline
    '3dZcat -prefix cat_functional.nii functional2.nii functional3.nii'


    """

    input_spec = Zcat_input_spec
    output_spec = Zcat_output_spec
    executable = "3dZcat"
