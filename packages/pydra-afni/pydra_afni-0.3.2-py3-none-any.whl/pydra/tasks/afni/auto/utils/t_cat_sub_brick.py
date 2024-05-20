import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_files",
        list,
        {
            "help_string": "List of tuples of file names and subbrick selectors as strings.Don't forget to protect the single quotes in the subbrick selectorso the contents are protected from the command line interpreter.",
            "argstr": "{in_files[0]}{in_files[1]} ...",
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
            "output_file_template": '"functional_tcat.nii"',
        },
    ),
    (
        "rlt",
        ty.Any,
        {
            "help_string": "Remove linear trends in each voxel time series loaded from each input dataset, SEPARATELY. Option -rlt removes the least squares fit of 'a+b*t' to each voxel time series. Option -rlt+ adds dataset mean back in. Option -rlt++ adds overall mean of all dataset timeseries back in.",
            "argstr": "-rlt{rlt}",
            "position": 1,
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
TCatSubBrick_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
TCatSubBrick_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class TCatSubBrick(ShellCommandTask):
    """
    Examples
    -------

    >>> from pydra.tasks.afni.auto.utils.t_cat_sub_brick import TCatSubBrick

    >>> task = TCatSubBrick()
    >>> task.inputs.in_files = [('functional.nii', "'{2..$}'"), ('functional2.nii', "'{2..$}'")]
    >>> task.inputs.out_file = "functional_tcat.nii"
    >>> task.inputs.rlt = "+"
    >>> task.cmdline
    '3dTcat -rlt+ -prefix functional_tcat.nii functional.nii"{2..$}" functional2.nii"{2..$}" '


    """

    input_spec = TCatSubBrick_input_spec
    output_spec = TCatSubBrick_output_spec
    executable = "3dTcat"


input_fields = [
    (
        "in_files",
        list,
        {
            "help_string": "List of tuples of file names and subbrick selectors as strings.Don't forget to protect the single quotes in the subbrick selectorso the contents are protected from the command line interpreter.",
            "argstr": "{in_files[0]}{in_files[1]} ...",
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
            "output_file_template": '"functional_tcat.nii"',
        },
    ),
    (
        "rlt",
        ty.Any,
        {
            "help_string": "Remove linear trends in each voxel time series loaded from each input dataset, SEPARATELY. Option -rlt removes the least squares fit of 'a+b*t' to each voxel time series. Option -rlt+ adds dataset mean back in. Option -rlt++ adds overall mean of all dataset timeseries back in.",
            "argstr": "-rlt{rlt}",
            "position": 1,
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
t_cat_sub_brick_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
t_cat_sub_brick_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class t_cat_sub_brick(ShellCommandTask):
    """
    Examples
    -------

    >>> from pydra.tasks.afni.auto.utils.t_cat_sub_brick import t_cat_sub_brick

    >>> task = t_cat_sub_brick()
    >>> task.inputs.in_files = [('functional.nii', "'{2..$}'"), ('functional2.nii', "'{2..$}'")]
    >>> task.inputs.out_file = "functional_tcat.nii"
    >>> task.inputs.rlt = "+"
    >>> task.cmdline
    '3dTcat -rlt+ -prefix functional_tcat.nii functional.nii"{2..$}" functional2.nii"{2..$}" '


    """

    input_spec = t_cat_sub_brick_input_spec
    output_spec = t_cat_sub_brick_output_spec
    executable = "3dTcat"
