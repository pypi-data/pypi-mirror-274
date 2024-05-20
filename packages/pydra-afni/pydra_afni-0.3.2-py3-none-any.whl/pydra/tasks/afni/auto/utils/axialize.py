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
            "help_string": "input file to 3daxialize",
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
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_axialize",
        },
    ),
    ("verb", bool, {"help_string": "Print out a progerss report", "argstr": "-verb"}),
    (
        "sagittal",
        bool,
        {
            "help_string": "Do sagittal slice order [-orient ASL]",
            "argstr": "-sagittal",
            "xor": ["coronal", "axial"],
        },
    ),
    (
        "coronal",
        bool,
        {
            "help_string": "Do coronal slice order  [-orient RSA]",
            "argstr": "-coronal",
            "xor": ["sagittal", "axial"],
        },
    ),
    (
        "axial",
        bool,
        {
            "help_string": "Do axial slice order    [-orient RAI]This is the default AFNI axial order, andis the one currently required by thevolume rendering plugin; this is alsothe default orientation output by thisprogram (hence the program's name).",
            "argstr": "-axial",
            "xor": ["coronal", "sagittal"],
        },
    ),
    (
        "orientation",
        str,
        {"help_string": "new orientation code", "argstr": "-orient {orientation}"},
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Axialize_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Axialize_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Axialize(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.axialize import Axialize

    >>> task = Axialize()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.cmdline
    '3daxialize -prefix axialized.nii functional.nii'


    """

    input_spec = Axialize_input_spec
    output_spec = Axialize_output_spec
    executable = "3daxialize"
