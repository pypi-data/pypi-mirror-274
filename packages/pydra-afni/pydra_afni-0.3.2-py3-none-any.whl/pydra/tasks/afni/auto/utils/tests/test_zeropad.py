from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.zeropad import Zeropad
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_zeropad_1():
    task = Zeropad()
    task.inputs.in_files = Nifti1.sample(seed=0)
    task.inputs.out_file = Nifti1.sample(seed=1)
    task.inputs.master = File.sample(seed=13)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_zeropad_2():
    task = Zeropad()
    task.inputs.in_files = Nifti1.sample(seed=0)
    task.inputs.out_file = Nifti1.sample(seed=1)
    task.inputs.I = 10
    task.inputs.S = 10
    task.inputs.A = 10
    task.inputs.P = 10
    task.inputs.L = 10
    task.inputs.R = 10
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
