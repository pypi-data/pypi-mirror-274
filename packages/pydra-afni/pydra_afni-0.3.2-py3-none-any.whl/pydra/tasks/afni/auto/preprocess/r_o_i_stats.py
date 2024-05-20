from fileformats.generic import File
from fileformats.medimage import Nifti1, NiftiGz
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
            "help_string": "input dataset",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "mask",
        File,
        {"help_string": "input mask", "argstr": "-mask {mask}", "position": 3},
    ),
    (
        "mask_file",
        NiftiGz,
        {"help_string": "input mask", "argstr": "-mask {mask_file}"},
    ),
    (
        "mask_f2short",
        bool,
        {
            "help_string": "Tells the program to convert a float mask to short integers, by simple rounding.",
            "argstr": "-mask_f2short",
        },
    ),
    (
        "num_roi",
        int,
        {
            "help_string": "Forces the assumption that the mask dataset's ROIs are denoted by 1 to n inclusive.  Normally, the program figures out the ROIs on its own.  This option is useful if a) you are certain that the mask dataset has no values outside the range [0 n], b) there may be some ROIs missing between [1 n] in the mask data-set and c) you want those columns in the output any-way so the output lines up with the output from other invocations of 3dROIstats.",
            "argstr": "-numroi {num_roi}",
        },
    ),
    (
        "zerofill",
        str,
        {
            "help_string": "For ROI labels not found, use the provided string instead of a '0' in the output file. Only active if `num_roi` is enabled.",
            "argstr": "-zerofill {zerofill}",
            "requires": ["num_roi"],
        },
    ),
    (
        "roisel",
        File,
        {
            "help_string": "Only considers ROIs denoted by values found in the specified file. Note that the order of the ROIs as specified in the file is not preserved. So an SEL.1D of '2 8 20' produces the same output as '8 20 2'",
            "argstr": "-roisel {roisel}",
        },
    ),
    ("debug", bool, {"help_string": "print debug information", "argstr": "-debug"}),
    ("quiet", bool, {"help_string": "execute quietly", "argstr": "-quiet"}),
    (
        "nomeanout",
        bool,
        {
            "help_string": "Do not include the (zero-inclusive) mean among computed stats",
            "argstr": "-nomeanout",
        },
    ),
    (
        "nobriklab",
        bool,
        {
            "help_string": "Do not print the sub-brick label next to its index",
            "argstr": "-nobriklab",
        },
    ),
    (
        "format1D",
        bool,
        {
            "help_string": "Output results in a 1D format that includes commented labels",
            "argstr": "-1Dformat",
            "xor": ["format1DR"],
        },
    ),
    (
        "format1DR",
        bool,
        {
            "help_string": "Output results in a 1D format that includes uncommented labels. May not work optimally with typical 1D functions, but is useful for R functions.",
            "argstr": "-1DRformat",
            "xor": ["format1D"],
        },
    ),
    (
        "stat",
        ty.List[File],
        {
            "help_string": "Statistics to compute. Options include:\n\n * mean       =   Compute the mean using only non_zero voxels.\n                  Implies the opposite for the mean computed\n                  by default.\n * median     =   Compute the median of nonzero voxels\n * mode       =   Compute the mode of nonzero voxels.\n                  (integral valued sets only)\n * minmax     =   Compute the min/max of nonzero voxels\n * sum        =   Compute the sum using only nonzero voxels.\n * voxels     =   Compute the number of nonzero voxels\n * sigma      =   Compute the standard deviation of nonzero\n                  voxels\n\nStatistics that include zero-valued voxels:\n\n * zerominmax =   Compute the min/max of all voxels.\n * zerosigma  =   Compute the standard deviation of all\n                  voxels.\n * zeromedian =   Compute the median of all voxels.\n * zeromode   =   Compute the mode of all voxels.\n * summary    =   Only output a summary line with the grand\n                  mean across all briks in the input dataset.\n                  This option cannot be used with nomeanout.\n\nMore that one option can be specified.",
            "argstr": "{stat}...",
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output file",
            "argstr": "> {out_file}",
            "position": -1,
            "output_file_template": "{in_file}_roistat.1D",
        },
    ),
]
r_o_i_stats_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
r_o_i_stats_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class r_o_i_stats(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1, NiftiGz
    >>> from pydra.tasks.afni.auto.preprocess.r_o_i_stats import r_o_i_stats

    >>> task = r_o_i_stats()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.mask = File.mock()
    >>> task.inputs.mask_file = NiftiGz.mock(None)
    >>> task.inputs.roisel = File.mock()
    >>> task.inputs.nomeanout = True
    >>> task.inputs.stat = None
    >>> task.cmdline
    '3dROIstats -mask skeleton_mask.nii.gz -nomeanout -nzmean -nzmedian -nzvoxels functional.nii > functional_roistat.1D'


    """

    input_spec = r_o_i_stats_input_spec
    output_spec = r_o_i_stats_output_spec
    executable = "3dROIstats"
