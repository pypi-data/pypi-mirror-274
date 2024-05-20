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
            "help_string": "input file to 3dECM",
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
        "full",
        bool,
        {
            "help_string": "Full power method; enables thresholding; automatically selected if -thresh or -sparsity are set",
            "argstr": "-full",
        },
    ),
    (
        "fecm",
        bool,
        {
            "help_string": "Fast centrality method; substantial speed increase but cannot accommodate thresholding; automatically selected if -thresh or -sparsity are not set",
            "argstr": "-fecm",
        },
    ),
    (
        "shift",
        float,
        {
            "help_string": "shift correlation coefficients in similarity matrix to enforce non-negativity, s >= 0.0; default = 0.0 for -full, 1.0 for -fecm",
            "argstr": "-shift {shift}",
        },
    ),
    (
        "scale",
        float,
        {
            "help_string": "scale correlation coefficients in similarity matrix to after shifting, x >= 0.0; default = 1.0 for -full, 0.5 for -fecm",
            "argstr": "-scale {scale}",
        },
    ),
    (
        "eps",
        float,
        {
            "help_string": "sets the stopping criterion for the power iteration; :math:`l2\\|v_\\text{old} - v_\\text{new}\\| < eps\\|v_\\text{old}\\|`; default = 0.001",
            "argstr": "-eps {eps}",
        },
    ),
    (
        "max_iter",
        int,
        {
            "help_string": "sets the maximum number of iterations to use in the power iteration; default = 1000",
            "argstr": "-max_iter {max_iter}",
        },
    ),
    (
        "memory",
        float,
        {
            "help_string": "Limit memory consumption on system by setting the amount of GB to limit the algorithm to; default = 2GB",
            "argstr": "-memory {memory}",
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
ECM_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ECM_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ECM(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.ecm import ECM

    >>> task = ECM()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.sparsity = 0.1 # keep top 0.1% of connections
    >>> task.inputs.mask = Nifti1.mock(None)
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.cmdline
    '3dECM -mask mask.nii -prefix out.nii -sparsity 0.100000 functional.nii'


    """

    input_spec = ECM_input_spec
    output_spec = ECM_output_spec
    executable = "3dECM"
