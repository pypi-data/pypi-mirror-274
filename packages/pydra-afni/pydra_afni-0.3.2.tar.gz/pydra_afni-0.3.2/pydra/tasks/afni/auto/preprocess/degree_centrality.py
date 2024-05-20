from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dDegreeCentrality",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "sparsity",
        float,
        {
            "help_string": "only take the top percent of connections",
            "argstr": "-sparsity {sparsity}",
        },
    ),
    (
        "oned_file",
        str,
        {
            "help_string": "output filepath to text dump of correlation matrix",
            "argstr": "-out1D {oned_file}",
        },
    ),
    (
        "mask",
        Nifti1,
        {"help_string": "mask file to mask input data", "argstr": "-mask {mask}"},
    ),
    (
        "thresh",
        float,
        {
            "help_string": "threshold to exclude connections where corr <= thresh",
            "argstr": "-thresh {thresh}",
        },
    ),
    ("polort", int, {"help_string": "", "argstr": "-polort {polort}"}),
    (
        "autoclip",
        bool,
        {
            "help_string": "Clip off low-intensity regions in the dataset",
            "argstr": "-autoclip",
        },
    ),
    (
        "automask",
        bool,
        {
            "help_string": "Mask the dataset to target brain-only voxels",
            "argstr": "-automask",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
    (
        "out_file",
        Nifti1,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_afni",
        },
    ),
]
degree_centrality_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "oned_file",
        File,
        {
            "help_string": "The text output of the similarity matrix computed after thresholding with one-dimensional and ijk voxel indices, correlations, image extents, and affine matrix."
        },
    )
]
degree_centrality_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class degree_centrality(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.degree_centrality import degree_centrality

    >>> task = degree_centrality()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.sparsity = 1 # keep the top one percent of connections
    >>> task.inputs.mask = Nifti1.mock(None)
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.cmdline
    '3dDegreeCentrality -mask mask.nii -prefix out.nii -sparsity 1.000000 functional.nii'


    """

    input_spec = degree_centrality_input_spec
    output_spec = degree_centrality_output_spec
    executable = "3dDegreeCentrality"


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dDegreeCentrality",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "sparsity",
        float,
        {
            "help_string": "only take the top percent of connections",
            "argstr": "-sparsity {sparsity}",
        },
    ),
    (
        "oned_file",
        str,
        {
            "help_string": "output filepath to text dump of correlation matrix",
            "argstr": "-out1D {oned_file}",
        },
    ),
    (
        "mask",
        Nifti1,
        {"help_string": "mask file to mask input data", "argstr": "-mask {mask}"},
    ),
    (
        "thresh",
        float,
        {
            "help_string": "threshold to exclude connections where corr <= thresh",
            "argstr": "-thresh {thresh}",
        },
    ),
    ("polort", int, {"help_string": "", "argstr": "-polort {polort}"}),
    (
        "autoclip",
        bool,
        {
            "help_string": "Clip off low-intensity regions in the dataset",
            "argstr": "-autoclip",
        },
    ),
    (
        "automask",
        bool,
        {
            "help_string": "Mask the dataset to target brain-only voxels",
            "argstr": "-automask",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
    (
        "out_file",
        Nifti1,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_afni",
        },
    ),
]
DegreeCentrality_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "oned_file",
        File,
        {
            "help_string": "The text output of the similarity matrix computed after thresholding with one-dimensional and ijk voxel indices, correlations, image extents, and affine matrix."
        },
    )
]
DegreeCentrality_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class DegreeCentrality(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.degree_centrality import DegreeCentrality

    >>> task = DegreeCentrality()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.sparsity = 1 # keep the top one percent of connections
    >>> task.inputs.mask = Nifti1.mock(None)
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.cmdline
    '3dDegreeCentrality -mask mask.nii -prefix out.nii -sparsity 1.000000 functional.nii'


    """

    input_spec = DegreeCentrality_input_spec
    output_spec = DegreeCentrality_output_spec
    executable = "3dDegreeCentrality"
