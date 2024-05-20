from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.seg import Seg
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_seg_1():
    task = Seg()
    task.inputs.in_file = Nifti1.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_seg_2():
    task = Seg()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.mask = "AUTO"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
