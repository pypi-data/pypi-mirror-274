from fileformats.generic import File
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
            "help_string": "ANAT is the volume to segment",
            "argstr": "-anat {in_file}",
            "copyfile": True,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "mask",
        ty.Any,
        {
            "help_string": 'only non-zero voxels in mask are analyzed. mask can either be a dataset or the string "AUTO" which would use AFNI\'s automask function to create the mask.',
            "argstr": "-mask {mask}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "blur_meth",
        ty.Any,
        {
            "help_string": "set the blurring method for bias field estimation",
            "argstr": "-blur_meth {blur_meth}",
        },
    ),
    (
        "bias_fwhm",
        float,
        {
            "help_string": "The amount of blurring used when estimating the field bias with the Wells method",
            "argstr": "-bias_fwhm {bias_fwhm}",
        },
    ),
    (
        "classes",
        str,
        {
            "help_string": "CLASS_STRING is a semicolon delimited string of class labels",
            "argstr": "-classes {classes}",
        },
    ),
    (
        "bmrf",
        float,
        {
            "help_string": "Weighting factor controlling spatial homogeneity of the classifications",
            "argstr": "-bmrf {bmrf}",
        },
    ),
    (
        "bias_classes",
        str,
        {
            "help_string": "A semicolon delimited string of classes that contribute to the estimation of the bias field",
            "argstr": "-bias_classes {bias_classes}",
        },
    ),
    (
        "prefix",
        str,
        {
            "help_string": "the prefix for the output folder containing all output volumes",
            "argstr": "-prefix {prefix}",
        },
    ),
    (
        "mixfrac",
        str,
        {
            "help_string": "MIXFRAC sets up the volume-wide (within mask) tissue fractions while initializing the segmentation (see IGNORE for exception)",
            "argstr": "-mixfrac {mixfrac}",
        },
    ),
    (
        "mixfloor",
        float,
        {
            "help_string": "Set the minimum value for any class's mixing fraction",
            "argstr": "-mixfloor {mixfloor}",
        },
    ),
    (
        "main_N",
        int,
        {
            "help_string": "Number of iterations to perform.",
            "argstr": "-main_N {main_N}",
        },
    ),
]
Seg_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", File, {"help_string": "output file"})]
Seg_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Seg(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.seg import Seg

    >>> task = Seg()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.mask = "AUTO"
    >>> task.cmdline
    '3dSeg -mask AUTO -anat structural.nii'


    """

    input_spec = Seg_input_spec
    output_spec = Seg_output_spec
    executable = "3dSeg"
