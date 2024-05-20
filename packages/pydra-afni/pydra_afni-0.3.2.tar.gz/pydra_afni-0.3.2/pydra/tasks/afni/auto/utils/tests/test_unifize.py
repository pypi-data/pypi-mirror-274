from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.unifize import Unifize
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_unifize_1():
    task = Unifize()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = Nifti1.sample(seed=1)
    task.inputs.scale_file = File.sample(seed=5)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_unifize_2():
    task = Unifize()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = Nifti1.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
