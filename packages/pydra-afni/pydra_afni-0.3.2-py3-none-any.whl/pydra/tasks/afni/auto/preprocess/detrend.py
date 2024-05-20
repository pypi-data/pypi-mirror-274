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
            "help_string": "input file to 3dDetrend",
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
            "output_file_template": "{in_file}_detrend",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Detrend_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Detrend_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Detrend(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.detrend import Detrend

    >>> task = Detrend()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.outputtype = "AFNI"
    >>> task.cmdline
    '3dDetrend -polort 2 -prefix functional_detrend functional.nii'


    """

    input_spec = Detrend_input_spec
    output_spec = Detrend_output_spec
    executable = "3dDetrend"
