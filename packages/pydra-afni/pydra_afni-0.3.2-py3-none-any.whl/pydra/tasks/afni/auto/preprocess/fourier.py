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
            "help_string": "input file to 3dFourier",
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
            "output_file_template": "{in_file}_fourier",
        },
    ),
    (
        "lowpass",
        float,
        {"help_string": "lowpass", "argstr": "-lowpass {lowpass}", "mandatory": True},
    ),
    (
        "highpass",
        float,
        {
            "help_string": "highpass",
            "argstr": "-highpass {highpass}",
            "mandatory": True,
        },
    ),
    (
        "retrend",
        bool,
        {
            "help_string": "Any mean and linear trend are removed before filtering. This will restore the trend after filtering.",
            "argstr": "-retrend",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Fourier_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Fourier_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Fourier(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.fourier import Fourier

    >>> task = Fourier()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.lowpass = 0.1
    >>> task.inputs.highpass = 0.005
    >>> task.inputs.retrend = True
    >>> task.cmdline
    '3dFourier -highpass 0.005000 -lowpass 0.100000 -prefix functional_fourier -retrend functional.nii'


    """

    input_spec = Fourier_input_spec
    output_spec = Fourier_output_spec
    executable = "3dFourier"
