from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.auto_tlrc import AutoTLRC
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_autotlrc_1():
    task = AutoTLRC()
    task.inputs.in_file = Nifti1.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_autotlrc_2():
    task = AutoTLRC()
    task.inputs.in_file = Nifti1.sample(seed=1)
    task.inputs.base = "TT_N27+tlrc"
    task.inputs.no_ss = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
