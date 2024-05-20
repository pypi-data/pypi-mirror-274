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
            "help_string": "input dataset",
            "argstr": "-input {in_file}",
            "mandatory": True,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output file",
            "argstr": "> {out_file}",
            "position": -1,
            "output_file_template": "{in_file}_fwhmx.out",
        },
    ),
    (
        "out_subbricks",
        Path,
        {
            "help_string": "output file listing the subbricks FWHM",
            "argstr": "-out {out_subbricks}",
            "output_file_template": "{in_file}_subbricks.out",
        },
    ),
    (
        "mask",
        File,
        {
            "help_string": "use only voxels that are nonzero in mask",
            "argstr": "-mask {mask}",
        },
    ),
    (
        "automask",
        bool,
        False,
        {
            "help_string": "compute a mask from THIS dataset, a la 3dAutomask",
            "argstr": "-automask",
        },
    ),
    (
        "detrend",
        ty.Any,
        False,
        {
            "help_string": "instead of demed (0th order detrending), detrend to the specified order.  If order is not given, the program picks q=NT/30. -detrend disables -demed, and includes -unif.",
            "argstr": "-detrend",
            "xor": ["demed"],
        },
    ),
    (
        "demed",
        bool,
        {
            "help_string": "If the input dataset has more than one sub-brick (e.g., has a time axis), then subtract the median of each voxel's time series before processing FWHM. This will tend to remove intrinsic spatial structure and leave behind the noise.",
            "argstr": "-demed",
            "xor": ["detrend"],
        },
    ),
    (
        "unif",
        bool,
        {
            "help_string": "If the input dataset has more than one sub-brick, then normalize each voxel's time series to have the same MAD before processing FWHM.",
            "argstr": "-unif",
        },
    ),
    (
        "out_detrend",
        Path,
        {
            "help_string": "Save the detrended file into a dataset",
            "argstr": "-detprefix {out_detrend}",
            "output_file_template": "{in_file}_detrend",
        },
    ),
    (
        "geom",
        bool,
        {
            "help_string": "if in_file has more than one sub-brick, compute the final estimate as the geometric mean of the individual sub-brick FWHM estimates",
            "argstr": "-geom",
            "xor": ["arith"],
        },
    ),
    (
        "arith",
        bool,
        {
            "help_string": "if in_file has more than one sub-brick, compute the final estimate as the arithmetic mean of the individual sub-brick FWHM estimates",
            "argstr": "-arith",
            "xor": ["geom"],
        },
    ),
    (
        "combine",
        bool,
        {
            "help_string": "combine the final measurements along each axis",
            "argstr": "-combine",
        },
    ),
    (
        "compat",
        bool,
        {"help_string": "be compatible with the older 3dFWHM", "argstr": "-compat"},
    ),
    (
        "acf",
        ty.Any,
        False,
        {"help_string": "computes the spatial autocorrelation", "argstr": "-acf"},
    ),
]
f_w_h_mx_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("fwhm", ty.Any, {"help_string": "FWHM along each axis"}),
    ("acf_param", ty.Any, {"help_string": "fitted ACF model parameters"}),
    ("out_acf", File, {"help_string": "output acf file"}),
]
f_w_h_mx_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class f_w_h_mx(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.f_w_h_mx import f_w_h_mx

    >>> task = f_w_h_mx()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.mask = File.mock()
    >>> task.cmdline
    '3dFWHMx -input functional.nii -out functional_subbricks.out > functional_fwhmx.out'


    """

    input_spec = f_w_h_mx_input_spec
    output_spec = f_w_h_mx_output_spec
    executable = "3dFWHMx"
