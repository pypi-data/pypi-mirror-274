from fileformats.generic import File
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "ttype",
        str,
        {
            "help_string": "tname: classification or regression",
            "argstr": "-type {ttype}",
            "mandatory": True,
        },
    ),
    (
        "in_file",
        File,
        {
            "help_string": "A 3D+t AFNI brik dataset to be used for training.",
            "argstr": "-trainvol {in_file}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output sum of weighted linear support vectors file name",
            "argstr": "-bucket {out_file}",
            "output_file_template": "{in_file}_vectors",
        },
    ),
    (
        "model",
        Path,
        {
            "help_string": "basename for the brik containing the SVM model",
            "argstr": "-model {model}",
            "output_file_template": "{in_file}_model",
        },
    ),
    (
        "alphas",
        Path,
        {
            "help_string": "output alphas file name",
            "argstr": "-alpha {alphas}",
            "output_file_template": "{in_file}_alphas",
        },
    ),
    (
        "mask",
        File,
        {
            "help_string": "byte-format brik file used to mask voxels in the analysis",
            "argstr": "-mask {mask}",
            "copyfile": False,
            "position": -1,
        },
    ),
    (
        "nomodelmask",
        bool,
        {
            "help_string": "Flag to enable the omission of a mask file",
            "argstr": "-nomodelmask",
        },
    ),
    (
        "trainlabels",
        File,
        {
            "help_string": ".1D labels corresponding to the stimulus paradigm for the training data.",
            "argstr": "-trainlabels {trainlabels}",
        },
    ),
    (
        "censor",
        File,
        {
            "help_string": ".1D censor file that allows the user to ignore certain samples in the training data.",
            "argstr": "-censor {censor}",
        },
    ),
    (
        "kernel",
        str,
        {
            "help_string": "string specifying type of kernel function:linear, polynomial, rbf, sigmoid",
            "argstr": "-kernel {kernel}",
        },
    ),
    (
        "max_iterations",
        int,
        {
            "help_string": "Specify the maximum number of iterations for the optimization.",
            "argstr": "-max_iterations {max_iterations}",
        },
    ),
    (
        "w_out",
        bool,
        {
            "help_string": "output sum of weighted linear support vectors",
            "argstr": "-wout",
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
s_v_m_train_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
s_v_m_train_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class s_v_m_train(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.afni.auto.svm.s_v_m_train import s_v_m_train

    """

    input_spec = s_v_m_train_input_spec
    output_spec = s_v_m_train_output_spec
    executable = "3dsvm"
