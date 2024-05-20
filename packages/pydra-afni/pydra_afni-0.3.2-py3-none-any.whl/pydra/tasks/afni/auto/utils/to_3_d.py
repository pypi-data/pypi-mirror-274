from fileformats.medimage import Nifti1
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "out_file",
        Nifti1,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_folder}",
        },
    ),
    (
        "in_folder",
        ty.Any,
        {
            "help_string": "folder with DICOM images to convert",
            "argstr": "{in_folder}/*.dcm",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "filetype",
        ty.Any,
        {"help_string": "type of datafile being converted", "argstr": "-{filetype}"},
    ),
    (
        "skipoutliers",
        bool,
        {"help_string": "skip the outliers check", "argstr": "-skip_outliers"},
    ),
    (
        "assumemosaic",
        bool,
        {
            "help_string": "assume that Siemens image is mosaic",
            "argstr": "-assume_dicom_mosaic",
        },
    ),
    (
        "datatype",
        ty.Any,
        {"help_string": "set output file datatype", "argstr": "-datum {datatype}"},
    ),
    (
        "funcparams",
        str,
        {
            "help_string": "parameters for functional data",
            "argstr": "-time:zt {funcparams} alt+z2",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
to3_d_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
to3_d_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class to3_d(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.to_3_d import to3_d

    >>> task = to3_d()
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.inputs.in_folder = "."
    >>> task.inputs.filetype = "anat"
    >>> task.inputs.datatype = "float"
    >>> task.cmdline
    'to3d -datum float -anat -prefix dicomdir.nii ./*.dcm'


    """

    input_spec = to3_d_input_spec
    output_spec = to3_d_output_spec
    executable = "to3d"
