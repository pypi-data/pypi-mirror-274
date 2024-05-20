from fileformats.generic import File
from fileformats.medimage import Nifti
from fileformats.text import TextFile
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_files",
        ty.List[Nifti],
        {
            "help_string": "list of input files, possibly with subbrick selectors",
            "argstr": "{in_files} ...",
            "position": -2,
        },
    ),
    (
        "out_file",
        TextFile,
        {
            "help_string": "collect output to a file",
            "argstr": " |& tee {out_file}",
            "position": -1,
        },
    ),
    (
        "mask",
        File,
        {"help_string": "Use this dataset as a mask", "argstr": "-mask {mask}"},
    ),
    (
        "mrange",
        ty.Any,
        {
            "help_string": "Means to further restrict the voxels from 'mset' so thatonly those mask values within this range (inclusive) willbe used.",
            "argstr": "-mrange {mrange[0]} {mrange[1]}",
        },
    ),
    (
        "demean",
        bool,
        {
            "help_string": "Remove the mean from each volume prior to computing the correlation",
            "argstr": "-demean",
        },
    ),
    (
        "docor",
        bool,
        {
            "help_string": "Return the correlation coefficient (default).",
            "argstr": "-docor",
        },
    ),
    (
        "dodot",
        bool,
        {"help_string": "Return the dot product (unscaled).", "argstr": "-dodot"},
    ),
    (
        "docoef",
        bool,
        {
            "help_string": "Return the least square fit coefficients {{a,b}} so that dset2 is approximately a + b\\*dset1",
            "argstr": "-docoef",
        },
    ),
    (
        "dosums",
        bool,
        {
            "help_string": "Return the 6 numbers xbar=<x> ybar=<y> <(x-xbar)^2> <(y-ybar)^2> <(x-xbar)(y-ybar)> and the correlation coefficient.",
            "argstr": "-dosums",
        },
    ),
    (
        "dodice",
        bool,
        {
            "help_string": "Return the Dice coefficient (the Sorensen-Dice index).",
            "argstr": "-dodice",
        },
    ),
    (
        "doeta2",
        bool,
        {
            "help_string": "Return eta-squared (Cohen, NeuroImage 2008).",
            "argstr": "-doeta2",
        },
    ),
    (
        "full",
        bool,
        {
            "help_string": "Compute the whole matrix. A waste of time, but handy for parsing.",
            "argstr": "-full",
        },
    ),
    (
        "show_labels",
        bool,
        {
            "help_string": "Print sub-brick labels to help identify what is being correlated. This option is useful whenyou have more than 2 sub-bricks at input.",
            "argstr": "-show_labels",
        },
    ),
    (
        "upper",
        bool,
        {"help_string": "Compute upper triangular matrix", "argstr": "-upper"},
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Dot_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", TextFile, {"help_string": "output file"})]
Dot_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Dot(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.afni.auto.utils.dot import Dot

    >>> task = Dot()
    >>> task.inputs.in_files = None
    >>> task.inputs.out_file = TextFile.mock(None)
    >>> task.inputs.mask = File.mock()
    >>> task.inputs.dodice = True
    >>> task.cmdline
    '3dDot -dodice functional.nii[0] structural.nii |& tee out.mask_ae_dice.txt'


    """

    input_spec = Dot_input_spec
    output_spec = Dot_output_spec
    executable = "3dDot"
