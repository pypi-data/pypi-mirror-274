from fileformats.generic import File
from fileformats.medimage import Nifti1, NiftiGz
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dWarp",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_file",
        NiftiGz,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_warp",
        },
    ),
    (
        "tta2mni",
        bool,
        {
            "help_string": "transform dataset from Talairach to MNI152",
            "argstr": "-tta2mni",
        },
    ),
    (
        "mni2tta",
        bool,
        {
            "help_string": "transform dataset from MNI152 to Talaraich",
            "argstr": "-mni2tta",
        },
    ),
    (
        "matparent",
        File,
        {
            "help_string": "apply transformation from 3dWarpDrive",
            "argstr": "-matparent {matparent}",
        },
    ),
    (
        "oblique_parent",
        File,
        {
            "help_string": "Read in the oblique transformation matrix from an oblique dataset and make cardinal dataset oblique to match",
            "argstr": "-oblique_parent {oblique_parent}",
        },
    ),
    (
        "deoblique",
        bool,
        {
            "help_string": "transform dataset from oblique to cardinal",
            "argstr": "-deoblique",
        },
    ),
    (
        "interp",
        ty.Any,
        {
            "help_string": "spatial interpolation methods [default = linear]",
            "argstr": "-{interp}",
        },
    ),
    (
        "gridset",
        File,
        {
            "help_string": "copy grid of specified dataset",
            "argstr": "-gridset {gridset}",
        },
    ),
    (
        "newgrid",
        float,
        {
            "help_string": "specify grid of this size (mm)",
            "argstr": "-newgrid {newgrid}",
        },
    ),
    (
        "zpad",
        int,
        {
            "help_string": "pad input dataset with N planes of zero on all sides.",
            "argstr": "-zpad {zpad}",
        },
    ),
    (
        "verbose",
        bool,
        {"help_string": "Print out some information along the way.", "argstr": "-verb"},
    ),
    (
        "save_warp",
        bool,
        {"help_string": "save warp as .mat file", "requires": ["verbose"]},
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Warp_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("warp_file", File, {"help_string": "warp transform .mat file"})]
Warp_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Warp(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1, NiftiGz
    >>> from pydra.tasks.afni.auto.preprocess.warp import Warp

    >>> task = Warp()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = NiftiGz.mock(None)
    >>> task.inputs.matparent = File.mock()
    >>> task.inputs.oblique_parent = File.mock()
    >>> task.inputs.deoblique = True
    >>> task.inputs.gridset = File.mock()
    >>> task.cmdline
    '3dWarp -deoblique -prefix trans.nii.gz structural.nii'


    >>> task = Warp()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = NiftiGz.mock(None)
    >>> task.inputs.matparent = File.mock()
    >>> task.inputs.oblique_parent = File.mock()
    >>> task.inputs.gridset = File.mock()
    >>> task.inputs.newgrid = 1.0
    >>> task.cmdline
    '3dWarp -newgrid 1.000000 -prefix trans.nii.gz structural.nii'


    """

    input_spec = Warp_input_spec
    output_spec = Warp_output_spec
    executable = "3dWarp"
