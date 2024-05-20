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
            "help_string": "",
            "argstr": "-input {in_file}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "seeds",
        File,
        {"help_string": "", "argstr": "-seed {seeds}", "xor": "seeds_width"},
    ),
    ("mask", Nifti1, {"help_string": "", "argstr": "-mask {mask}"}),
    ("automask", bool, {"help_string": "", "argstr": "-automask"}),
    ("polort", int, {"help_string": "", "argstr": "-polort {polort}"}),
    (
        "bandpass",
        ty.Any,
        {"help_string": "", "argstr": "-bpass {bandpass[0]} {bandpass[1]}"},
    ),
    (
        "regress_out_timeseries",
        File,
        {"help_string": "", "argstr": "-ort {regress_out_timeseries}"},
    ),
    ("blur_fwhm", float, {"help_string": "", "argstr": "-Gblur {blur_fwhm}"}),
    (
        "seeds_width",
        float,
        {"help_string": "", "argstr": "-Mseed {seeds_width}", "xor": "seeds"},
    ),
    ("mean_file", File, {"help_string": "", "argstr": "-Mean {mean_file}"}),
    ("zmean", File, {"help_string": "", "argstr": "-Zmean {zmean}"}),
    ("qmean", File, {"help_string": "", "argstr": "-Qmean {qmean}"}),
    ("pmean", File, {"help_string": "", "argstr": "-Pmean {pmean}"}),
    ("thresholds", list, {"help_string": ""}),
    (
        "absolute_threshold",
        File,
        {
            "help_string": "",
            "argstr": "-Thresh {absolute_threshold[0]} {absolute_threshold[1]}",
            "xor": (
                "absolute_threshold",
                "var_absolute_threshold",
                "var_absolute_threshold_normalize",
            ),
        },
    ),
    (
        "var_absolute_threshold",
        File,
        {
            "help_string": "",
            "argstr": "-VarThresh {var_absolute_threshold[0]} {var_absolute_threshold[1]} {var_absolute_threshold[2]} {var_absolute_threshold[3]}",
            "xor": (
                "absolute_threshold",
                "var_absolute_threshold",
                "var_absolute_threshold_normalize",
            ),
        },
    ),
    (
        "var_absolute_threshold_normalize",
        File,
        {
            "help_string": "",
            "argstr": "-VarThreshN {var_absolute_threshold_normalize[0]} {var_absolute_threshold_normalize[1]} {var_absolute_threshold_normalize[2]} {var_absolute_threshold_normalize[3]}",
            "xor": (
                "absolute_threshold",
                "var_absolute_threshold",
                "var_absolute_threshold_normalize",
            ),
        },
    ),
    (
        "correlation_maps",
        File,
        {"help_string": "", "argstr": "-CorrMap {correlation_maps}"},
    ),
    (
        "correlation_maps_masked",
        File,
        {"help_string": "", "argstr": "-CorrMask {correlation_maps_masked}"},
    ),
    ("expr", str, {"help_string": ""}),
    (
        "average_expr",
        File,
        {
            "help_string": "",
            "argstr": "-Aexpr {average_expr[0]} {average_expr[1]}",
            "xor": ("average_expr", "average_expr_nonzero", "sum_expr"),
        },
    ),
    (
        "average_expr_nonzero",
        File,
        {
            "help_string": "",
            "argstr": "-Cexpr {average_expr_nonzero[0]} {average_expr_nonzero[1]}",
            "xor": ("average_expr", "average_expr_nonzero", "sum_expr"),
        },
    ),
    (
        "sum_expr",
        File,
        {
            "help_string": "",
            "argstr": "-Sexpr {sum_expr[0]} {sum_expr[1]}",
            "xor": ("average_expr", "average_expr_nonzero", "sum_expr"),
        },
    ),
    ("histogram_bin_numbers", int, {"help_string": ""}),
    (
        "histogram",
        File,
        {"help_string": "", "argstr": "-Hist {histogram[0]} {histogram[1]}"},
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
    (
        "out_file",
        Path,
        {"help_string": "output image file name", "argstr": "-prefix {out_file}"},
    ),
]
t_corr_map_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("mean_file", File, {}),
    ("zmean", File, {}),
    ("qmean", File, {}),
    ("pmean", File, {}),
    ("absolute_threshold", File, {}),
    ("var_absolute_threshold", File, {}),
    ("var_absolute_threshold_normalize", File, {}),
    ("correlation_maps", File, {}),
    ("correlation_maps_masked", File, {}),
    ("average_expr", File, {}),
    ("average_expr_nonzero", File, {}),
    ("sum_expr", File, {}),
    ("histogram", File, {}),
]
t_corr_map_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class t_corr_map(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.t_corr_map import t_corr_map

    >>> task = t_corr_map()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.seeds = File.mock()
    >>> task.inputs.mask = Nifti1.mock(None)
    >>> task.inputs.regress_out_timeseries = File.mock()
    >>> task.inputs.mean_file = File.mock()
    >>> task.inputs.zmean = File.mock()
    >>> task.inputs.qmean = File.mock()
    >>> task.inputs.pmean = File.mock()
    >>> task.inputs.absolute_threshold = File.mock()
    >>> task.inputs.var_absolute_threshold = File.mock()
    >>> task.inputs.var_absolute_threshold_normalize = File.mock()
    >>> task.inputs.correlation_maps = File.mock()
    >>> task.inputs.correlation_maps_masked = File.mock()
    >>> task.inputs.average_expr = File.mock()
    >>> task.inputs.average_expr_nonzero = File.mock()
    >>> task.inputs.sum_expr = File.mock()
    >>> task.inputs.histogram = File.mock()
    >>> task.cmdline
    '3dTcorrMap -input functional.nii -mask mask.nii -Mean functional_meancorr.nii'


    """

    input_spec = t_corr_map_input_spec
    output_spec = t_corr_map_output_spec
    executable = "3dTcorrMap"


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "",
            "argstr": "-input {in_file}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "seeds",
        File,
        {"help_string": "", "argstr": "-seed {seeds}", "xor": "seeds_width"},
    ),
    ("mask", Nifti1, {"help_string": "", "argstr": "-mask {mask}"}),
    ("automask", bool, {"help_string": "", "argstr": "-automask"}),
    ("polort", int, {"help_string": "", "argstr": "-polort {polort}"}),
    (
        "bandpass",
        ty.Any,
        {"help_string": "", "argstr": "-bpass {bandpass[0]} {bandpass[1]}"},
    ),
    (
        "regress_out_timeseries",
        File,
        {"help_string": "", "argstr": "-ort {regress_out_timeseries}"},
    ),
    ("blur_fwhm", float, {"help_string": "", "argstr": "-Gblur {blur_fwhm}"}),
    (
        "seeds_width",
        float,
        {"help_string": "", "argstr": "-Mseed {seeds_width}", "xor": "seeds"},
    ),
    ("mean_file", File, {"help_string": "", "argstr": "-Mean {mean_file}"}),
    ("zmean", File, {"help_string": "", "argstr": "-Zmean {zmean}"}),
    ("qmean", File, {"help_string": "", "argstr": "-Qmean {qmean}"}),
    ("pmean", File, {"help_string": "", "argstr": "-Pmean {pmean}"}),
    ("thresholds", list, {"help_string": ""}),
    (
        "absolute_threshold",
        File,
        {
            "help_string": "",
            "argstr": "-Thresh {absolute_threshold[0]} {absolute_threshold[1]}",
            "xor": (
                "absolute_threshold",
                "var_absolute_threshold",
                "var_absolute_threshold_normalize",
            ),
        },
    ),
    (
        "var_absolute_threshold",
        File,
        {
            "help_string": "",
            "argstr": "-VarThresh {var_absolute_threshold[0]} {var_absolute_threshold[1]} {var_absolute_threshold[2]} {var_absolute_threshold[3]}",
            "xor": (
                "absolute_threshold",
                "var_absolute_threshold",
                "var_absolute_threshold_normalize",
            ),
        },
    ),
    (
        "var_absolute_threshold_normalize",
        File,
        {
            "help_string": "",
            "argstr": "-VarThreshN {var_absolute_threshold_normalize[0]} {var_absolute_threshold_normalize[1]} {var_absolute_threshold_normalize[2]} {var_absolute_threshold_normalize[3]}",
            "xor": (
                "absolute_threshold",
                "var_absolute_threshold",
                "var_absolute_threshold_normalize",
            ),
        },
    ),
    (
        "correlation_maps",
        File,
        {"help_string": "", "argstr": "-CorrMap {correlation_maps}"},
    ),
    (
        "correlation_maps_masked",
        File,
        {"help_string": "", "argstr": "-CorrMask {correlation_maps_masked}"},
    ),
    ("expr", str, {"help_string": ""}),
    (
        "average_expr",
        File,
        {
            "help_string": "",
            "argstr": "-Aexpr {average_expr[0]} {average_expr[1]}",
            "xor": ("average_expr", "average_expr_nonzero", "sum_expr"),
        },
    ),
    (
        "average_expr_nonzero",
        File,
        {
            "help_string": "",
            "argstr": "-Cexpr {average_expr_nonzero[0]} {average_expr_nonzero[1]}",
            "xor": ("average_expr", "average_expr_nonzero", "sum_expr"),
        },
    ),
    (
        "sum_expr",
        File,
        {
            "help_string": "",
            "argstr": "-Sexpr {sum_expr[0]} {sum_expr[1]}",
            "xor": ("average_expr", "average_expr_nonzero", "sum_expr"),
        },
    ),
    ("histogram_bin_numbers", int, {"help_string": ""}),
    (
        "histogram",
        File,
        {"help_string": "", "argstr": "-Hist {histogram[0]} {histogram[1]}"},
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
    (
        "out_file",
        Path,
        {"help_string": "output image file name", "argstr": "-prefix {out_file}"},
    ),
]
TCorrMap_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("mean_file", File, {}),
    ("zmean", File, {}),
    ("qmean", File, {}),
    ("pmean", File, {}),
    ("absolute_threshold", File, {}),
    ("var_absolute_threshold", File, {}),
    ("var_absolute_threshold_normalize", File, {}),
    ("correlation_maps", File, {}),
    ("correlation_maps_masked", File, {}),
    ("average_expr", File, {}),
    ("average_expr_nonzero", File, {}),
    ("sum_expr", File, {}),
    ("histogram", File, {}),
]
TCorrMap_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class TCorrMap(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.t_corr_map import TCorrMap

    >>> task = TCorrMap()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.seeds = File.mock()
    >>> task.inputs.mask = Nifti1.mock(None)
    >>> task.inputs.regress_out_timeseries = File.mock()
    >>> task.inputs.mean_file = File.mock()
    >>> task.inputs.zmean = File.mock()
    >>> task.inputs.qmean = File.mock()
    >>> task.inputs.pmean = File.mock()
    >>> task.inputs.absolute_threshold = File.mock()
    >>> task.inputs.var_absolute_threshold = File.mock()
    >>> task.inputs.var_absolute_threshold_normalize = File.mock()
    >>> task.inputs.correlation_maps = File.mock()
    >>> task.inputs.correlation_maps_masked = File.mock()
    >>> task.inputs.average_expr = File.mock()
    >>> task.inputs.average_expr_nonzero = File.mock()
    >>> task.inputs.sum_expr = File.mock()
    >>> task.inputs.histogram = File.mock()
    >>> task.cmdline
    '3dTcorrMap -input functional.nii -mask mask.nii -Mean functional_meancorr.nii'


    """

    input_spec = TCorrMap_input_spec
    output_spec = TCorrMap_output_spec
    executable = "3dTcorrMap"
