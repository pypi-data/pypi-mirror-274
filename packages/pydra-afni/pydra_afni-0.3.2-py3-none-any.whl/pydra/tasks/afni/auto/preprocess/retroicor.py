from fileformats.generic import File
from fileformats.medimage import Nifti1
from fileformats.medimage_afni import OneD
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
            "help_string": "input file to 3dretroicor",
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
            "position": 1,
            "output_file_template": "{in_file}_retroicor",
        },
    ),
    (
        "card",
        OneD,
        {
            "help_string": "1D cardiac data file for cardiac correction",
            "argstr": "-card {card}",
            "position": -2,
        },
    ),
    (
        "resp",
        OneD,
        {
            "help_string": "1D respiratory waveform data for correction",
            "argstr": "-resp {resp}",
            "position": -3,
        },
    ),
    (
        "threshold",
        int,
        {
            "help_string": "Threshold for detection of R-wave peaks in input (Make sure it is above the background noise level, Try 3/4 or 4/5 times range plus minimum)",
            "argstr": "-threshold {threshold}",
            "position": -4,
        },
    ),
    (
        "order",
        int,
        {
            "help_string": "The order of the correction (2 is typical)",
            "argstr": "-order {order}",
            "position": -5,
        },
    ),
    (
        "cardphase",
        File,
        {
            "help_string": "Filename for 1D cardiac phase output",
            "argstr": "-cardphase {cardphase}",
            "position": -6,
        },
    ),
    (
        "respphase",
        File,
        {
            "help_string": "Filename for 1D resp phase output",
            "argstr": "-respphase {respphase}",
            "position": -7,
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Retroicor_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Retroicor_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Retroicor(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from fileformats.medimage_afni import OneD
    >>> from pydra.tasks.afni.auto.preprocess.retroicor import Retroicor

    >>> task = Retroicor()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.card = OneD.mock(None)
    >>> task.inputs.resp = OneD.mock(None)
    >>> task.inputs.cardphase = File.mock()
    >>> task.inputs.respphase = File.mock()
    >>> task.inputs.outputtype = "NIFTI"
    >>> task.cmdline
    '3dretroicor -prefix functional_retroicor.nii -resp resp.1D -card mask.1D functional.nii'


    """

    input_spec = Retroicor_input_spec
    output_spec = Retroicor_output_spec
    executable = "3dretroicor"
