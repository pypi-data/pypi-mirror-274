from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dUndump, whose geometry will determinethe geometry of the output",
            "argstr": "-master {in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_file",
        Nifti1,
        {"help_string": "output image file name", "argstr": "-prefix {out_file}"},
    ),
    (
        "mask_file",
        File,
        {
            "help_string": "mask image file name. Only voxels that are nonzero in the mask can be set.",
            "argstr": "-mask {mask_file}",
        },
    ),
    (
        "datatype",
        ty.Any,
        {"help_string": "set output file datatype", "argstr": "-datum {datatype}"},
    ),
    (
        "default_value",
        float,
        {
            "help_string": "default value stored in each input voxel that does not have a value supplied in the input file",
            "argstr": "-dval {default_value}",
        },
    ),
    (
        "fill_value",
        float,
        {
            "help_string": "value, used for each voxel in the output dataset that is NOT listed in the input file",
            "argstr": "-fval {fill_value}",
        },
    ),
    (
        "coordinates_specification",
        ty.Any,
        {
            "help_string": "Coordinates in the input file as index triples (i, j, k) or spatial coordinates (x, y, z) in mm",
            "argstr": "-{coordinates_specification}",
        },
    ),
    (
        "srad",
        float,
        {
            "help_string": "radius in mm of the sphere that will be filled about each input (x,y,z) or (i,j,k) voxel. If the radius is not given, or is 0, then each input data line sets the value in only one voxel.",
            "argstr": "-srad {srad}",
        },
    ),
    (
        "orient",
        ty.Any,
        {
            "help_string": "Specifies the coordinate order used by -xyz. The code must be 3 letters, one each from the pairs {R,L} {A,P} {I,S}.  The first letter gives the orientation of the x-axis, the second the orientation of the y-axis, the third the z-axis: R = right-to-left         L = left-to-right A = anterior-to-posterior P = posterior-to-anterior I = inferior-to-superior  S = superior-to-inferior If -orient isn't used, then the coordinate order of the -master (in_file) dataset is used to interpret (x,y,z) inputs.",
            "argstr": "-orient {orient}",
        },
    ),
    (
        "head_only",
        bool,
        {
            "help_string": "create only the .HEAD file which gets exploited by the AFNI matlab library function New_HEAD.m",
            "argstr": "-head_only",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Undump_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", Nifti1, {"help_string": "assembled file"})]
Undump_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Undump(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.undump import Undump

    >>> task = Undump()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.inputs.mask_file = File.mock()
    >>> task.cmdline
    '3dUndump -prefix structural_undumped.nii -master structural.nii'


    """

    input_spec = Undump_input_spec
    output_spec = Undump_output_spec
    executable = "3dUndump"
