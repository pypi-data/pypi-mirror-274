from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


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
        {
            "help_string": "compute correlation only across masked voxels",
            "argstr": "-mask {mask}",
            "xor": ["autoclip", "automask"],
        },
    ),
    (
        "spearman",
        bool,
        False,
        {
            "help_string": "Quality index is 1 minus the Spearman (rank) correlation coefficient of each sub-brick with the median sub-brick. (default).",
            "argstr": "-spearman",
        },
    ),
    (
        "quadrant",
        bool,
        False,
        {
            "help_string": "Similar to -spearman, but using 1 minus the quadrant correlation coefficient as the quality index.",
            "argstr": "-quadrant",
        },
    ),
    (
        "autoclip",
        bool,
        False,
        {
            "help_string": "clip off small voxels",
            "argstr": "-autoclip",
            "xor": ["mask"],
        },
    ),
    (
        "automask",
        bool,
        False,
        {
            "help_string": "clip off small voxels",
            "argstr": "-automask",
            "xor": ["mask"],
        },
    ),
    ("clip", float, {"help_string": "clip off values below", "argstr": "-clip {clip}"}),
    (
        "interval",
        bool,
        False,
        {
            "help_string": "write out the median + 3.5 MAD of outlier count with each timepoint",
            "argstr": "-range",
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "capture standard output",
            "argstr": "> {out_file}",
            "position": -1,
            "output_file_template": "{in_file}_tqual",
        },
    ),
]
quality_index_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
quality_index_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class quality_index(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.quality_index import quality_index

    >>> task = quality_index()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.mask = File.mock()
    >>> task.cmdline
    '3dTqual functional.nii > functional_tqual'


    """

    input_spec = quality_index_input_spec
    output_spec = quality_index_output_spec
    executable = "3dTqual"


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
        {
            "help_string": "compute correlation only across masked voxels",
            "argstr": "-mask {mask}",
            "xor": ["autoclip", "automask"],
        },
    ),
    (
        "spearman",
        bool,
        False,
        {
            "help_string": "Quality index is 1 minus the Spearman (rank) correlation coefficient of each sub-brick with the median sub-brick. (default).",
            "argstr": "-spearman",
        },
    ),
    (
        "quadrant",
        bool,
        False,
        {
            "help_string": "Similar to -spearman, but using 1 minus the quadrant correlation coefficient as the quality index.",
            "argstr": "-quadrant",
        },
    ),
    (
        "autoclip",
        bool,
        False,
        {
            "help_string": "clip off small voxels",
            "argstr": "-autoclip",
            "xor": ["mask"],
        },
    ),
    (
        "automask",
        bool,
        False,
        {
            "help_string": "clip off small voxels",
            "argstr": "-automask",
            "xor": ["mask"],
        },
    ),
    ("clip", float, {"help_string": "clip off values below", "argstr": "-clip {clip}"}),
    (
        "interval",
        bool,
        False,
        {
            "help_string": "write out the median + 3.5 MAD of outlier count with each timepoint",
            "argstr": "-range",
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "capture standard output",
            "argstr": "> {out_file}",
            "position": -1,
            "output_file_template": "{in_file}_tqual",
        },
    ),
]
QualityIndex_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
QualityIndex_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class QualityIndex(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.quality_index import QualityIndex

    >>> task = QualityIndex()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.mask = File.mock()
    >>> task.cmdline
    '3dTqual functional.nii > functional_tqual'


    """

    input_spec = QualityIndex_input_spec
    output_spec = QualityIndex_output_spec
    executable = "3dTqual"
