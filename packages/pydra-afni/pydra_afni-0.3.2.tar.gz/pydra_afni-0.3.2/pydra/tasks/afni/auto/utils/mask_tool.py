from fileformats.medimage import Nifti1
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        ty.List[Nifti1],
        {
            "help_string": "input file or files to 3dmask_tool",
            "argstr": "-input {in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_mask",
        },
    ),
    (
        "count",
        bool,
        {
            "help_string": "Instead of created a binary 0/1 mask dataset, create one with counts of voxel overlap, i.e., each voxel will contain the number of masks that it is set in.",
            "argstr": "-count",
            "position": 2,
        },
    ),
    (
        "datum",
        ty.Any,
        {"help_string": "specify data type for output.", "argstr": "-datum {datum}"},
    ),
    (
        "dilate_inputs",
        str,
        {
            "help_string": "Use this option to dilate and/or erode datasets as they are read. ex. '5 -5' to dilate and erode 5 times",
            "argstr": "-dilate_inputs {dilate_inputs}",
        },
    ),
    (
        "dilate_results",
        str,
        {
            "help_string": "dilate and/or erode combined mask at the given levels.",
            "argstr": "-dilate_results {dilate_results}",
        },
    ),
    (
        "frac",
        float,
        {
            "help_string": "When combining masks (across datasets and sub-bricks), use this option to restrict the result to a certain fraction of the set of volumes",
            "argstr": "-frac {frac}",
        },
    ),
    (
        "inter",
        bool,
        {"help_string": "intersection, this means -frac 1.0", "argstr": "-inter"},
    ),
    ("union", bool, {"help_string": "union, this means -frac 0", "argstr": "-union"}),
    (
        "fill_holes",
        bool,
        {
            "help_string": "This option can be used to fill holes in the resulting mask, i.e. after all other processing has been done.",
            "argstr": "-fill_holes",
        },
    ),
    (
        "fill_dirs",
        str,
        {
            "help_string": "fill holes only in the given directions. This option is for use with -fill holes. should be a single string that specifies 1-3 of the axes using {x,y,z} labels (i.e. dataset axis order), or using the labels in {R,L,A,P,I,S}.",
            "argstr": "-fill_dirs {fill_dirs}",
            "requires": ["fill_holes"],
        },
    ),
    (
        "verbose",
        int,
        {
            "help_string": "specify verbosity level, for 0 to 3",
            "argstr": "-verb {verbose}",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
mask_tool_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
mask_tool_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class mask_tool(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.mask_tool import mask_tool

    >>> task = mask_tool()
    >>> task.inputs.in_file = None
    >>> task.inputs.outputtype = "NIFTI"
    >>> task.cmdline
    '3dmask_tool -prefix functional_mask.nii -input functional.nii'


    """

    input_spec = mask_tool_input_spec
    output_spec = mask_tool_output_spec
    executable = "3dmask_tool"


input_fields = [
    (
        "in_file",
        ty.List[Nifti1],
        {
            "help_string": "input file or files to 3dmask_tool",
            "argstr": "-input {in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_mask",
        },
    ),
    (
        "count",
        bool,
        {
            "help_string": "Instead of created a binary 0/1 mask dataset, create one with counts of voxel overlap, i.e., each voxel will contain the number of masks that it is set in.",
            "argstr": "-count",
            "position": 2,
        },
    ),
    (
        "datum",
        ty.Any,
        {"help_string": "specify data type for output.", "argstr": "-datum {datum}"},
    ),
    (
        "dilate_inputs",
        str,
        {
            "help_string": "Use this option to dilate and/or erode datasets as they are read. ex. '5 -5' to dilate and erode 5 times",
            "argstr": "-dilate_inputs {dilate_inputs}",
        },
    ),
    (
        "dilate_results",
        str,
        {
            "help_string": "dilate and/or erode combined mask at the given levels.",
            "argstr": "-dilate_results {dilate_results}",
        },
    ),
    (
        "frac",
        float,
        {
            "help_string": "When combining masks (across datasets and sub-bricks), use this option to restrict the result to a certain fraction of the set of volumes",
            "argstr": "-frac {frac}",
        },
    ),
    (
        "inter",
        bool,
        {"help_string": "intersection, this means -frac 1.0", "argstr": "-inter"},
    ),
    ("union", bool, {"help_string": "union, this means -frac 0", "argstr": "-union"}),
    (
        "fill_holes",
        bool,
        {
            "help_string": "This option can be used to fill holes in the resulting mask, i.e. after all other processing has been done.",
            "argstr": "-fill_holes",
        },
    ),
    (
        "fill_dirs",
        str,
        {
            "help_string": "fill holes only in the given directions. This option is for use with -fill holes. should be a single string that specifies 1-3 of the axes using {x,y,z} labels (i.e. dataset axis order), or using the labels in {R,L,A,P,I,S}.",
            "argstr": "-fill_dirs {fill_dirs}",
            "requires": ["fill_holes"],
        },
    ),
    (
        "verbose",
        int,
        {
            "help_string": "specify verbosity level, for 0 to 3",
            "argstr": "-verb {verbose}",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
MaskTool_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
MaskTool_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MaskTool(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.mask_tool import MaskTool

    >>> task = MaskTool()
    >>> task.inputs.in_file = None
    >>> task.inputs.outputtype = "NIFTI"
    >>> task.cmdline
    '3dmask_tool -prefix functional_mask.nii -input functional.nii'


    """

    input_spec = MaskTool_input_spec
    output_spec = MaskTool_output_spec
    executable = "3dmask_tool"
