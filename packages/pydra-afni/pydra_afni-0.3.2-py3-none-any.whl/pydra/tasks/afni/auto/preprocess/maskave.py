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
            "help_string": "input file to 3dmaskave",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output image file name",
            "argstr": "> {out_file}",
            "position": -1,
            "output_file_template": "{in_file}_maskave.1D",
        },
    ),
    (
        "mask",
        Nifti1,
        {
            "help_string": "matrix to align input file",
            "argstr": "-mask {mask}",
            "position": 1,
        },
    ),
    (
        "quiet",
        bool,
        {
            "help_string": "matrix to align input file",
            "argstr": "-quiet",
            "position": 2,
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Maskave_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Maskave_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Maskave(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.maskave import Maskave

    >>> task = Maskave()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.mask = Nifti1.mock(None)
    >>> task.inputs.quiet = True
    >>> task.cmdline
    '3dmaskave -mask seed_mask.nii -quiet functional.nii > functional_maskave.1D'


    """

    input_spec = Maskave_input_spec
    output_spec = Maskave_output_spec
    executable = "3dmaskave"
