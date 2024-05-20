from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.means import Means
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_means_1():
    task = Means()
    task.inputs.in_file_a = Nifti1.sample(seed=0)
    task.inputs.in_file_b = Nifti1.sample(seed=1)
    task.inputs.out_file = Nifti1.sample(seed=3)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_means_2():
    task = Means()
    task.inputs.in_file_a = Nifti1.sample(seed=0)
    task.inputs.in_file_b = Nifti1.sample(seed=1)
    task.inputs.out_file = Nifti1.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_means_3():
    task = Means()
    task.inputs.in_file_a = Nifti1.sample(seed=0)
    task.inputs.datum = "short"
    task.inputs.out_file = Nifti1.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
