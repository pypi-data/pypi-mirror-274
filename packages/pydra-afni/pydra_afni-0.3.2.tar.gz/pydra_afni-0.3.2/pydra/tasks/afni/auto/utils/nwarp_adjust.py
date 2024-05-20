from fileformats.generic import File
from fileformats.medimage import NiftiGz
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "warps",
        ty.List[NiftiGz],
        {
            "help_string": "List of input 3D warp datasets",
            "argstr": "-nwarp {warps}",
            "mandatory": True,
        },
    ),
    (
        "in_files",
        ty.List[File],
        {
            "help_string": "List of input 3D datasets to be warped by the adjusted warp datasets.  There must be exactly as many of these datasets as there are input warps.",
            "argstr": "-source {in_files}",
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Output mean dataset, only needed if in_files are also given. The output dataset will be on the common grid shared by the source datasets.",
            "argstr": "-prefix {out_file}",
            "requires": ["in_files"],
            "output_file_template": "{in_files}_NwarpAdjust",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
nwarp_adjust_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
nwarp_adjust_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class nwarp_adjust(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import NiftiGz
    >>> from pydra.tasks.afni.auto.utils.nwarp_adjust import nwarp_adjust

    >>> task = nwarp_adjust()
    >>> task.inputs.warps = None
    >>> task.cmdline
    '3dNwarpAdjust -nwarp func2anat_InverseWarp.nii.gz func2anat_InverseWarp.nii.gz func2anat_InverseWarp.nii.gz func2anat_InverseWarp.nii.gz func2anat_InverseWarp.nii.gz'


    """

    input_spec = nwarp_adjust_input_spec
    output_spec = nwarp_adjust_output_spec
    executable = "3dNwarpAdjust"


input_fields = [
    (
        "warps",
        ty.List[NiftiGz],
        {
            "help_string": "List of input 3D warp datasets",
            "argstr": "-nwarp {warps}",
            "mandatory": True,
        },
    ),
    (
        "in_files",
        ty.List[File],
        {
            "help_string": "List of input 3D datasets to be warped by the adjusted warp datasets.  There must be exactly as many of these datasets as there are input warps.",
            "argstr": "-source {in_files}",
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Output mean dataset, only needed if in_files are also given. The output dataset will be on the common grid shared by the source datasets.",
            "argstr": "-prefix {out_file}",
            "requires": ["in_files"],
            "output_file_template": "{in_files}_NwarpAdjust",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
NwarpAdjust_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
NwarpAdjust_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class NwarpAdjust(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import NiftiGz
    >>> from pydra.tasks.afni.auto.utils.nwarp_adjust import NwarpAdjust

    >>> task = NwarpAdjust()
    >>> task.inputs.warps = None
    >>> task.cmdline
    '3dNwarpAdjust -nwarp func2anat_InverseWarp.nii.gz func2anat_InverseWarp.nii.gz func2anat_InverseWarp.nii.gz func2anat_InverseWarp.nii.gz func2anat_InverseWarp.nii.gz'


    """

    input_spec = NwarpAdjust_input_spec
    output_spec = NwarpAdjust_output_spec
    executable = "3dNwarpAdjust"
