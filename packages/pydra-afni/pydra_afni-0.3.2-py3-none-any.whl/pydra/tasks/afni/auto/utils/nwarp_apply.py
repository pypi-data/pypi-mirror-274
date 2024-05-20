from fileformats.generic import File
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        ty.Any,
        {
            "help_string": "the name of the dataset to be warped can be multiple datasets",
            "argstr": "-source {in_file}",
            "mandatory": True,
        },
    ),
    (
        "warp",
        ty.Any,
        {
            "help_string": "the name of the warp dataset. multiple warps can be concatenated (make sure they exist)",
            "argstr": "-nwarp {warp}",
            "mandatory": True,
        },
    ),
    (
        "inv_warp",
        bool,
        {
            "help_string": "After the warp specified in '-nwarp' is computed, invert it",
            "argstr": "-iwarp",
        },
    ),
    (
        "master",
        File,
        {
            "help_string": "the name of the master dataset, which defines the output grid",
            "argstr": "-master {master}",
        },
    ),
    (
        "interp",
        ty.Any,
        "wsinc5",
        {
            "help_string": "defines interpolation method to use during warp",
            "argstr": "-interp {interp}",
        },
    ),
    (
        "ainterp",
        ty.Any,
        {
            "help_string": "specify a different interpolation method than might be used for the warp",
            "argstr": "-ainterp {ainterp}",
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_Nwarp",
        },
    ),
    (
        "short",
        bool,
        {
            "help_string": "Write output dataset using 16-bit short integers, rather than the usual 32-bit floats.",
            "argstr": "-short",
        },
    ),
    (
        "quiet",
        bool,
        {"help_string": "don't be verbose :(", "argstr": "-quiet", "xor": ["verb"]},
    ),
    (
        "verb",
        bool,
        {"help_string": "be extra verbose :)", "argstr": "-verb", "xor": ["quiet"]},
    ),
]
nwarp_apply_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
nwarp_apply_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class nwarp_apply(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.afni.auto.utils.nwarp_apply import nwarp_apply

    >>> task = nwarp_apply()
    >>> task.inputs.in_file = "Fred+orig"
    >>> task.inputs.warp = "'Fred_WARP+tlrc Fred.Xaff12.1D'"
    >>> task.inputs.master = File.mock(None)
    >>> task.cmdline
    '3dNwarpApply -source Fred+orig -interp wsinc5 -master NWARP -prefix Fred+orig_Nwarp -nwarp "Fred_WARP+tlrc Fred.Xaff12.1D"'


    """

    input_spec = nwarp_apply_input_spec
    output_spec = nwarp_apply_output_spec
    executable = "3dNwarpApply"


input_fields = [
    (
        "in_file",
        ty.Any,
        {
            "help_string": "the name of the dataset to be warped can be multiple datasets",
            "argstr": "-source {in_file}",
            "mandatory": True,
        },
    ),
    (
        "warp",
        ty.Any,
        {
            "help_string": "the name of the warp dataset. multiple warps can be concatenated (make sure they exist)",
            "argstr": "-nwarp {warp}",
            "mandatory": True,
        },
    ),
    (
        "inv_warp",
        bool,
        {
            "help_string": "After the warp specified in '-nwarp' is computed, invert it",
            "argstr": "-iwarp",
        },
    ),
    (
        "master",
        File,
        {
            "help_string": "the name of the master dataset, which defines the output grid",
            "argstr": "-master {master}",
        },
    ),
    (
        "interp",
        ty.Any,
        "wsinc5",
        {
            "help_string": "defines interpolation method to use during warp",
            "argstr": "-interp {interp}",
        },
    ),
    (
        "ainterp",
        ty.Any,
        {
            "help_string": "specify a different interpolation method than might be used for the warp",
            "argstr": "-ainterp {ainterp}",
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_Nwarp",
        },
    ),
    (
        "short",
        bool,
        {
            "help_string": "Write output dataset using 16-bit short integers, rather than the usual 32-bit floats.",
            "argstr": "-short",
        },
    ),
    (
        "quiet",
        bool,
        {"help_string": "don't be verbose :(", "argstr": "-quiet", "xor": ["verb"]},
    ),
    (
        "verb",
        bool,
        {"help_string": "be extra verbose :)", "argstr": "-verb", "xor": ["quiet"]},
    ),
]
NwarpApply_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
NwarpApply_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class NwarpApply(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.afni.auto.utils.nwarp_apply import NwarpApply

    >>> task = NwarpApply()
    >>> task.inputs.in_file = "Fred+orig"
    >>> task.inputs.warp = "'Fred_WARP+tlrc Fred.Xaff12.1D'"
    >>> task.inputs.master = File.mock(None)
    >>> task.cmdline
    '3dNwarpApply -source Fred+orig -interp wsinc5 -master NWARP -prefix Fred+orig_Nwarp -nwarp "Fred_WARP+tlrc Fred.Xaff12.1D"'


    """

    input_spec = NwarpApply_input_spec
    output_spec = NwarpApply_output_spec
    executable = "3dNwarpApply"
