from fileformats.medimage_afni import OneD
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.cat import Cat
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_cat_1():
    task = Cat()
    task.inputs.in_files = [OneD.sample(seed=0)]
    task.inputs.out_file = OneD.sample(seed=1)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_cat_2():
    task = Cat()
    task.inputs.in_files = [OneD.sample(seed=0)]
    task.inputs.out_file = OneD.sample(seed=1)
    task.inputs.sel = "'[0,2]'"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
