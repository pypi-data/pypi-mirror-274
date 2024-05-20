from fileformats.generic import File
from fileformats.medimage_afni import Head
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Head,
        {
            "help_string": "input file to 3dNotes",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    ("add", str, {"help_string": "note to add", "argstr": '-a "{add}"'}),
    (
        "add_history",
        str,
        {
            "help_string": "note to add to history",
            "argstr": '-h "{add_history}"',
            "xor": ["rep_history"],
        },
    ),
    (
        "rep_history",
        str,
        {
            "help_string": "note with which to replace history",
            "argstr": '-HH "{rep_history}"',
            "xor": ["add_history"],
        },
    ),
    ("delete", int, {"help_string": "delete note number num", "argstr": "-d {delete}"}),
    (
        "ses",
        bool,
        {"help_string": "print to stdout the expanded notes", "argstr": "-ses"},
    ),
    (
        "out_file",
        File,
        {"help_string": "output image file name", "argstr": "{out_file}"},
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Notes_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", File, {"help_string": "output file"})]
Notes_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Notes(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage_afni import Head
    >>> from pydra.tasks.afni.auto.utils.notes import Notes

    >>> task = Notes()
    >>> task.inputs.in_file = Head.mock(None)
    >>> task.inputs.add = "This note is added."
    >>> task.inputs.add_history = "This note is added to history."
    >>> task.inputs.out_file = File.mock()
    >>> task.cmdline
    '3dNotes -a "This note is added." -h "This note is added to history." functional.HEAD'


    """

    input_spec = Notes_input_spec
    output_spec = Notes_output_spec
    executable = "3dNotes"
