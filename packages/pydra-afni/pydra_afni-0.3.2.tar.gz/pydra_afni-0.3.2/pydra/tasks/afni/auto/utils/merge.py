from fileformats.medimage import Nifti1
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_files",
        ty.List[Nifti1],
        {
            "help_string": "",
            "argstr": "{in_files}",
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
            "output_file_template": "{in_files}_merge",
        },
    ),
    (
        "doall",
        bool,
        {
            "help_string": "apply options to all sub-bricks in dataset",
            "argstr": "-doall",
        },
    ),
    (
        "blurfwhm",
        int,
        {"help_string": "FWHM blur value (mm)", "argstr": "-1blur_fwhm {blurfwhm}"},
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Merge_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Merge_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Merge(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.merge import Merge

    >>> task = Merge()
    >>> task.inputs.in_files = None
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.inputs.doall = True
    >>> task.inputs.blurfwhm = 4
    >>> task.cmdline
    '3dmerge -1blur_fwhm 4 -doall -prefix e7.nii functional.nii functional2.nii'


    """

    input_spec = Merge_input_spec
    output_spec = Merge_output_spec
    executable = "3dmerge"
