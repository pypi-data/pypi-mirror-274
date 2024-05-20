from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dClipLevel",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "mfrac",
        float,
        {
            "help_string": "Use the number ff instead of 0.50 in the algorithm",
            "argstr": "-mfrac {mfrac}",
            "position": 2,
        },
    ),
    (
        "doall",
        bool,
        {
            "help_string": "Apply the algorithm to each sub-brick separately.",
            "argstr": "-doall",
            "position": 3,
            "xor": "grad",
        },
    ),
    (
        "grad",
        File,
        {
            "help_string": "Also compute a 'gradual' clip level as a function of voxel position, and output that to a dataset.",
            "argstr": "-grad {grad}",
            "position": 3,
            "xor": "doall",
        },
    ),
]
ClipLevel_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("clip_val", float, {"help_string": "output"})]
ClipLevel_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ClipLevel(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.clip_level import ClipLevel

    >>> task = ClipLevel()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.grad = File.mock()
    >>> task.cmdline
    '3dClipLevel anatomical.nii'


    """

    input_spec = ClipLevel_input_spec
    output_spec = ClipLevel_output_spec
    executable = "3dClipLevel"


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dClipLevel",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "mfrac",
        float,
        {
            "help_string": "Use the number ff instead of 0.50 in the algorithm",
            "argstr": "-mfrac {mfrac}",
            "position": 2,
        },
    ),
    (
        "doall",
        bool,
        {
            "help_string": "Apply the algorithm to each sub-brick separately.",
            "argstr": "-doall",
            "position": 3,
            "xor": "grad",
        },
    ),
    (
        "grad",
        File,
        {
            "help_string": "Also compute a 'gradual' clip level as a function of voxel position, and output that to a dataset.",
            "argstr": "-grad {grad}",
            "position": 3,
            "xor": "doall",
        },
    ),
]
clip_level_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("clip_val", float, {"help_string": "output"})]
clip_level_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class clip_level(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.clip_level import clip_level

    >>> task = clip_level()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.grad = File.mock()
    >>> task.cmdline
    '3dClipLevel anatomical.nii'


    """

    input_spec = clip_level_input_spec
    output_spec = clip_level_output_spec
    executable = "3dClipLevel"
