from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.autobox import Autobox
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_autobox_1():
    task = Autobox()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_autobox_2():
    task = Autobox()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.padding = 5
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
