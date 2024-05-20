from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.to_3_d import to3_d
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_to3_d_1():
    task = to3_d()
    task.inputs.out_file = Nifti1.sample(seed=0)
    task.inputs.in_folder = "."
    task.inputs.filetype = "anat"
    task.inputs.datatype = "float"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
