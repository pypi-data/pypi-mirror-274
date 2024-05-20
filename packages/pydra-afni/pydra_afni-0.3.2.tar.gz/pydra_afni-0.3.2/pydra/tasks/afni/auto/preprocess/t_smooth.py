from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dTSmooth",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output file from 3dTSmooth",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_smooth",
        },
    ),
    (
        "datum",
        str,
        {
            "help_string": "Sets the data type of the output dataset",
            "argstr": "-datum {datum}",
        },
    ),
    (
        "lin",
        bool,
        {
            "help_string": "3 point linear filter: :math:`0.15\\,a + 0.70\\,b + 0.15\\,c` [This is the default smoother]",
            "argstr": "-lin",
        },
    ),
    (
        "med",
        bool,
        {"help_string": "3 point median filter: median(a,b,c)", "argstr": "-med"},
    ),
    (
        "osf",
        bool,
        {
            "help_string": "3 point order statistics filter::math:`0.15\\,min(a,b,c) + 0.70\\,median(a,b,c) + 0.15\\,max(a,b,c)`",
            "argstr": "-osf",
        },
    ),
    (
        "lin3",
        int,
        {
            "help_string": "3 point linear filter: :math:`0.5\\,(1-m)\\,a + m\\,b + 0.5\\,(1-m)\\,c`. Here, 'm' is a number strictly between 0 and 1.",
            "argstr": "-3lin {lin3}",
        },
    ),
    (
        "hamming",
        int,
        {
            "help_string": "Use N point Hamming windows. (N must be odd and bigger than 1.)",
            "argstr": "-hamming {hamming}",
        },
    ),
    (
        "blackman",
        int,
        {
            "help_string": "Use N point Blackman windows. (N must be odd and bigger than 1.)",
            "argstr": "-blackman {blackman}",
        },
    ),
    (
        "custom",
        File,
        {
            "help_string": "odd # of coefficients must be in a single column in ASCII file",
            "argstr": "-custom {custom}",
        },
    ),
    (
        "adaptive",
        int,
        {
            "help_string": "use adaptive mean filtering of width N (where N must be odd and bigger than 3).",
            "argstr": "-adaptive {adaptive}",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
t_smooth_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
t_smooth_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class t_smooth(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.t_smooth import t_smooth

    >>> task = t_smooth()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.custom = File.mock()
    >>> task.inputs.adaptive = 5
    >>> task.cmdline
    '3dTsmooth -adaptive 5 -prefix functional_smooth functional.nii'


    """

    input_spec = t_smooth_input_spec
    output_spec = t_smooth_output_spec
    executable = "3dTsmooth"


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dTSmooth",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output file from 3dTSmooth",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_smooth",
        },
    ),
    (
        "datum",
        str,
        {
            "help_string": "Sets the data type of the output dataset",
            "argstr": "-datum {datum}",
        },
    ),
    (
        "lin",
        bool,
        {
            "help_string": "3 point linear filter: :math:`0.15\\,a + 0.70\\,b + 0.15\\,c` [This is the default smoother]",
            "argstr": "-lin",
        },
    ),
    (
        "med",
        bool,
        {"help_string": "3 point median filter: median(a,b,c)", "argstr": "-med"},
    ),
    (
        "osf",
        bool,
        {
            "help_string": "3 point order statistics filter::math:`0.15\\,min(a,b,c) + 0.70\\,median(a,b,c) + 0.15\\,max(a,b,c)`",
            "argstr": "-osf",
        },
    ),
    (
        "lin3",
        int,
        {
            "help_string": "3 point linear filter: :math:`0.5\\,(1-m)\\,a + m\\,b + 0.5\\,(1-m)\\,c`. Here, 'm' is a number strictly between 0 and 1.",
            "argstr": "-3lin {lin3}",
        },
    ),
    (
        "hamming",
        int,
        {
            "help_string": "Use N point Hamming windows. (N must be odd and bigger than 1.)",
            "argstr": "-hamming {hamming}",
        },
    ),
    (
        "blackman",
        int,
        {
            "help_string": "Use N point Blackman windows. (N must be odd and bigger than 1.)",
            "argstr": "-blackman {blackman}",
        },
    ),
    (
        "custom",
        File,
        {
            "help_string": "odd # of coefficients must be in a single column in ASCII file",
            "argstr": "-custom {custom}",
        },
    ),
    (
        "adaptive",
        int,
        {
            "help_string": "use adaptive mean filtering of width N (where N must be odd and bigger than 3).",
            "argstr": "-adaptive {adaptive}",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
TSmooth_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
TSmooth_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class TSmooth(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.t_smooth import TSmooth

    >>> task = TSmooth()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.custom = File.mock()
    >>> task.inputs.adaptive = 5
    >>> task.cmdline
    '3dTsmooth -adaptive 5 -prefix functional_smooth functional.nii'


    """

    input_spec = TSmooth_input_spec
    output_spec = TSmooth_output_spec
    executable = "3dTsmooth"
