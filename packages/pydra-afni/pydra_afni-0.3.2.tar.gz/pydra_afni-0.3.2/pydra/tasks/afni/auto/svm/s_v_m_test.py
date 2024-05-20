from fileformats.generic import File
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "model",
        str,
        {
            "help_string": "modname is the basename for the brik containing the SVM model",
            "argstr": "-model {model}",
            "mandatory": True,
        },
    ),
    (
        "in_file",
        File,
        {
            "help_string": "A 3D or 3D+t AFNI brik dataset to be used for testing.",
            "argstr": "-testvol {in_file}",
            "mandatory": True,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "filename for .1D prediction file(s).",
            "argstr": "-predictions {out_file}",
            "output_file_template": "%s_predictions",
        },
    ),
    (
        "testlabels",
        File,
        {
            "help_string": "*true* class category .1D labels for the test dataset. It is used to calculate the prediction accuracy performance",
            "argstr": "-testlabels {testlabels}",
        },
    ),
    (
        "classout",
        bool,
        {
            "help_string": "Flag to specify that pname files should be integer-valued, corresponding to class category decisions.",
            "argstr": "-classout",
        },
    ),
    (
        "nopredcensord",
        bool,
        {
            "help_string": "Flag to prevent writing predicted values for censored time-points",
            "argstr": "-nopredcensord",
        },
    ),
    (
        "nodetrend",
        bool,
        {
            "help_string": "Flag to specify that pname files should not be linearly detrended",
            "argstr": "-nodetrend",
        },
    ),
    (
        "multiclass",
        bool,
        {
            "help_string": "Specifies multiclass algorithm for classification",
            "argstr": "-multiclass {multiclass}",
        },
    ),
    (
        "options",
        str,
        {"help_string": "additional options for SVM-light", "argstr": "{options}"},
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
s_v_m_test_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
s_v_m_test_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class s_v_m_test(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.afni.auto.svm.s_v_m_test import s_v_m_test

    """

    input_spec = s_v_m_test_input_spec
    output_spec = s_v_m_test_output_spec
    executable = "3dsvm"
