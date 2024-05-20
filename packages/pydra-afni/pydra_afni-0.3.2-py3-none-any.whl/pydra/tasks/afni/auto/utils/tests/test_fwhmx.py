from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.fwh_mx import FWHMx
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_fwhmx_1():
    task = FWHMx()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.mask = File.sample(seed=3)
    task.inputs.automask = False
    task.inputs.detrend = False
    task.inputs.acf = False
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_fwhmx_2():
    task = FWHMx()
    task.inputs.in_file = Nifti1.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
