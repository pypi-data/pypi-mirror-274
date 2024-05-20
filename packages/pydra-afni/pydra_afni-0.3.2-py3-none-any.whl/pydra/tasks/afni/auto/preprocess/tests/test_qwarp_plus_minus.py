from fileformats.medimage import NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.qwarp_plus_minus import qwarp_plus_minus
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_qwarp_plus_minus_1():
    task = qwarp_plus_minus()
    task.inputs.in_file = NiftiGz.sample(seed=3)
    task.inputs.base_file = NiftiGz.sample(seed=4)
    task.inputs.nopadWARP = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
