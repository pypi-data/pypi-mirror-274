from fileformats.medimage import Nifti1
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dZcutup",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_file",
        Nifti1,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_zcutup",
        },
    ),
    (
        "keep",
        str,
        {"help_string": "slice range to keep in output", "argstr": "-keep {keep}"},
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
ZCutUp_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ZCutUp_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ZCutUp(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.z_cut_up import ZCutUp

    >>> task = ZCutUp()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.inputs.keep = "0 10"
    >>> task.cmdline
    '3dZcutup -keep 0 10 -prefix functional_zcutup.nii functional.nii'


    """

    input_spec = ZCutUp_input_spec
    output_spec = ZCutUp_output_spec
    executable = "3dZcutup"


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dZcutup",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_file",
        Nifti1,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_zcutup",
        },
    ),
    (
        "keep",
        str,
        {"help_string": "slice range to keep in output", "argstr": "-keep {keep}"},
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
z_cut_up_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
z_cut_up_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class z_cut_up(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.z_cut_up import z_cut_up

    >>> task = z_cut_up()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.inputs.keep = "0 10"
    >>> task.cmdline
    '3dZcutup -keep 0 10 -prefix functional_zcutup.nii functional.nii'


    """

    input_spec = z_cut_up_input_spec
    output_spec = z_cut_up_output_spec
    executable = "3dZcutup"
