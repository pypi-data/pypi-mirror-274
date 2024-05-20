from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.one_d_tool_py import one_d_tool_py
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_one_d_tool_py_1():
    task = one_d_tool_py()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.set_nruns = 3
    task.inputs.demean = True
    task.inputs.out_file = File.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
