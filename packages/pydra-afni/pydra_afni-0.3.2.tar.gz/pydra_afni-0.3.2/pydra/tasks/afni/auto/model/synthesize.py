from fileformats.medimage import Nifti1
from fileformats.medimage_afni import OneD
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "cbucket",
        Nifti1,
        {
            "help_string": "Read the dataset output from 3dDeconvolve via the '-cbucket' option.",
            "argstr": "-cbucket {cbucket}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "matrix",
        OneD,
        {
            "help_string": "Read the matrix output from 3dDeconvolve via the '-x1D' option.",
            "argstr": "-matrix {matrix}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "select",
        list,
        {
            "help_string": "A list of selected columns from the matrix (and the corresponding coefficient sub-bricks from the cbucket). Valid types include 'baseline',  'polort', 'allfunc', 'allstim', 'all', Can also provide 'something' where something matches a stim_label from 3dDeconvolve, and 'digits' where digits are the numbers of the select matrix columns by numbers (starting at 0), or number ranges of the form '3..7' and '3-7'.",
            "argstr": "-select {select}",
            "mandatory": True,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output dataset prefix name (default 'syn')",
            "argstr": "-prefix {out_file}",
            "output_file_template": "syn",
        },
    ),
    (
        "dry_run",
        bool,
        {
            "help_string": "Don't compute the output, just check the inputs.",
            "argstr": "-dry",
        },
    ),
    (
        "TR",
        float,
        {
            "help_string": "TR to set in the output.  The default value of TR is read from the header of the matrix file.",
            "argstr": "-TR {TR}",
        },
    ),
    (
        "cenfill",
        ty.Any,
        {
            "help_string": "Determines how censored time points from the 3dDeconvolve run will be filled. Valid types are 'zero', 'nbhr' and 'none'.",
            "argstr": "-cenfill {cenfill}",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Synthesize_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Synthesize_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Synthesize(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from fileformats.medimage_afni import OneD
    >>> from pydra.tasks.afni.auto.model.synthesize import Synthesize

    >>> task = Synthesize()
    >>> task.inputs.cbucket = Nifti1.mock(None)
    >>> task.inputs.matrix = OneD.mock(None)
    >>> task.inputs.select = ["baseline"]
    >>> task.cmdline
    '3dSynthesize -cbucket functional.nii -matrix output.1D -select baseline'


    """

    input_spec = Synthesize_input_spec
    output_spec = Synthesize_output_spec
    executable = "3dSynthesize"
