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
            "help_string": "timeseries x space (volume or surface) file",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "polort",
        int,
        {
            "help_string": "Remove polynomical trend of order m or -1 for no detrending",
            "argstr": "-polort {polort}",
        },
    ),
    ("eta2", bool, {"help_string": "eta^2 similarity", "argstr": "-eta2"}),
    ("mask", Nifti1, {"help_string": "mask of voxels", "argstr": "-mask {mask}"}),
    (
        "mask_only_targets",
        bool,
        {
            "help_string": "use mask only on targets voxels",
            "argstr": "-mask_only_targets",
            "xor": ["mask_source"],
        },
    ),
    (
        "mask_source",
        File,
        {
            "help_string": "mask for source voxels",
            "argstr": "-mask_source {mask_source}",
            "xor": ["mask_only_targets"],
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_similarity_matrix.1D",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
AutoTcorrelate_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
AutoTcorrelate_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class AutoTcorrelate(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.auto_tcorrelate import AutoTcorrelate

    >>> task = AutoTcorrelate()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.polort = -1
    >>> task.inputs.eta2 = True
    >>> task.inputs.mask = Nifti1.mock(None)
    >>> task.inputs.mask_only_targets = True
    >>> task.inputs.mask_source = File.mock()
    >>> task.cmdline
    '3dAutoTcorrelate -eta2 -mask mask.nii -mask_only_targets -prefix functional_similarity_matrix.1D -polort -1 functional.nii'


    """

    input_spec = AutoTcorrelate_input_spec
    output_spec = AutoTcorrelate_output_spec
    executable = "3dAutoTcorrelate"


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "timeseries x space (volume or surface) file",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "polort",
        int,
        {
            "help_string": "Remove polynomical trend of order m or -1 for no detrending",
            "argstr": "-polort {polort}",
        },
    ),
    ("eta2", bool, {"help_string": "eta^2 similarity", "argstr": "-eta2"}),
    ("mask", Nifti1, {"help_string": "mask of voxels", "argstr": "-mask {mask}"}),
    (
        "mask_only_targets",
        bool,
        {
            "help_string": "use mask only on targets voxels",
            "argstr": "-mask_only_targets",
            "xor": ["mask_source"],
        },
    ),
    (
        "mask_source",
        File,
        {
            "help_string": "mask for source voxels",
            "argstr": "-mask_source {mask_source}",
            "xor": ["mask_only_targets"],
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_similarity_matrix.1D",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
auto_tcorrelate_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
auto_tcorrelate_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class auto_tcorrelate(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.auto_tcorrelate import auto_tcorrelate

    >>> task = auto_tcorrelate()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.polort = -1
    >>> task.inputs.eta2 = True
    >>> task.inputs.mask = Nifti1.mock(None)
    >>> task.inputs.mask_only_targets = True
    >>> task.inputs.mask_source = File.mock()
    >>> task.cmdline
    '3dAutoTcorrelate -eta2 -mask mask.nii -mask_only_targets -prefix functional_similarity_matrix.1D -polort -1 functional.nii'


    """

    input_spec = auto_tcorrelate_input_spec
    output_spec = auto_tcorrelate_output_spec
    executable = "3dAutoTcorrelate"
