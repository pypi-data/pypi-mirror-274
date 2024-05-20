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
            "help_string": "input file to 3dTNorm",
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
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_tnorm",
        },
    ),
    (
        "norm2",
        bool,
        {
            "help_string": "L2 normalize (sum of squares = 1) [DEFAULT]",
            "argstr": "-norm2",
        },
    ),
    (
        "normR",
        bool,
        {
            "help_string": "normalize so sum of squares = number of time points \\* e.g., so RMS = 1.",
            "argstr": "-normR",
        },
    ),
    (
        "norm1",
        bool,
        {
            "help_string": "L1 normalize (sum of absolute values = 1)",
            "argstr": "-norm1",
        },
    ),
    (
        "normx",
        bool,
        {
            "help_string": "Scale so max absolute value = 1 (L_infinity norm)",
            "argstr": "-normx",
        },
    ),
    (
        "polort",
        int,
        {
            "help_string": "Detrend with polynomials of order p before normalizing [DEFAULT = don't do this].\nUse '-polort 0' to remove the mean, for example",
            "argstr": "-polort {polort}",
        },
    ),
    (
        "L1fit",
        bool,
        {
            "help_string": "Detrend with L1 regression (L2 is the default)\nThis option is here just for the hell of it",
            "argstr": "-L1fit",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
TNorm_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
TNorm_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class TNorm(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.t_norm import TNorm

    >>> task = TNorm()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = None
    >>> task.inputs.norm2 = True
    >>> task.cmdline
    '3dTnorm -norm2 -prefix rm.errts.unit errts+tlrc functional.nii'


    """

    input_spec = TNorm_input_spec
    output_spec = TNorm_output_spec
    executable = "3dTnorm"


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dTNorm",
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
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_tnorm",
        },
    ),
    (
        "norm2",
        bool,
        {
            "help_string": "L2 normalize (sum of squares = 1) [DEFAULT]",
            "argstr": "-norm2",
        },
    ),
    (
        "normR",
        bool,
        {
            "help_string": "normalize so sum of squares = number of time points \\* e.g., so RMS = 1.",
            "argstr": "-normR",
        },
    ),
    (
        "norm1",
        bool,
        {
            "help_string": "L1 normalize (sum of absolute values = 1)",
            "argstr": "-norm1",
        },
    ),
    (
        "normx",
        bool,
        {
            "help_string": "Scale so max absolute value = 1 (L_infinity norm)",
            "argstr": "-normx",
        },
    ),
    (
        "polort",
        int,
        {
            "help_string": "Detrend with polynomials of order p before normalizing [DEFAULT = don't do this].\nUse '-polort 0' to remove the mean, for example",
            "argstr": "-polort {polort}",
        },
    ),
    (
        "L1fit",
        bool,
        {
            "help_string": "Detrend with L1 regression (L2 is the default)\nThis option is here just for the hell of it",
            "argstr": "-L1fit",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
t_norm_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
t_norm_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class t_norm(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.t_norm import t_norm

    >>> task = t_norm()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = None
    >>> task.inputs.norm2 = True
    >>> task.cmdline
    '3dTnorm -norm2 -prefix rm.errts.unit errts+tlrc functional.nii'


    """

    input_spec = t_norm_input_spec
    output_spec = t_norm_output_spec
    executable = "3dTnorm"
