from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.svm.svm_test import SVMTest
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_svmtest_1():
    task = SVMTest()
    task.inputs.in_file = File.sample(seed=1)
    task.inputs.testlabels = File.sample(seed=3)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
