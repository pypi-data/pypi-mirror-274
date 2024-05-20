from fileformats.generic import File
from fileformats.medimage import Gifti
from fileformats.medimage_afni import Dset
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Gifti,
        {
            "help_string": "input file to ConvertDset",
            "argstr": "-input {in_file}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        Dset,
        {
            "help_string": "output file for ConvertDset",
            "argstr": "-prefix {out_file}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_type",
        ty.Any,
        {
            "help_string": "output type",
            "argstr": "-o_{out_type}",
            "mandatory": True,
            "position": 0,
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
ConvertDset_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", Dset, {"help_string": "output file"})]
ConvertDset_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ConvertDset(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Gifti
    >>> from fileformats.medimage_afni import Dset
    >>> from pydra.tasks.afni.auto.utils.convert_dset import ConvertDset

    >>> task = ConvertDset()
    >>> task.inputs.in_file = Gifti.mock(None)
    >>> task.inputs.out_file = Dset.mock(None)
    >>> task.inputs.out_type = "niml_asc"
    >>> task.cmdline
    'ConvertDset -o_niml_asc -input lh.pial_converted.gii -prefix lh.pial_converted.niml.dset'


    """

    input_spec = ConvertDset_input_spec
    output_spec = ConvertDset_output_spec
    executable = "ConvertDset"


input_fields = [
    (
        "in_file",
        File,
        {
            "help_string": "input file to ConvertDset",
            "argstr": "-input {in_file}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        File,
        {
            "help_string": "output file for ConvertDset",
            "argstr": "-prefix {out_file}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_type",
        ty.Any,
        {
            "help_string": "output type",
            "argstr": "-o_{out_type}",
            "mandatory": True,
            "position": 0,
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
convert_dset_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", File, {"help_string": "output file"})]
convert_dset_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class convert_dset(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.afni.auto.utils.convert_dset import convert_dset

    >>> task = convert_dset()
    >>> task.inputs.in_file = File.mock(None)
    >>> task.inputs.out_file = File.mock(None)
    >>> task.inputs.out_type = "niml_asc"
    >>> task.cmdline
    'ConvertDset -o_niml_asc -input lh.pial_converted.gii -prefix lh.pial_converted.niml.dset'


    """

    input_spec = convert_dset_input_spec
    output_spec = convert_dset_output_spec
    executable = "ConvertDset"
