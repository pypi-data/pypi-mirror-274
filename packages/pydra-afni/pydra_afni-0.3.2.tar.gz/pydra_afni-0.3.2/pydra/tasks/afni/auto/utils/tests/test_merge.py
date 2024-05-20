from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.merge import Merge
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_merge_1():
    task = Merge()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.out_file = Nifti1.sample(seed=1)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_merge_2():
    task = Merge()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.out_file = Nifti1.sample(seed=1)
    task.inputs.doall = True
    task.inputs.blurfwhm = 4
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
