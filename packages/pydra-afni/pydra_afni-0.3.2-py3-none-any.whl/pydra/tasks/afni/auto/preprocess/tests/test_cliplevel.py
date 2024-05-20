from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.clip_level import ClipLevel
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_cliplevel_1():
    task = ClipLevel()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.grad = File.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_cliplevel_2():
    task = ClipLevel()
    task.inputs.in_file = Nifti1.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
