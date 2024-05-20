from fileformats.generic import File
from fileformats.medimage_afni import OneD
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.one_d_tool_py import OneDToolPy
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_onedtoolpy_1():
    task = OneDToolPy()
    task.inputs.in_file = OneD.sample(seed=0)
    task.inputs.out_file = OneD.sample(seed=4)
    task.inputs.show_cormat_warnings = File.sample(seed=9)
    task.inputs.py27_path = "python2"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_onedtoolpy_2():
    task = OneDToolPy()
    task.inputs.in_file = OneD.sample(seed=0)
    task.inputs.set_nruns = 3
    task.inputs.demean = True
    task.inputs.out_file = OneD.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
