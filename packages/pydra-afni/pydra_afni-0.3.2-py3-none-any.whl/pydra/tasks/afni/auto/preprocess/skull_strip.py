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
            "help_string": "input file to 3dSkullStrip",
            "argstr": "-input {in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_skullstrip",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
skull_strip_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
skull_strip_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class skull_strip(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.skull_strip import skull_strip

    >>> task = skull_strip()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.cmdline
    '3dSkullStrip -input functional.nii -o_ply -prefix functional_skullstrip'


    """

    input_spec = skull_strip_input_spec
    output_spec = skull_strip_output_spec
    executable = "3dSkullStrip"


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dSkullStrip",
            "argstr": "-input {in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_skullstrip",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
SkullStrip_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
SkullStrip_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SkullStrip(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.skull_strip import SkullStrip

    >>> task = SkullStrip()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.cmdline
    '3dSkullStrip -input functional.nii -o_ply -prefix functional_skullstrip'


    """

    input_spec = SkullStrip_input_spec
    output_spec = SkullStrip_output_spec
    executable = "3dSkullStrip"
