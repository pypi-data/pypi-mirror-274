from fileformats.medimage import Nifti1
from fileformats.medimage_afni import OneD
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dfim+",
            "argstr": "-input {in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "out_file",
        Nifti1,
        {
            "help_string": "output image file name",
            "argstr": "-bucket {out_file}",
            "output_file_template": "{in_file}_fim",
        },
    ),
    (
        "ideal_file",
        OneD,
        {
            "help_string": "ideal time series file name",
            "argstr": "-ideal_file {ideal_file}",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "fim_thr",
        float,
        {
            "help_string": "fim internal mask threshold value",
            "argstr": "-fim_thr {fim_thr}",
            "position": 3,
        },
    ),
    (
        "out",
        str,
        {
            "help_string": "Flag to output the specified parameter",
            "argstr": "-out {out}",
            "position": 4,
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Fim_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Fim_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Fim(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from fileformats.medimage_afni import OneD
    >>> from pydra.tasks.afni.auto.preprocess.fim import Fim

    >>> task = Fim()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.inputs.ideal_file = OneD.mock(None)
    >>> task.inputs.fim_thr = 0.0009
    >>> task.inputs.out = "Correlation"
    >>> task.cmdline
    '3dfim+ -input functional.nii -ideal_file seed.1D -fim_thr 0.000900 -out Correlation -bucket functional_corr.nii'


    """

    input_spec = Fim_input_spec
    output_spec = Fim_output_spec
    executable = "3dfim+"
