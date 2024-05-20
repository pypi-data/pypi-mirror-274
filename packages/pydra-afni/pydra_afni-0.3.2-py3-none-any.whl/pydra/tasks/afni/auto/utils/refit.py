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
            "help_string": "input file to 3drefit",
            "argstr": "{in_file}",
            "copyfile": True,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "deoblique",
        bool,
        {
            "help_string": "replace current transformation matrix with cardinal matrix",
            "argstr": "-deoblique",
        },
    ),
    (
        "xorigin",
        str,
        {
            "help_string": "x distance for edge voxel offset",
            "argstr": "-xorigin {xorigin}",
        },
    ),
    (
        "yorigin",
        str,
        {
            "help_string": "y distance for edge voxel offset",
            "argstr": "-yorigin {yorigin}",
        },
    ),
    (
        "zorigin",
        str,
        {
            "help_string": "z distance for edge voxel offset",
            "argstr": "-zorigin {zorigin}",
        },
    ),
    (
        "duporigin_file",
        File,
        {
            "help_string": "Copies the xorigin, yorigin, and zorigin values from the header of the given dataset",
            "argstr": "-duporigin {duporigin_file}",
        },
    ),
    (
        "xdel",
        float,
        {"help_string": "new x voxel dimension in mm", "argstr": "-xdel {xdel}"},
    ),
    (
        "ydel",
        float,
        {"help_string": "new y voxel dimension in mm", "argstr": "-ydel {ydel}"},
    ),
    (
        "zdel",
        float,
        {"help_string": "new z voxel dimension in mm", "argstr": "-zdel {zdel}"},
    ),
    (
        "xyzscale",
        float,
        {
            "help_string": "Scale the size of the dataset voxels by the given factor",
            "argstr": "-xyzscale {xyzscale}",
        },
    ),
    (
        "space",
        ty.Any,
        {
            "help_string": "Associates the dataset with a specific template type, e.g. TLRC, MNI, ORIG",
            "argstr": "-space {space}",
        },
    ),
    (
        "atrcopy",
        ty.Any,
        {
            "help_string": "Copy AFNI header attribute from the given file into the header of the dataset(s) being modified. For more information on AFNI header attributes, see documentation file README.attributes. More than one '-atrcopy' option can be used. For AFNI advanced users only. Do NOT use -atrcopy or -atrstring with other modification options. See also -copyaux.",
            "argstr": "-atrcopy {atrcopy[0]} {atrcopy[1]}",
        },
    ),
    (
        "atrstring",
        ty.Any,
        {
            "help_string": "Copy the last given string into the dataset(s) being modified, giving it the attribute name given by the last string.To be safe, the last string should be in quotes.",
            "argstr": "-atrstring {atrstring[0]} {atrstring[1]}",
        },
    ),
    (
        "atrfloat",
        ty.Any,
        {
            "help_string": "Create or modify floating point attributes. The input values may be specified as a single string in quotes or as a 1D filename or string, example '1 0.2 0 0 -0.2 1 0 0 0 0 1 0' or flipZ.1D or '1D:1,0.2,2@0,-0.2,1,2@0,2@0,1,0'",
            "argstr": "-atrfloat {atrfloat[0]} {atrfloat[1]}",
        },
    ),
    (
        "atrint",
        ty.Any,
        {
            "help_string": "Create or modify integer attributes. The input values may be specified as a single string in quotes or as a 1D filename or string, example '1 0 0 0 0 1 0 0 0 0 1 0' or flipZ.1D or '1D:1,0,2@0,-0,1,2@0,2@0,1,0'",
            "argstr": "-atrint {atrint[0]} {atrint[1]}",
        },
    ),
    (
        "saveatr",
        bool,
        {
            "help_string": "(default) Copy the attributes that are known to AFNI into the dset->dblk structure thereby forcing changes to known attributes to be present in the output. This option only makes sense with -atrcopy.",
            "argstr": "-saveatr",
        },
    ),
    (
        "nosaveatr",
        bool,
        {"help_string": "Opposite of -saveatr", "argstr": "-nosaveatr"},
    ),
]
Refit_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", File, {"help_string": "output file"})]
Refit_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Refit(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.refit import Refit

    >>> task = Refit()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.deoblique = True
    >>> task.inputs.duporigin_file = File.mock()
    >>> task.cmdline
    '3drefit -deoblique structural.nii'


    >>> task = Refit()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.duporigin_file = File.mock()
    >>> task.inputs.atrfloat = ("IJK_TO_DICOM_REAL", "'1 0.2 0 0 -0.2 1 0 0 0 0 1 0'")
    >>> task.cmdline
    '3drefit -atrfloat IJK_TO_DICOM_REAL "1 0.2 0 0 -0.2 1 0 0 0 0 1 0" structural.nii'


    """

    input_spec = Refit_input_spec
    output_spec = Refit_output_spec
    executable = "3drefit"
