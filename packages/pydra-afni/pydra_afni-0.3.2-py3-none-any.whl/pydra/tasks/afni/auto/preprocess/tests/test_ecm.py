from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.ecm import ECM
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_ecm_1():
    task = ECM()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.mask = Nifti1.sample(seed=9)
    task.inputs.num_threads = 1
    task.inputs.out_file = Nifti1.sample(seed=16)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_ecm_2():
    task = ECM()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.sparsity = 0.1  # keep top 0.1% of connections
    task.inputs.mask = Nifti1.sample(seed=9)
    task.inputs.out_file = Nifti1.sample(seed=16)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
