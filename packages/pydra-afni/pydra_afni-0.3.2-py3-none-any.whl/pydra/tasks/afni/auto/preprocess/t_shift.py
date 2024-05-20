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
            "help_string": "input file to 3dTshift",
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
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_tshift",
        },
    ),
    (
        "tr",
        str,
        {
            "help_string": 'manually set the TR. You can attach suffix "s" for seconds or "ms" for milliseconds.',
            "argstr": "-TR {tr}",
        },
    ),
    (
        "tzero",
        float,
        {
            "help_string": "align each slice to given time offset",
            "argstr": "-tzero {tzero}",
            "xor": ["tslice"],
        },
    ),
    (
        "tslice",
        int,
        {
            "help_string": "align each slice to time offset of given slice",
            "argstr": "-slice {tslice}",
            "xor": ["tzero"],
        },
    ),
    (
        "ignore",
        int,
        {
            "help_string": "ignore the first set of points specified",
            "argstr": "-ignore {ignore}",
        },
    ),
    (
        "interp",
        ty.Any,
        {
            "help_string": "different interpolation methods (see 3dTshift for details) default = Fourier",
            "argstr": "-{interp}",
        },
    ),
    (
        "tpattern",
        ty.Any,
        {
            "help_string": "use specified slice time pattern rather than one in header",
            "argstr": "-tpattern {tpattern}",
            "xor": ["slice_timing"],
        },
    ),
    (
        "slice_timing",
        ty.Any,
        {
            "help_string": "time offsets from the volume acquisition onset for each slice",
            "argstr": "-tpattern @{slice_timing}",
            "xor": ["tpattern"],
        },
    ),
    (
        "slice_encoding_direction",
        ty.Any,
        "k",
        {
            "help_string": "Direction in which slice_timing is specified (default: k). If negative,slice_timing is defined in reverse order, that is, the first entry corresponds to the slice with the largest index, and the final entry corresponds to slice index zero. Only in effect when slice_timing is passed as list, not when it is passed as file."
        },
    ),
    (
        "rlt",
        bool,
        {
            "help_string": "Before shifting, remove the mean and linear trend",
            "argstr": "-rlt",
        },
    ),
    (
        "rltplus",
        bool,
        {
            "help_string": "Before shifting, remove the mean and linear trend and later put back the mean",
            "argstr": "-rlt+",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
TShift_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "timing_file",
        File,
        {"help_string": "AFNI formatted timing file, if ``slice_timing`` is a list"},
    )
]
TShift_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class TShift(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.t_shift import TShift

    >>> task = TShift()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.tr = "%.1fs" % TR
    >>> task.inputs.tzero = 0.0
    >>> task.inputs.slice_timing = list(np.arange(40) / TR)
    >>> task.cmdline
    '3dTshift -prefix functional_tshift -tpattern @slice_timing.1D -TR 2.5s -tzero 0.0 functional.nii'


    >>> task = TShift()
    >>> task.inputs.in_file = Nifti1.mock()
    >>> task.inputs.slice_encoding_direction = "k-"
    >>> task.cmdline
    '3dTshift -prefix functional_tshift -tpattern @slice_timing.1D -TR 2.5s -tzero 0.0 functional.nii" >>> np.loadtxt(tshift._list_outputs()["timing_file'


    >>> task = TShift()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.tr = "%.1fs" % TR
    >>> task.inputs.tzero = 0.0
    >>> task.inputs.slice_timing = "slice_timing.1D"
    >>> task.cmdline
    '3dTshift -prefix functional_tshift -tpattern @slice_timing.1D -TR 2.5s -tzero 0.0 functional.nii'


    >>> task = TShift()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.tr = "%.1fs" % TR
    >>> task.inputs.tzero = 0.0
    >>> task.inputs.tpattern = "alt+z"
    >>> task.cmdline
    '3dTshift -prefix functional_tshift -tpattern alt+z -TR 2.5s -tzero 0.0 functional.nii'


    >>> task = TShift()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.tr = "%.1fs" % TR
    >>> task.inputs.tzero = 0.0
    >>> task.inputs.tpattern = "@slice_timing.1D"
    >>> task.cmdline
    '3dTshift -prefix functional_tshift -tpattern @slice_timing.1D -TR 2.5s -tzero 0.0 functional.nii'


    """

    input_spec = TShift_input_spec
    output_spec = TShift_output_spec
    executable = "3dTshift"


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dTshift",
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
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_tshift",
        },
    ),
    (
        "tr",
        str,
        {
            "help_string": 'manually set the TR. You can attach suffix "s" for seconds or "ms" for milliseconds.',
            "argstr": "-TR {tr}",
        },
    ),
    (
        "tzero",
        float,
        {
            "help_string": "align each slice to given time offset",
            "argstr": "-tzero {tzero}",
            "xor": ["tslice"],
        },
    ),
    (
        "tslice",
        int,
        {
            "help_string": "align each slice to time offset of given slice",
            "argstr": "-slice {tslice}",
            "xor": ["tzero"],
        },
    ),
    (
        "ignore",
        int,
        {
            "help_string": "ignore the first set of points specified",
            "argstr": "-ignore {ignore}",
        },
    ),
    (
        "interp",
        ty.Any,
        {
            "help_string": "different interpolation methods (see 3dTshift for details) default = Fourier",
            "argstr": "-{interp}",
        },
    ),
    (
        "tpattern",
        ty.Any,
        {
            "help_string": "use specified slice time pattern rather than one in header",
            "argstr": "-tpattern {tpattern}",
            "xor": ["slice_timing"],
        },
    ),
    (
        "slice_timing",
        ty.Any,
        {
            "help_string": "time offsets from the volume acquisition onset for each slice",
            "argstr": "-tpattern @{slice_timing}",
            "xor": ["tpattern"],
        },
    ),
    (
        "slice_encoding_direction",
        ty.Any,
        "k",
        {
            "help_string": "Direction in which slice_timing is specified (default: k). If negative,slice_timing is defined in reverse order, that is, the first entry corresponds to the slice with the largest index, and the final entry corresponds to slice index zero. Only in effect when slice_timing is passed as list, not when it is passed as file."
        },
    ),
    (
        "rlt",
        bool,
        {
            "help_string": "Before shifting, remove the mean and linear trend",
            "argstr": "-rlt",
        },
    ),
    (
        "rltplus",
        bool,
        {
            "help_string": "Before shifting, remove the mean and linear trend and later put back the mean",
            "argstr": "-rlt+",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
t_shift_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "timing_file",
        File,
        {"help_string": "AFNI formatted timing file, if ``slice_timing`` is a list"},
    )
]
t_shift_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class t_shift(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.t_shift import t_shift

    >>> task = t_shift()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.tr = "%.1fs" % TR
    >>> task.inputs.tzero = 0.0
    >>> task.inputs.slice_timing = list(np.arange(40) / TR)
    >>> task.cmdline
    '3dTshift -prefix functional_tshift -tpattern @slice_timing.1D -TR 2.5s -tzero 0.0 functional.nii'


    >>> task = t_shift()
    >>> task.inputs.in_file = Nifti1.mock()
    >>> task.inputs.slice_encoding_direction = "k-"
    >>> task.cmdline
    '3dTshift -prefix functional_tshift -tpattern @slice_timing.1D -TR 2.5s -tzero 0.0 functional.nii" >>> np.loadtxt(tshift._list_outputs()["timing_file'


    >>> task = t_shift()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.tr = "%.1fs" % TR
    >>> task.inputs.tzero = 0.0
    >>> task.inputs.slice_timing = "slice_timing.1D"
    >>> task.cmdline
    '3dTshift -prefix functional_tshift -tpattern @slice_timing.1D -TR 2.5s -tzero 0.0 functional.nii'


    >>> task = t_shift()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.tr = "%.1fs" % TR
    >>> task.inputs.tzero = 0.0
    >>> task.inputs.tpattern = "alt+z"
    >>> task.cmdline
    '3dTshift -prefix functional_tshift -tpattern alt+z -TR 2.5s -tzero 0.0 functional.nii'


    >>> task = t_shift()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.tr = "%.1fs" % TR
    >>> task.inputs.tzero = 0.0
    >>> task.inputs.tpattern = "@slice_timing.1D"
    >>> task.cmdline
    '3dTshift -prefix functional_tshift -tpattern @slice_timing.1D -TR 2.5s -tzero 0.0 functional.nii'


    """

    input_spec = t_shift_input_spec
    output_spec = t_shift_output_spec
    executable = "3dTshift"
