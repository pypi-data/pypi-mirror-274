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
            "help_string": "input file to 3dLFCD",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "mask",
        Nifti1,
        {"help_string": "mask file to mask input data", "argstr": "-mask {mask}"},
    ),
    (
        "thresh",
        float,
        {
            "help_string": "threshold to exclude connections where corr <= thresh",
            "argstr": "-thresh {thresh}",
        },
    ),
    ("polort", int, {"help_string": "", "argstr": "-polort {polort}"}),
    (
        "autoclip",
        bool,
        {
            "help_string": "Clip off low-intensity regions in the dataset",
            "argstr": "-autoclip",
        },
    ),
    (
        "automask",
        bool,
        {
            "help_string": "Mask the dataset to target brain-only voxels",
            "argstr": "-automask",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
    (
        "out_file",
        Nifti1,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_afni",
        },
    ),
]
LFCD_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
LFCD_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class LFCD(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.lfcd import LFCD

    >>> task = LFCD()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.mask = Nifti1.mock(None)
    >>> task.inputs.thresh = 0.8 # keep all connections with corr >= 0.8
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.cmdline
    '3dLFCD -mask mask.nii -prefix out.nii -thresh 0.800000 functional.nii'


    """

    input_spec = LFCD_input_spec
    output_spec = LFCD_output_spec
    executable = "3dLFCD"
