from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dHist",
            "argstr": "-input {in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Write histogram to niml file with this prefix",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_hist",
        },
    ),
    (
        "showhist",
        bool,
        False,
        {"help_string": "write a text visual histogram", "argstr": "-showhist"},
    ),
    (
        "out_show",
        Path,
        {
            "help_string": "output image file name",
            "argstr": "> {out_show}",
            "position": -1,
            "output_file_template": "{in_file}_hist.out",
        },
    ),
    (
        "mask",
        File,
        {"help_string": "matrix to align input file", "argstr": "-mask {mask}"},
    ),
    ("nbin", int, {"help_string": "number of bins", "argstr": "-nbin {nbin}"}),
    (
        "max_value",
        float,
        {"help_string": "maximum intensity value", "argstr": "-max {max_value}"},
    ),
    (
        "min_value",
        float,
        {"help_string": "minimum intensity value", "argstr": "-min {min_value}"},
    ),
    (
        "bin_width",
        float,
        {"help_string": "bin width", "argstr": "-binwidth {bin_width}"},
    ),
]
Hist_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Hist_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Hist(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.hist import Hist

    >>> task = Hist()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.mask = File.mock()
    >>> task.cmdline
    '3dHist -input functional.nii -prefix functional_hist'


    """

    input_spec = Hist_input_spec
    output_spec = Hist_output_spec
    executable = "3dHist"
