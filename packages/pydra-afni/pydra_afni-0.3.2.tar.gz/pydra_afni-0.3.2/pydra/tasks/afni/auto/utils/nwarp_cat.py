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
            "help_string": "list of tuples of 3D warps and associated functions",
            "argstr": "{in_files}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "space",
        ty.Any,
        {
            "help_string": "string to attach to the output dataset as its atlas space marker.",
            "argstr": "-space {space}",
        },
    ),
    (
        "inv_warp",
        bool,
        {"help_string": "invert the final warp before output", "argstr": "-iwarp"},
    ),
    (
        "interp",
        ty.Any,
        "wsinc5",
        {
            "help_string": "specify a different interpolation method than might be used for the warp",
            "argstr": "-interp {interp}",
        },
    ),
    (
        "expad",
        int,
        {
            "help_string": "Pad the nonlinear warps by the given number of voxels in all directions. The warp displacements are extended by linear extrapolation from the faces of the input grid..",
            "argstr": "-expad {expad}",
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_files}_NwarpCat",
        },
    ),
    ("verb", bool, {"help_string": "be verbose", "argstr": "-verb"}),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
nwarp_cat_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
nwarp_cat_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class nwarp_cat(ShellCommandTask):
    """
    Examples
    -------

    >>> from pydra.tasks.afni.auto.utils.nwarp_cat import nwarp_cat

    >>> task = nwarp_cat()
    >>> task.inputs.in_files = ["Q25_warp+tlrc.HEAD", ("IDENT", "structural.nii")]
    >>> task.inputs.out_file = None
    >>> task.cmdline
    '3dNwarpCat -interp wsinc5 -prefix Fred_total_WARP Q25_warp+tlrc.HEAD "IDENT(structural.nii)"'


    """

    input_spec = nwarp_cat_input_spec
    output_spec = nwarp_cat_output_spec
    executable = "3dNwarpCat"


input_fields = [
    (
        "in_files",
        list,
        {
            "help_string": "list of tuples of 3D warps and associated functions",
            "argstr": "{in_files}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "space",
        ty.Any,
        {
            "help_string": "string to attach to the output dataset as its atlas space marker.",
            "argstr": "-space {space}",
        },
    ),
    (
        "inv_warp",
        bool,
        {"help_string": "invert the final warp before output", "argstr": "-iwarp"},
    ),
    (
        "interp",
        ty.Any,
        "wsinc5",
        {
            "help_string": "specify a different interpolation method than might be used for the warp",
            "argstr": "-interp {interp}",
        },
    ),
    (
        "expad",
        int,
        {
            "help_string": "Pad the nonlinear warps by the given number of voxels in all directions. The warp displacements are extended by linear extrapolation from the faces of the input grid..",
            "argstr": "-expad {expad}",
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_files}_NwarpCat",
        },
    ),
    ("verb", bool, {"help_string": "be verbose", "argstr": "-verb"}),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
NwarpCat_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
NwarpCat_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class NwarpCat(ShellCommandTask):
    """
    Examples
    -------

    >>> from pydra.tasks.afni.auto.utils.nwarp_cat import NwarpCat

    >>> task = NwarpCat()
    >>> task.inputs.in_files = ["Q25_warp+tlrc.HEAD", ("IDENT", "structural.nii")]
    >>> task.inputs.out_file = None
    >>> task.cmdline
    '3dNwarpCat -interp wsinc5 -prefix Fred_total_WARP Q25_warp+tlrc.HEAD "IDENT(structural.nii)"'


    """

    input_spec = NwarpCat_input_spec
    output_spec = NwarpCat_output_spec
    executable = "3dNwarpCat"
