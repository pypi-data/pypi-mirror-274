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
            "help_string": "input file to 3dAutomask",
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
            "output_file_template": "{in_file}_mask",
        },
    ),
    (
        "brain_file",
        Path,
        {
            "help_string": "output file from 3dAutomask",
            "argstr": "-apply_prefix {brain_file}",
            "output_file_template": "{in_file}_masked",
        },
    ),
    (
        "clfrac",
        float,
        {
            "help_string": "sets the clip level fraction (must be 0.1-0.9). A small value will tend to make the mask larger [default = 0.5].",
            "argstr": "-clfrac {clfrac}",
        },
    ),
    (
        "dilate",
        int,
        {"help_string": "dilate the mask outwards", "argstr": "-dilate {dilate}"},
    ),
    (
        "erode",
        int,
        {"help_string": "erode the mask inwards", "argstr": "-erode {erode}"},
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Automask_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Automask_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Automask(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.automask import Automask

    >>> task = Automask()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.dilate = 1
    >>> task.inputs.outputtype = "NIFTI"
    >>> task.cmdline
    '3dAutomask -apply_prefix functional_masked.nii -dilate 1 -prefix functional_mask.nii functional.nii'


    """

    input_spec = Automask_input_spec
    output_spec = Automask_output_spec
    executable = "3dAutomask"
