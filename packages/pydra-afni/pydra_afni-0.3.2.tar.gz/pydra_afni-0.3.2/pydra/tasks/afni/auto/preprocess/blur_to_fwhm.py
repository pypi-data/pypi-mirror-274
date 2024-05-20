from fileformats.generic import File
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
            "help_string": "The dataset that will be smoothed",
            "argstr": "-input {in_file}",
            "mandatory": True,
        },
    ),
    (
        "automask",
        bool,
        {
            "help_string": "Create an automask from the input dataset.",
            "argstr": "-automask",
        },
    ),
    (
        "fwhm",
        float,
        {
            "help_string": "Blur until the 3D FWHM reaches this value (in mm)",
            "argstr": "-FWHM {fwhm}",
        },
    ),
    (
        "fwhmxy",
        float,
        {
            "help_string": "Blur until the 2D (x,y)-plane FWHM reaches this value (in mm)",
            "argstr": "-FWHMxy {fwhmxy}",
        },
    ),
    (
        "blurmaster",
        File,
        {
            "help_string": "The dataset whose smoothness controls the process.",
            "argstr": "-blurmaster {blurmaster}",
        },
    ),
    (
        "mask",
        File,
        {
            "help_string": "Mask dataset, if desired. Voxels NOT in mask will be set to zero in output.",
            "argstr": "-mask {mask}",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
    (
        "out_file",
        Path,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_afni",
        },
    ),
]
BlurToFWHM_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
BlurToFWHM_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class BlurToFWHM(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.blur_to_fwhm import BlurToFWHM

    >>> task = BlurToFWHM()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.fwhm = 2.5
    >>> task.inputs.blurmaster = File.mock()
    >>> task.inputs.mask = File.mock()
    >>> task.cmdline
    '3dBlurToFWHM -FWHM 2.500000 -input epi.nii -prefix epi_afni'


    """

    input_spec = BlurToFWHM_input_spec
    output_spec = BlurToFWHM_output_spec
    executable = "3dBlurToFWHM"
