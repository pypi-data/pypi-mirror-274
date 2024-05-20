import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        list,
        {
            "help_string": "List of tuples of input datasets and subbrick selection strings\nas described in more detail in the following afni help string\nInput dataset specified using one of these forms:\n``prefix+view``, ``prefix+view.HEAD``, or ``prefix+view.BRIK``.\nYou can also add a sub-brick selection list after the end of the\ndataset name.  This allows only a subset of the sub-bricks to be\nincluded into the output (by default, all of the input dataset\nis copied into the output).  A sub-brick selection list looks like\none of the following forms::\n\n    fred+orig[5]                     ==> use only sub-brick #5\n    fred+orig[5,9,17]                ==> use #5, #9, and #17\n    fred+orig[5..8]     or [5-8]     ==> use #5, #6, #7, and #8\n    fred+orig[5..13(2)] or [5-13(2)] ==> use #5, #7, #9, #11, and #13\n\nSub-brick indexes start at 0.  You can use the character '$'\nto indicate the last sub-brick in a dataset; for example, you\ncan select every third sub-brick by using the selection list\n``fred+orig[0..$(3)]``\nN.B.: The sub-bricks are output in the order specified, which may\nnot be the order in the original datasets.  For example, using\n``fred+orig[0..$(2),1..$(2)]``\nwill cause the sub-bricks in fred+orig to be output into the\nnew dataset in an interleaved fashion. Using ``fred+orig[$..0]``\nwill reverse the order of the sub-bricks in the output.\nN.B.: Bucket datasets have multiple sub-bricks, but do NOT have\na time dimension.  You can input sub-bricks from a 3D+time dataset\ninto a bucket dataset.  You can use the '3dinfo' program to see\nhow many sub-bricks a 3D+time or a bucket dataset contains.\nN.B.: In non-bucket functional datasets (like the 'fico' datasets\noutput by FIM, or the 'fitt' datasets output by 3dttest), sub-brick\n``[0]`` is the 'intensity' and sub-brick [1] is the statistical parameter\nused as a threshold.  Thus, to create a bucket dataset using the\nintensity from dataset A and the threshold from dataset B, and\ncalling the output dataset C, you would type::\n\n    3dbucket -prefix C -fbuc 'A+orig[0]' -fbuc 'B+orig[1]\n\n",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "",
            "argstr": "-prefix {out_file}",
            "output_file_template": "buck",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Bucket_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Bucket_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Bucket(ShellCommandTask):
    """
    Examples
    -------

    >>> from pydra.tasks.afni.auto.utils.bucket import Bucket

    >>> task = Bucket()
    >>> task.inputs.in_file = [('functional.nii',"{2..$}"), ('functional.nii',"{1}")]
    >>> task.inputs.out_file = None
    >>> task.cmdline
    '3dbucket -prefix vr_base functional.nii"{2..$}" functional.nii"{1}"'


    """

    input_spec = Bucket_input_spec
    output_spec = Bucket_output_spec
    executable = "3dbucket"
