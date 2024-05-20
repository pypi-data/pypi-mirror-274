from fileformats.medimage import Nifti1
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file_a",
        Nifti1,
        {
            "help_string": "input file to 3dMean",
            "argstr": "{in_file_a}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "in_file_b",
        Nifti1,
        {
            "help_string": "another input file to 3dMean",
            "argstr": "{in_file_b}",
            "position": -1,
        },
    ),
    (
        "datum",
        str,
        {
            "help_string": "Sets the data type of the output dataset",
            "argstr": "-datum {datum}",
        },
    ),
    (
        "out_file",
        Nifti1,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file_a}_mean",
        },
    ),
    ("scale", str, {"help_string": "scaling of output", "argstr": "-{scale}scale"}),
    (
        "non_zero",
        bool,
        {"help_string": "use only non-zero values", "argstr": "-non_zero"},
    ),
    ("std_dev", bool, {"help_string": "calculate std dev", "argstr": "-stdev"}),
    ("sqr", bool, {"help_string": "mean square instead of value", "argstr": "-sqr"}),
    ("summ", bool, {"help_string": "take sum, (not average)", "argstr": "-sum"}),
    (
        "count",
        bool,
        {"help_string": "compute count of non-zero voxels", "argstr": "-count"},
    ),
    (
        "mask_inter",
        bool,
        {"help_string": "create intersection mask", "argstr": "-mask_inter"},
    ),
    ("mask_union", bool, {"help_string": "create union mask", "argstr": "-mask_union"}),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Means_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Means_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Means(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.means import Means

    >>> task = Means()
    >>> task.inputs.in_file_a = Nifti1.mock(None)
    >>> task.inputs.in_file_b = Nifti1.mock(None)
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.cmdline
    '3dMean -prefix output.nii im1.nii im2.nii'


    >>> task = Means()
    >>> task.inputs.in_file_a = Nifti1.mock(None)
    >>> task.inputs.in_file_b = Nifti1.mock()
    >>> task.inputs.datum = "short"
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.cmdline
    '3dMean -datum short -prefix output.nii im1.nii'


    """

    input_spec = Means_input_spec
    output_spec = Means_output_spec
    executable = "3dMean"
