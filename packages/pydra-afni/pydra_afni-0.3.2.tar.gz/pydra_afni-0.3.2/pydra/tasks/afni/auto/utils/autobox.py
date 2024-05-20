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
            "help_string": "input file",
            "argstr": "-input {in_file}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "padding",
        int,
        {
            "help_string": "Number of extra voxels to pad on each side of box",
            "argstr": "-npad {padding}",
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_autobox",
        },
    ),
    (
        "no_clustering",
        bool,
        {
            "help_string": "Don't do any clustering to find box. Any non-zero voxel will be preserved in the cropped volume. The default method uses some clustering to find the cropping box, and will clip off small isolated blobs.",
            "argstr": "-noclust",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Autobox_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("x_min", int, {}),
    ("x_max", int, {}),
    ("y_min", int, {}),
    ("y_max", int, {}),
    ("z_min", int, {}),
    ("z_max", int, {}),
]
Autobox_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Autobox(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.autobox import Autobox

    >>> task = Autobox()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.padding = 5
    >>> task.cmdline
    '3dAutobox -input structural.nii -prefix structural_autobox -npad 5'


    """

    input_spec = Autobox_input_spec
    output_spec = Autobox_output_spec
    executable = "3dAutobox"
