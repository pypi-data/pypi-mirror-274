from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        File,
        {
            "help_string": "input file to 3dAFNItoNIFTI",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_file",
        Nifti1,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}.nii",
        },
    ),
    (
        "pure",
        bool,
        {
            "help_string": "Do NOT write an AFNI extension field into the output file. Only use this option if needed. You can also use the 'nifti_tool' program to strip extensions from a file.",
            "argstr": "-pure",
        },
    ),
    (
        "denote",
        bool,
        {
            "help_string": "When writing the AFNI extension field, remove text notes that might contain subject identifying information.",
            "argstr": "-denote",
        },
    ),
    (
        "oldid",
        bool,
        {
            "help_string": "Give the new dataset the input datasets AFNI ID code.",
            "argstr": "-oldid",
            "xor": ["newid"],
        },
    ),
    (
        "newid",
        bool,
        {
            "help_string": "Give the new dataset a new AFNI ID code, to distinguish it from the input dataset.",
            "argstr": "-newid",
            "xor": ["oldid"],
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
a_f_n_ito_n_i_f_t_i_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
a_f_n_ito_n_i_f_t_i_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class a_f_n_ito_n_i_f_t_i(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.a_f_n_ito_n_i_f_t_i import a_f_n_ito_n_i_f_t_i

    >>> task = a_f_n_ito_n_i_f_t_i()
    >>> task.inputs.in_file = File.mock(None)
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.cmdline
    '3dAFNItoNIFTI -prefix afni_output.nii afni_output.3D'


    """

    input_spec = a_f_n_ito_n_i_f_t_i_input_spec
    output_spec = a_f_n_ito_n_i_f_t_i_output_spec
    executable = "3dAFNItoNIFTI"
