from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.lfcd import LFCD
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_lfcd_1():
    task = LFCD()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.mask = Nifti1.sample(seed=1)
    task.inputs.num_threads = 1
    task.inputs.out_file = Nifti1.sample(seed=8)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_lfcd_2():
    task = LFCD()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.mask = Nifti1.sample(seed=1)
    task.inputs.thresh = 0.8  # keep all connections with corr >= 0.8
    task.inputs.out_file = Nifti1.sample(seed=8)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
