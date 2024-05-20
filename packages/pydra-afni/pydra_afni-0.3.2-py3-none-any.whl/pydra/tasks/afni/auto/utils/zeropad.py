from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_files",
        Nifti1,
        {
            "help_string": "input dataset",
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
            "help_string": "output dataset prefix name (default 'zeropad')",
            "argstr": "-prefix {out_file}",
            "output_file_template": "zeropad",
        },
    ),
    (
        "I",
        int,
        {
            "help_string": "adds 'n' planes of zero at the Inferior edge",
            "argstr": "-I {I}",
            "xor": ["master"],
        },
    ),
    (
        "S",
        int,
        {
            "help_string": "adds 'n' planes of zero at the Superior edge",
            "argstr": "-S {S}",
            "xor": ["master"],
        },
    ),
    (
        "A",
        int,
        {
            "help_string": "adds 'n' planes of zero at the Anterior edge",
            "argstr": "-A {A}",
            "xor": ["master"],
        },
    ),
    (
        "P",
        int,
        {
            "help_string": "adds 'n' planes of zero at the Posterior edge",
            "argstr": "-P {P}",
            "xor": ["master"],
        },
    ),
    (
        "L",
        int,
        {
            "help_string": "adds 'n' planes of zero at the Left edge",
            "argstr": "-L {L}",
            "xor": ["master"],
        },
    ),
    (
        "R",
        int,
        {
            "help_string": "adds 'n' planes of zero at the Right edge",
            "argstr": "-R {R}",
            "xor": ["master"],
        },
    ),
    (
        "z",
        int,
        {
            "help_string": "adds 'n' planes of zero on EACH of the dataset z-axis (slice-direction) faces",
            "argstr": "-z {z}",
            "xor": ["master"],
        },
    ),
    (
        "RL",
        int,
        {
            "help_string": "specify that planes should be added or cut symmetrically to make the resulting volume haveN slices in the right-left direction",
            "argstr": "-RL {RL}",
            "xor": ["master"],
        },
    ),
    (
        "AP",
        int,
        {
            "help_string": "specify that planes should be added or cut symmetrically to make the resulting volume haveN slices in the anterior-posterior direction",
            "argstr": "-AP {AP}",
            "xor": ["master"],
        },
    ),
    (
        "IS",
        int,
        {
            "help_string": "specify that planes should be added or cut symmetrically to make the resulting volume haveN slices in the inferior-superior direction",
            "argstr": "-IS {IS}",
            "xor": ["master"],
        },
    ),
    (
        "mm",
        bool,
        {
            "help_string": "pad counts 'n' are in mm instead of slices, where each 'n' is an integer and at least 'n' mm of slices will be added/removed; e.g., n =  3 and slice thickness = 2.5 mm ==> 2 slices added",
            "argstr": "-mm",
            "xor": ["master"],
        },
    ),
    (
        "master",
        File,
        {
            "help_string": "match the volume described in dataset 'mset', where mset must have the same orientation and grid spacing as dataset to be padded. the goal of -master is to make the output dataset from 3dZeropad match the spatial 'extents' of mset by adding or subtracting slices as needed. You can't use -I,-S,..., or -mm with -master",
            "argstr": "-master {master}",
            "xor": ["I", "S", "A", "P", "L", "R", "z", "RL", "AP", "IS", "mm"],
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Zeropad_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Zeropad_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Zeropad(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.zeropad import Zeropad

    >>> task = Zeropad()
    >>> task.inputs.in_files = Nifti1.mock(None)
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.inputs.I = 10
    >>> task.inputs.S = 10
    >>> task.inputs.A = 10
    >>> task.inputs.P = 10
    >>> task.inputs.L = 10
    >>> task.inputs.R = 10
    >>> task.inputs.master = File.mock()
    >>> task.cmdline
    '3dZeropad -A 10 -I 10 -L 10 -P 10 -R 10 -S 10 -prefix pad_functional.nii functional.nii'


    """

    input_spec = Zeropad_input_spec
    output_spec = Zeropad_output_spec
    executable = "3dZeropad"
