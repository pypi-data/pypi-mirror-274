from fileformats.generic import File
from fileformats.medimage_afni import OneD
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        File,
        {
            "help_string": "input file to OneDTool",
            "argstr": "-infile {in_file}",
            "mandatory": True,
        },
    ),
    (
        "set_nruns",
        int,
        {
            "help_string": "treat the input data as if it has nruns",
            "argstr": "-set_nruns {set_nruns}",
        },
    ),
    (
        "derivative",
        bool,
        {
            "help_string": "take the temporal derivative of each vector (done as first backward difference)",
            "argstr": "-derivative",
        },
    ),
    (
        "demean",
        bool,
        {
            "help_string": "demean each run (new mean of each run = 0.0)",
            "argstr": "-demean",
        },
    ),
    (
        "out_file",
        File,
        {
            "help_string": "write the current 1D data to FILE",
            "argstr": "-write {out_file}",
            "xor": ["show_cormat_warnings"],
        },
    ),
    (
        "show_censor_count",
        bool,
        {
            "help_string": "display the total number of censored TRs  Note : if input is a valid xmat.1D dataset, then the count will come from the header.  Otherwise the input is assumed to be a binary censorfile, and zeros are simply counted.",
            "argstr": "-show_censor_count",
        },
    ),
    (
        "censor_motion",
        ty.Any,
        {
            "help_string": "Tuple of motion limit and outfile prefix. need to also set set_nruns -r set_run_lengths",
            "argstr": "-censor_motion {censor_motion[0]} {censor_motion[1]}",
        },
    ),
    (
        "censor_prev_TR",
        bool,
        {
            "help_string": "for each censored TR, also censor previous",
            "argstr": "-censor_prev_TR",
        },
    ),
    (
        "show_trs_uncensored",
        ty.Any,
        {
            "help_string": "display a list of TRs which were not censored in the specified style",
            "argstr": "-show_trs_uncensored {show_trs_uncensored}",
        },
    ),
    (
        "show_cormat_warnings",
        File,
        {
            "help_string": "Write cormat warnings to a file",
            "argstr": "-show_cormat_warnings |& tee {show_cormat_warnings}",
            "position": -1,
            "xor": ["out_file"],
        },
    ),
    (
        "show_indices_interest",
        bool,
        {
            "help_string": "display column indices for regs of interest",
            "argstr": "-show_indices_interest",
        },
    ),
    (
        "show_trs_run",
        int,
        {
            "help_string": "restrict -show_trs_[un]censored to the given 1-based run",
            "argstr": "-show_trs_run {show_trs_run}",
        },
    ),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
    ("py27_path", ty.Any, "python2", {"help_string": ""}),
]
one_d_tool_py_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", File, {"help_string": "output of 1D_tool.py"})]
one_d_tool_py_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class one_d_tool_py(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.afni.auto.utils.one_d_tool_py import one_d_tool_py

    >>> task = one_d_tool_py()
    >>> task.inputs.in_file = File.mock(None)
    >>> task.inputs.set_nruns = 3
    >>> task.inputs.demean = True
    >>> task.inputs.out_file = File.mock(None)
    >>> task.inputs.show_cormat_warnings = File.mock()
    >>> task.cmdline
    'python2 ...1d_tool.py -demean -infile f1.1D -write motion_dmean.1D -set_nruns 3'


    """

    input_spec = one_d_tool_py_input_spec
    output_spec = one_d_tool_py_output_spec
    executable = "1d_tool.py"


input_fields = [
    (
        "in_file",
        OneD,
        {
            "help_string": "input file to OneDTool",
            "argstr": "-infile {in_file}",
            "mandatory": True,
        },
    ),
    (
        "set_nruns",
        int,
        {
            "help_string": "treat the input data as if it has nruns",
            "argstr": "-set_nruns {set_nruns}",
        },
    ),
    (
        "derivative",
        bool,
        {
            "help_string": "take the temporal derivative of each vector (done as first backward difference)",
            "argstr": "-derivative",
        },
    ),
    (
        "demean",
        bool,
        {
            "help_string": "demean each run (new mean of each run = 0.0)",
            "argstr": "-demean",
        },
    ),
    (
        "out_file",
        OneD,
        {
            "help_string": "write the current 1D data to FILE",
            "argstr": "-write {out_file}",
            "xor": ["show_cormat_warnings"],
        },
    ),
    (
        "show_censor_count",
        bool,
        {
            "help_string": "display the total number of censored TRs  Note : if input is a valid xmat.1D dataset, then the count will come from the header.  Otherwise the input is assumed to be a binary censorfile, and zeros are simply counted.",
            "argstr": "-show_censor_count",
        },
    ),
    (
        "censor_motion",
        ty.Any,
        {
            "help_string": "Tuple of motion limit and outfile prefix. need to also set set_nruns -r set_run_lengths",
            "argstr": "-censor_motion {censor_motion[0]} {censor_motion[1]}",
        },
    ),
    (
        "censor_prev_TR",
        bool,
        {
            "help_string": "for each censored TR, also censor previous",
            "argstr": "-censor_prev_TR",
        },
    ),
    (
        "show_trs_uncensored",
        ty.Any,
        {
            "help_string": "display a list of TRs which were not censored in the specified style",
            "argstr": "-show_trs_uncensored {show_trs_uncensored}",
        },
    ),
    (
        "show_cormat_warnings",
        File,
        {
            "help_string": "Write cormat warnings to a file",
            "argstr": "-show_cormat_warnings |& tee {show_cormat_warnings}",
            "position": -1,
            "xor": ["out_file"],
        },
    ),
    (
        "show_indices_interest",
        bool,
        {
            "help_string": "display column indices for regs of interest",
            "argstr": "-show_indices_interest",
        },
    ),
    (
        "show_trs_run",
        int,
        {
            "help_string": "restrict -show_trs_[un]censored to the given 1-based run",
            "argstr": "-show_trs_run {show_trs_run}",
        },
    ),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
    ("py27_path", ty.Any, "python2", {"help_string": ""}),
]
OneDToolPy_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", OneD, {"help_string": "output of 1D_tool.py"})]
OneDToolPy_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class OneDToolPy(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage_afni import OneD
    >>> from pydra.tasks.afni.auto.utils.one_d_tool_py import OneDToolPy

    >>> task = OneDToolPy()
    >>> task.inputs.in_file = OneD.mock(None)
    >>> task.inputs.set_nruns = 3
    >>> task.inputs.demean = True
    >>> task.inputs.out_file = OneD.mock(None)
    >>> task.inputs.show_cormat_warnings = File.mock()
    >>> task.cmdline
    'python2 ...1d_tool.py -demean -infile f1.1D -write motion_dmean.1D -set_nruns 3'


    """

    input_spec = OneDToolPy_input_spec
    output_spec = OneDToolPy_output_spec
    executable = "1d_tool.py"
