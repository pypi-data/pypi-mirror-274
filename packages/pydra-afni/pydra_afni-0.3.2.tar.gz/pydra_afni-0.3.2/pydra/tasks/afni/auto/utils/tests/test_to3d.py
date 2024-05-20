from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.to_3d import To3D
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_to3d_1():
    task = To3D()
    task.inputs.out_file = Nifti1.sample(seed=0)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_to3d_2():
    task = To3D()
    task.inputs.out_file = Nifti1.sample(seed=0)
    task.inputs.in_folder = "."
    task.inputs.filetype = "anat"
    task.inputs.datatype = "float"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
