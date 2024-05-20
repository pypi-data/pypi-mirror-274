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
            "help_string": "input file to 3dBandpass",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output file from 3dBandpass",
            "argstr": "-prefix {out_file}",
            "position": 1,
            "output_file_template": "{in_file}_bp",
        },
    ),
    (
        "lowpass",
        float,
        {
            "help_string": "lowpass",
            "argstr": "{lowpass}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "highpass",
        float,
        {
            "help_string": "highpass",
            "argstr": "{highpass}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "mask",
        File,
        {"help_string": "mask file", "argstr": "-mask {mask}", "position": 2},
    ),
    (
        "despike",
        bool,
        {
            "help_string": "Despike each time series before other processing. Hopefully, you don't actually need to do this, which is why it is optional.",
            "argstr": "-despike",
        },
    ),
    (
        "orthogonalize_file",
        ty.List[File],
        {
            "help_string": "Also orthogonalize input to columns in f.1D. Multiple '-ort' options are allowed.",
            "argstr": "-ort {orthogonalize_file}",
        },
    ),
    (
        "orthogonalize_dset",
        File,
        {
            "help_string": "Orthogonalize each voxel to the corresponding voxel time series in dataset 'fset', which must have the same spatial and temporal grid structure as the main input dataset. At present, only one '-dsort' option is allowed.",
            "argstr": "-dsort {orthogonalize_dset}",
        },
    ),
    (
        "no_detrend",
        bool,
        {
            "help_string": "Skip the quadratic detrending of the input that occurs before the FFT-based bandpassing. You would only want to do this if the dataset had been detrended already in some other program.",
            "argstr": "-nodetrend",
        },
    ),
    (
        "tr",
        float,
        {
            "help_string": "Set time step (TR) in sec [default=from dataset header].",
            "argstr": "-dt {tr}",
        },
    ),
    (
        "nfft",
        int,
        {
            "help_string": "Set the FFT length [must be a legal value].",
            "argstr": "-nfft {nfft}",
        },
    ),
    (
        "normalize",
        bool,
        {
            "help_string": "Make all output time series have L2 norm = 1 (i.e., sum of squares = 1).",
            "argstr": "-norm",
        },
    ),
    (
        "automask",
        bool,
        {"help_string": "Create a mask from the input dataset.", "argstr": "-automask"},
    ),
    (
        "blur",
        float,
        {
            "help_string": "Blur (inside the mask only) with a filter width (FWHM) of 'fff' millimeters.",
            "argstr": "-blur {blur}",
        },
    ),
    (
        "localPV",
        float,
        {
            "help_string": "Replace each vector by the local Principal Vector (AKA first singular vector) from a neighborhood of radius 'rrr' millimeters. Note that the PV time series is L2 normalized. This option is mostly for Bob Cox to have fun with.",
            "argstr": "-localPV {localPV}",
        },
    ),
    (
        "notrans",
        bool,
        {
            "help_string": "Don't check for initial positive transients in the data. The test is a little slow, so skipping it is OK, if you KNOW the data time series are transient-free.",
            "argstr": "-notrans",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Bandpass_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Bandpass_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Bandpass(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.bandpass import Bandpass

    >>> task = Bandpass()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.lowpass = 0.1
    >>> task.inputs.highpass = 0.005
    >>> task.inputs.mask = File.mock()
    >>> task.inputs.orthogonalize_dset = File.mock()
    >>> task.cmdline
    '3dBandpass -prefix functional_bp 0.005000 0.100000 functional.nii'


    """

    input_spec = Bandpass_input_spec
    output_spec = Bandpass_output_spec
    executable = "3dBandpass"
