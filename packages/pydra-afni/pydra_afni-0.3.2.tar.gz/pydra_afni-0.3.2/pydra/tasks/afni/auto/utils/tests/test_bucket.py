import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.bucket import Bucket
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_bucket_1():
    task = Bucket()
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_bucket_2():
    task = Bucket()
    task.inputs.in_file = [("functional.nii", "{2..$}"), ("functional.nii", "{1}")]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
