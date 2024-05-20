from fileformats.generic import File
from fileformats.medimage import Nifti1, NiftiGz
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input dataset",
            "argstr": "-inset {in_file}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "out_file",
        NiftiGz,
        {
            "help_string": "Output dataset.",
            "argstr": "-prefix {out_file}",
            "position": 0,
            "output_file_template": "{in_file}_reho",
        },
    ),
    (
        "chi_sq",
        bool,
        {
            "help_string": "Output the Friedman chi-squared value in addition to the Kendall's W. This option is currently compatible only with the AFNI (BRIK/HEAD) output type; the chi-squared value will be the second sub-brick of the output dataset.",
            "argstr": "-chi_sq",
        },
    ),
    (
        "mask_file",
        File,
        {
            "help_string": "Mask within which ReHo should be calculated voxelwise",
            "argstr": "-mask {mask_file}",
        },
    ),
    (
        "neighborhood",
        ty.Any,
        {
            "help_string": "\nvoxels in neighborhood. can be:\n``faces`` (for voxel and 6 facewise neighbors, only),\n``edges`` (for voxel and 18 face- and edge-wise neighbors),\n``vertices`` (for voxel and 26 face-, edge-, and node-wise neighbors).",
            "argstr": "-nneigh {neighborhood}",
            "xor": ["sphere", "ellipsoid"],
        },
    ),
    (
        "sphere",
        float,
        {
            "help_string": "\\\nFor additional voxelwise neighborhood control, the\nradius R of a desired neighborhood can be put in; R is\na floating point number, and must be >1. Examples of\nthe numbers of voxels in a given radius are as follows\n(you can roughly approximate with the ol' :math:`4\\pi\\,R^3/3`\nthing):\n\n    * R=2.0 -> V=33\n    * R=2.3 -> V=57,\n    * R=2.9 -> V=93,\n    * R=3.1 -> V=123,\n    * R=3.9 -> V=251,\n    * R=4.5 -> V=389,\n    * R=6.1 -> V=949,\n\nbut you can choose most any value.",
            "argstr": "-neigh_RAD {sphere}",
            "xor": ["neighborhood", "ellipsoid"],
        },
    ),
    (
        "ellipsoid",
        ty.Any,
        {
            "help_string": "\\\nTuple indicating the x, y, and z radius of an ellipsoid\ndefining the neighbourhood of each voxel.\nThe 'hood is then made according to the following relation:\n:math:`(i/A)^2 + (j/B)^2 + (k/C)^2 \\le 1.`\nwhich will have approx. :math:`V=4 \\pi \\, A B C/3`. The impetus for\nthis freedom was for use with data having anisotropic\nvoxel edge lengths.",
            "argstr": "-neigh_X {ellipsoid[0]} -neigh_Y {ellipsoid[1]} -neigh_Z {ellipsoid[2]}",
            "xor": ["sphere", "neighborhood"],
        },
    ),
    (
        "label_set",
        File,
        {
            "help_string": "a set of ROIs, each labelled with distinct integers. ReHo will then be calculated per ROI.",
            "argstr": "-in_rois {label_set}",
        },
    ),
    (
        "overwrite",
        bool,
        {
            "help_string": "overwrite output file if it already exists",
            "argstr": "-overwrite",
        },
    ),
]
ReHo_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_vals",
        File,
        {"help_string": "Table of labelwise regional homogeneity values"},
    )
]
ReHo_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ReHo(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1, NiftiGz
    >>> from pydra.tasks.afni.auto.utils.re_ho import ReHo

    >>> task = ReHo()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = NiftiGz.mock(None)
    >>> task.inputs.mask_file = File.mock()
    >>> task.inputs.neighborhood = "vertices"
    >>> task.inputs.label_set = File.mock()
    >>> task.cmdline
    '3dReHo -prefix reho.nii.gz -inset functional.nii -nneigh 27'


    """

    input_spec = ReHo_input_spec
    output_spec = ReHo_output_spec
    executable = "3dReHo"


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input dataset",
            "argstr": "-inset {in_file}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "out_file",
        NiftiGz,
        {
            "help_string": "Output dataset.",
            "argstr": "-prefix {out_file}",
            "position": 0,
            "output_file_template": "{in_file}_reho",
        },
    ),
    (
        "chi_sq",
        bool,
        {
            "help_string": "Output the Friedman chi-squared value in addition to the Kendall's W. This option is currently compatible only with the AFNI (BRIK/HEAD) output type; the chi-squared value will be the second sub-brick of the output dataset.",
            "argstr": "-chi_sq",
        },
    ),
    (
        "mask_file",
        File,
        {
            "help_string": "Mask within which ReHo should be calculated voxelwise",
            "argstr": "-mask {mask_file}",
        },
    ),
    (
        "neighborhood",
        ty.Any,
        {
            "help_string": "\nvoxels in neighborhood. can be:\n``faces`` (for voxel and 6 facewise neighbors, only),\n``edges`` (for voxel and 18 face- and edge-wise neighbors),\n``vertices`` (for voxel and 26 face-, edge-, and node-wise neighbors).",
            "argstr": "-nneigh {neighborhood}",
            "xor": ["sphere", "ellipsoid"],
        },
    ),
    (
        "sphere",
        float,
        {
            "help_string": "\\\nFor additional voxelwise neighborhood control, the\nradius R of a desired neighborhood can be put in; R is\na floating point number, and must be >1. Examples of\nthe numbers of voxels in a given radius are as follows\n(you can roughly approximate with the ol' :math:`4\\pi\\,R^3/3`\nthing):\n\n    * R=2.0 -> V=33\n    * R=2.3 -> V=57,\n    * R=2.9 -> V=93,\n    * R=3.1 -> V=123,\n    * R=3.9 -> V=251,\n    * R=4.5 -> V=389,\n    * R=6.1 -> V=949,\n\nbut you can choose most any value.",
            "argstr": "-neigh_RAD {sphere}",
            "xor": ["neighborhood", "ellipsoid"],
        },
    ),
    (
        "ellipsoid",
        ty.Any,
        {
            "help_string": "\\\nTuple indicating the x, y, and z radius of an ellipsoid\ndefining the neighbourhood of each voxel.\nThe 'hood is then made according to the following relation:\n:math:`(i/A)^2 + (j/B)^2 + (k/C)^2 \\le 1.`\nwhich will have approx. :math:`V=4 \\pi \\, A B C/3`. The impetus for\nthis freedom was for use with data having anisotropic\nvoxel edge lengths.",
            "argstr": "-neigh_X {ellipsoid[0]} -neigh_Y {ellipsoid[1]} -neigh_Z {ellipsoid[2]}",
            "xor": ["sphere", "neighborhood"],
        },
    ),
    (
        "label_set",
        File,
        {
            "help_string": "a set of ROIs, each labelled with distinct integers. ReHo will then be calculated per ROI.",
            "argstr": "-in_rois {label_set}",
        },
    ),
    (
        "overwrite",
        bool,
        {
            "help_string": "overwrite output file if it already exists",
            "argstr": "-overwrite",
        },
    ),
]
re_ho_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_vals",
        File,
        {"help_string": "Table of labelwise regional homogeneity values"},
    )
]
re_ho_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class re_ho(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1, NiftiGz
    >>> from pydra.tasks.afni.auto.utils.re_ho import re_ho

    >>> task = re_ho()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = NiftiGz.mock(None)
    >>> task.inputs.mask_file = File.mock()
    >>> task.inputs.neighborhood = "vertices"
    >>> task.inputs.label_set = File.mock()
    >>> task.cmdline
    '3dReHo -prefix reho.nii.gz -inset functional.nii -nneigh 27'


    """

    input_spec = re_ho_input_spec
    output_spec = re_ho_output_spec
    executable = "3dReHo"
