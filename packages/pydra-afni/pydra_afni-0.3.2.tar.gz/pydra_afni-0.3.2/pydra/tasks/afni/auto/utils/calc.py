from fileformats.generic import File
from fileformats.medimage import Nifti1, NiftiGz
from fileformats.medimage_afni import All1
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file_a",
        Nifti1,
        {
            "help_string": "input file to 3dcalc",
            "argstr": "-a {in_file_a}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "in_file_b",
        Nifti1,
        {
            "help_string": "operand file to 3dcalc",
            "argstr": "-b {in_file_b}",
            "position": 1,
        },
    ),
    (
        "in_file_c",
        File,
        {
            "help_string": "operand file to 3dcalc",
            "argstr": "-c {in_file_c}",
            "position": 2,
        },
    ),
    (
        "out_file",
        ty.Union[All1, NiftiGz],
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file_a}_calc",
        },
    ),
    (
        "expr",
        str,
        {
            "help_string": "expr",
            "argstr": '-expr "{expr}"',
            "mandatory": True,
            "position": 3,
        },
    ),
    (
        "start_idx",
        int,
        {"help_string": "start index for in_file_a", "requires": ["stop_idx"]},
    ),
    (
        "stop_idx",
        int,
        {"help_string": "stop index for in_file_a", "requires": ["start_idx"]},
    ),
    ("single_idx", int, {"help_string": "volume index for in_file_a"}),
    ("overwrite", bool, {"help_string": "overwrite output", "argstr": "-overwrite"}),
    ("other", File, {"help_string": "other options", "argstr": ""}),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Calc_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Calc_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Calc(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1, NiftiGz
    >>> from fileformats.medimage_afni import All1
    >>> from pydra.tasks.afni.auto.utils.calc import Calc

    >>> task = Calc()
    >>> task.inputs.in_file_a = Nifti1.mock(None)
    >>> task.inputs.in_file_b = Nifti1.mock(None)
    >>> task.inputs.in_file_c = File.mock()
    >>> task.inputs.out_file = None
    >>> task.inputs.expr = "a*b"
    >>> task.inputs.other = File.mock()
    >>> task.inputs.outputtype = "NIFTI"
    >>> task.cmdline
    '3dcalc -a functional.nii -b functional2.nii -expr "a*b" -prefix functional_calc.nii.gz'


    >>> task = Calc()
    >>> task.inputs.in_file_a = Nifti1.mock(None)
    >>> task.inputs.in_file_b = Nifti1.mock()
    >>> task.inputs.in_file_c = File.mock()
    >>> task.inputs.out_file = None
    >>> task.inputs.expr = "1"
    >>> task.inputs.overwrite = True
    >>> task.inputs.other = File.mock()
    >>> task.cmdline
    '3dcalc -a functional.nii -expr "1" -prefix rm.epi.all1 -overwrite'


    """

    input_spec = Calc_input_spec
    output_spec = Calc_output_spec
    executable = "3dcalc"
