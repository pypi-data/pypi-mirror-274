from fileformats.medimage import Nifti1, NiftiGz
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "xset",
        Nifti1,
        {
            "help_string": "input xset",
            "argstr": "{xset}",
            "copyfile": False,
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "yset",
        Nifti1,
        {
            "help_string": "input yset",
            "argstr": "{yset}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_file",
        NiftiGz,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{xset}_tcorr",
        },
    ),
    (
        "pearson",
        bool,
        {
            "help_string": "Correlation is the normal Pearson correlation coefficient",
            "argstr": "-pearson",
        },
    ),
    (
        "polort",
        int,
        {
            "help_string": "Remove polynomical trend of order m",
            "argstr": "-polort {polort}",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
t_correlate_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
t_correlate_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class t_correlate(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1, NiftiGz
    >>> from pydra.tasks.afni.auto.preprocess.t_correlate import t_correlate

    >>> task = t_correlate()
    >>> task.inputs.xset = Nifti1.mock(None)
    >>> task.inputs.yset = Nifti1.mock(None)
    >>> task.inputs.out_file = NiftiGz.mock(None)
    >>> task.inputs.pearson = True
    >>> task.inputs.polort = -1
    >>> task.cmdline
    '3dTcorrelate -prefix functional_tcorrelate.nii.gz -pearson -polort -1 u_rc1s1_Template.nii u_rc1s2_Template.nii'


    """

    input_spec = t_correlate_input_spec
    output_spec = t_correlate_output_spec
    executable = "3dTcorrelate"


input_fields = [
    (
        "xset",
        Nifti1,
        {
            "help_string": "input xset",
            "argstr": "{xset}",
            "copyfile": False,
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "yset",
        Nifti1,
        {
            "help_string": "input yset",
            "argstr": "{yset}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_file",
        NiftiGz,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{xset}_tcorr",
        },
    ),
    (
        "pearson",
        bool,
        {
            "help_string": "Correlation is the normal Pearson correlation coefficient",
            "argstr": "-pearson",
        },
    ),
    (
        "polort",
        int,
        {
            "help_string": "Remove polynomical trend of order m",
            "argstr": "-polort {polort}",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
TCorrelate_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
TCorrelate_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class TCorrelate(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1, NiftiGz
    >>> from pydra.tasks.afni.auto.preprocess.t_correlate import TCorrelate

    >>> task = TCorrelate()
    >>> task.inputs.xset = Nifti1.mock(None)
    >>> task.inputs.yset = Nifti1.mock(None)
    >>> task.inputs.out_file = NiftiGz.mock(None)
    >>> task.inputs.pearson = True
    >>> task.inputs.polort = -1
    >>> task.cmdline
    '3dTcorrelate -prefix functional_tcorrelate.nii.gz -pearson -polort -1 u_rc1s1_Template.nii u_rc1s2_Template.nii'


    """

    input_spec = TCorrelate_input_spec
    output_spec = TCorrelate_output_spec
    executable = "3dTcorrelate"
