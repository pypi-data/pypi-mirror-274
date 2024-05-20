from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.zcat import Zcat
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_zcat_1():
    task = Zcat()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.out_file = Nifti1.sample(seed=1)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_zcat_2():
    task = Zcat()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.out_file = Nifti1.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
