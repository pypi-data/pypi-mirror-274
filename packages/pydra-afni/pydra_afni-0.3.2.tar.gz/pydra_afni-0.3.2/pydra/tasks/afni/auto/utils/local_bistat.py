from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file1",
        Nifti1,
        {
            "help_string": "Filename of the first image",
            "argstr": "{in_file1}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "in_file2",
        Nifti1,
        {
            "help_string": "Filename of the second image",
            "argstr": "{in_file2}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "neighborhood",
        ty.Any,
        {
            "help_string": "The region around each voxel that will be extracted for the statistics calculation. Possible regions are: 'SPHERE', 'RHDD' (rhombic dodecahedron), 'TOHD' (truncated octahedron) with a given radius in mm or 'RECT' (rectangular block) with dimensions to specify in mm.",
            "argstr": "-nbhd '{neighborhood[0]}({neighborhood[1]})'",
            "mandatory": True,
        },
    ),
    (
        "stat",
        ty.List[File],
        {
            "help_string": "Statistics to compute. Possible names are:\n\n  * pearson  = Pearson correlation coefficient\n  * spearman = Spearman correlation coefficient\n  * quadrant = Quadrant correlation coefficient\n  * mutinfo  = Mutual Information\n  * normuti  = Normalized Mutual Information\n  * jointent = Joint entropy\n  * hellinger= Hellinger metric\n  * crU      = Correlation ratio (Unsymmetric)\n  * crM      = Correlation ratio (symmetrized by Multiplication)\n  * crA      = Correlation ratio (symmetrized by Addition)\n  * L2slope  = slope of least-squares (L2) linear regression of\n               the data from dataset1 vs. the dataset2\n               (i.e., d2 = a + b*d1 ==> this is 'b')\n  * L1slope  = slope of least-absolute-sum (L1) linear\n               regression of the data from dataset1 vs.\n               the dataset2\n  * num      = number of the values in the region:\n               with the use of -mask or -automask,\n               the size of the region around any given\n               voxel will vary; this option lets you\n               map that size.\n  * ALL      = all of the above, in that order\n\nMore than one option can be used.",
            "argstr": "-stat {stat}...",
            "mandatory": True,
        },
    ),
    (
        "mask_file",
        File,
        {
            "help_string": "mask image file name. Voxels NOT in the mask will not be used in the neighborhood of any voxel. Also, a voxel NOT in the mask will have its statistic(s) computed as zero (0).",
            "argstr": "-mask {mask_file}",
        },
    ),
    (
        "automask",
        bool,
        {
            "help_string": "Compute the mask as in program 3dAutomask.",
            "argstr": "-automask",
            "xor": ["weight_file"],
        },
    ),
    (
        "weight_file",
        File,
        {
            "help_string": "File name of an image to use as a weight.  Only applies to 'pearson' statistics.",
            "argstr": "-weight {weight_file}",
            "xor": ["automask"],
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Output dataset.",
            "argstr": "-prefix {out_file}",
            "position": 0,
            "output_file_template": "{in_file1}_bistat",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
LocalBistat_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
LocalBistat_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class LocalBistat(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.local_bistat import LocalBistat

    >>> task = LocalBistat()
    >>> task.inputs.in_file1 = Nifti1.mock(None)
    >>> task.inputs.in_file2 = Nifti1.mock(None)
    >>> task.inputs.neighborhood = ("SPHERE", 1.2)
    >>> task.inputs.stat = None
    >>> task.inputs.mask_file = File.mock()
    >>> task.inputs.weight_file = File.mock()
    >>> task.inputs.outputtype = "NIFTI"
    >>> task.cmdline
    '3dLocalBistat -prefix functional_bistat.nii -nbhd "SPHERE(1.2)" -stat pearson functional.nii structural.nii'


    """

    input_spec = LocalBistat_input_spec
    output_spec = LocalBistat_output_spec
    executable = "3dLocalBistat"


input_fields = [
    (
        "in_file1",
        Nifti1,
        {
            "help_string": "Filename of the first image",
            "argstr": "{in_file1}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "in_file2",
        Nifti1,
        {
            "help_string": "Filename of the second image",
            "argstr": "{in_file2}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "neighborhood",
        ty.Any,
        {
            "help_string": "The region around each voxel that will be extracted for the statistics calculation. Possible regions are: 'SPHERE', 'RHDD' (rhombic dodecahedron), 'TOHD' (truncated octahedron) with a given radius in mm or 'RECT' (rectangular block) with dimensions to specify in mm.",
            "argstr": "-nbhd '{neighborhood[0]}({neighborhood[1]})'",
            "mandatory": True,
        },
    ),
    (
        "stat",
        ty.List[File],
        {
            "help_string": "Statistics to compute. Possible names are:\n\n  * pearson  = Pearson correlation coefficient\n  * spearman = Spearman correlation coefficient\n  * quadrant = Quadrant correlation coefficient\n  * mutinfo  = Mutual Information\n  * normuti  = Normalized Mutual Information\n  * jointent = Joint entropy\n  * hellinger= Hellinger metric\n  * crU      = Correlation ratio (Unsymmetric)\n  * crM      = Correlation ratio (symmetrized by Multiplication)\n  * crA      = Correlation ratio (symmetrized by Addition)\n  * L2slope  = slope of least-squares (L2) linear regression of\n               the data from dataset1 vs. the dataset2\n               (i.e., d2 = a + b*d1 ==> this is 'b')\n  * L1slope  = slope of least-absolute-sum (L1) linear\n               regression of the data from dataset1 vs.\n               the dataset2\n  * num      = number of the values in the region:\n               with the use of -mask or -automask,\n               the size of the region around any given\n               voxel will vary; this option lets you\n               map that size.\n  * ALL      = all of the above, in that order\n\nMore than one option can be used.",
            "argstr": "-stat {stat}...",
            "mandatory": True,
        },
    ),
    (
        "mask_file",
        File,
        {
            "help_string": "mask image file name. Voxels NOT in the mask will not be used in the neighborhood of any voxel. Also, a voxel NOT in the mask will have its statistic(s) computed as zero (0).",
            "argstr": "-mask {mask_file}",
        },
    ),
    (
        "automask",
        bool,
        {
            "help_string": "Compute the mask as in program 3dAutomask.",
            "argstr": "-automask",
            "xor": ["weight_file"],
        },
    ),
    (
        "weight_file",
        File,
        {
            "help_string": "File name of an image to use as a weight.  Only applies to 'pearson' statistics.",
            "argstr": "-weight {weight_file}",
            "xor": ["automask"],
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Output dataset.",
            "argstr": "-prefix {out_file}",
            "position": 0,
            "output_file_template": "{in_file1}_bistat",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
local_bistat_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
local_bistat_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class local_bistat(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.local_bistat import local_bistat

    >>> task = local_bistat()
    >>> task.inputs.in_file1 = Nifti1.mock(None)
    >>> task.inputs.in_file2 = Nifti1.mock(None)
    >>> task.inputs.neighborhood = ("SPHERE", 1.2)
    >>> task.inputs.stat = None
    >>> task.inputs.mask_file = File.mock()
    >>> task.inputs.weight_file = File.mock()
    >>> task.inputs.outputtype = "NIFTI"
    >>> task.cmdline
    '3dLocalBistat -prefix functional_bistat.nii -nbhd "SPHERE(1.2)" -stat pearson functional.nii structural.nii'


    """

    input_spec = local_bistat_input_spec
    output_spec = local_bistat_output_spec
    executable = "3dLocalBistat"
