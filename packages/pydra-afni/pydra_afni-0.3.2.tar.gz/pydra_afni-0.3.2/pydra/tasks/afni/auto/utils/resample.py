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
            "help_string": "input file to 3dresample",
            "argstr": "-inset {in_file}",
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
            "output_file_template": "{in_file}_resample",
        },
    ),
    (
        "orientation",
        str,
        {"help_string": "new orientation code", "argstr": "-orient {orientation}"},
    ),
    (
        "resample_mode",
        ty.Any,
        {
            "help_string": 'resampling method from set {"NN", "Li", "Cu", "Bk"}. These are for "Nearest Neighbor", "Linear", "Cubic" and "Blocky"interpolation, respectively. Default is NN.',
            "argstr": "-rmode {resample_mode}",
        },
    ),
    (
        "voxel_size",
        ty.Any,
        {
            "help_string": "resample to new dx, dy and dz",
            "argstr": "-dxyz {voxel_size[0]} {voxel_size[1]} {voxel_size[2]}",
        },
    ),
    (
        "master",
        File,
        {
            "help_string": "align dataset grid to a reference file",
            "argstr": "-master {master}",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Resample_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Resample_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Resample(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.resample import Resample

    >>> task = Resample()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.orientation = "RPI"
    >>> task.inputs.master = File.mock()
    >>> task.inputs.outputtype = "NIFTI"
    >>> task.cmdline
    '3dresample -orient RPI -prefix functional_resample.nii -inset functional.nii'


    """

    input_spec = Resample_input_spec
    output_spec = Resample_output_spec
    executable = "3dresample"
