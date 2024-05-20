from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.hist import Hist
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_hist_1():
    task = Hist()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.showhist = False
    task.inputs.mask = File.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_hist_2():
    task = Hist()
    task.inputs.in_file = Nifti1.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
