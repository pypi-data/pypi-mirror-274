from fileformats.medimage import Nifti1
from fileformats.medimage_afni import OneD, R1
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
            "help_string": "input file to 3dvolreg",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "in_weight_volume",
        ty.Any,
        {
            "help_string": "weights for each voxel specified by a file with an optional volume number (defaults to 0)",
            "argstr": "-weight '{in_weight_volume[0]}[{in_weight_volume[1]}]'",
        },
    ),
    (
        "out_file",
        R1,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_volreg",
        },
    ),
    (
        "basefile",
        Nifti1,
        {
            "help_string": "base file for registration",
            "argstr": "-base {basefile}",
            "position": -6,
        },
    ),
    (
        "zpad",
        int,
        {
            "help_string": "Zeropad around the edges by 'n' voxels during rotations",
            "argstr": "-zpad {zpad}",
            "position": -5,
        },
    ),
    (
        "md1d_file",
        Path,
        {
            "help_string": "max displacement output file",
            "argstr": "-maxdisp1D {md1d_file}",
            "position": -4,
            "output_file_template": "{in_file}_md.1D",
        },
    ),
    (
        "oned_file",
        OneD,
        {
            "help_string": "1D movement parameters output file",
            "argstr": "-1Dfile {oned_file}",
            "output_file_template": "{in_file}.1D",
        },
    ),
    (
        "verbose",
        bool,
        {
            "help_string": "more detailed description of the process",
            "argstr": "-verbose",
        },
    ),
    (
        "timeshift",
        bool,
        {"help_string": "time shift to mean slice time offset", "argstr": "-tshift 0"},
    ),
    (
        "copyorigin",
        bool,
        {"help_string": "copy base file origin coords to output", "argstr": "-twodup"},
    ),
    (
        "oned_matrix_save",
        OneD,
        {
            "help_string": "Save the matrix transformation",
            "argstr": "-1Dmatrix_save {oned_matrix_save}",
            "output_file_template": "{in_file}.aff12.1D",
        },
    ),
    (
        "interp",
        ty.Any,
        {
            "help_string": "spatial interpolation methods [default = heptic]",
            "argstr": "-{interp}",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Volreg_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Volreg_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Volreg(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from fileformats.medimage_afni import OneD, R1
    >>> from pydra.tasks.afni.auto.preprocess.volreg import Volreg

    >>> task = Volreg()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = R1.mock()
    >>> task.inputs.basefile = Nifti1.mock()
    >>> task.inputs.zpad = 4
    >>> task.inputs.oned_file = OneD.mock()
    >>> task.inputs.oned_matrix_save = OneD.mock()
    >>> task.inputs.outputtype = "NIFTI"
    >>> task.cmdline
    '3dvolreg -Fourier -twopass -1Dfile functional.1D -1Dmatrix_save functional.aff12.1D -prefix functional_volreg.nii -zpad 4 -maxdisp1D functional_md.1D functional.nii'


    >>> task = Volreg()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = R1.mock(None)
    >>> task.inputs.basefile = Nifti1.mock(None)
    >>> task.inputs.zpad = 1
    >>> task.inputs.oned_file = OneD.mock(None)
    >>> task.inputs.verbose = True
    >>> task.inputs.oned_matrix_save = OneD.mock(None)
    >>> task.inputs.interp = "cubic"
    >>> task.cmdline
    '3dvolreg -cubic -1Dfile dfile.r1.1D -1Dmatrix_save mat.r1.tshift+orig.1D -prefix rm.epi.volreg.r1 -verbose -base functional.nii -zpad 1 -maxdisp1D functional_md.1D functional.nii'


    """

    input_spec = Volreg_input_spec
    output_spec = Volreg_output_spec
    executable = "3dvolreg"
