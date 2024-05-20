from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.resample import Resample
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_resample_1():
    task = Resample()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.master = File.sample(seed=5)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_resample_2():
    task = Resample()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.orientation = "RPI"
    task.inputs.outputtype = "NIFTI"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
