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
            "help_string": "input file to 3dTstat",
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
            "output_file_template": "{in_file}_tstat",
        },
    ),
    ("mask", File, {"help_string": "mask file", "argstr": "-mask {mask}"}),
    (
        "options",
        str,
        {"help_string": "selected statistical output", "argstr": "{options}"},
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
t_stat_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
t_stat_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class t_stat(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.t_stat import t_stat

    >>> task = t_stat()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = None
    >>> task.inputs.mask = File.mock()
    >>> task.cmdline
    '3dTstat -mean -prefix stats functional.nii'


    """

    input_spec = t_stat_input_spec
    output_spec = t_stat_output_spec
    executable = "3dTstat"


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dTstat",
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
            "output_file_template": "{in_file}_tstat",
        },
    ),
    ("mask", File, {"help_string": "mask file", "argstr": "-mask {mask}"}),
    (
        "options",
        str,
        {"help_string": "selected statistical output", "argstr": "{options}"},
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
TStat_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
TStat_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class TStat(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.t_stat import TStat

    >>> task = TStat()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = None
    >>> task.inputs.mask = File.mock()
    >>> task.cmdline
    '3dTstat -mean -prefix stats functional.nii'


    """

    input_spec = TStat_input_spec
    output_spec = TStat_output_spec
    executable = "3dTstat"
