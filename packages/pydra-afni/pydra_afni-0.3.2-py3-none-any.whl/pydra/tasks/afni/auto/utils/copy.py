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
            "help_string": "input file to 3dcopy",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Nifti1,
        {
            "help_string": "output image file name",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": "{in_file}_copy",
        },
    ),
    ("verbose", bool, {"help_string": "print progress reports", "argstr": "-verb"}),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Copy_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Copy_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Copy(ShellCommandTask):
    """
    Examples
    -------

    >>> from copy import deepcopy
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.copy import Copy

    >>> task = Copy()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = Nifti1.mock()
    >>> task.cmdline
    '3dcopy functional.nii functional_copy'


    >>> task = Copy()
    >>> task.inputs.in_file = Nifti1.mock()
    >>> task.inputs.out_file = Nifti1.mock()
    >>> task.inputs.outputtype = "NIFTI"
    >>> task.cmdline
    '3dcopy functional.nii functional_copy.nii'


    >>> task = Copy()
    >>> task.inputs.in_file = Nifti1.mock()
    >>> task.inputs.out_file = Nifti1.mock()
    >>> task.inputs.outputtype = "NIFTI_GZ"
    >>> task.cmdline
    '3dcopy functional.nii functional_copy.nii.gz'


    >>> task = Copy()
    >>> task.inputs.in_file = Nifti1.mock()
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.cmdline
    '3dcopy functional.nii new_func.nii'


    """

    input_spec = Copy_input_spec
    output_spec = Copy_output_spec
    executable = "3dcopy"
