from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.t_norm import TNorm
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_tnorm_1():
    task = TNorm()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_tnorm_2():
    task = TNorm()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.norm2 = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
