from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.svm.svm_train import SVMTrain
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_svmtrain_1():
    task = SVMTrain()
    task.inputs.in_file = File.sample(seed=1)
    task.inputs.mask = File.sample(seed=5)
    task.inputs.trainlabels = File.sample(seed=7)
    task.inputs.censor = File.sample(seed=8)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
