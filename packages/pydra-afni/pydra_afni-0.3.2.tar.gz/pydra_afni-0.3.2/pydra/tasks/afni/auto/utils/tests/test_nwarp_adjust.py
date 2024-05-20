from fileformats.medimage import NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.nwarp_adjust import nwarp_adjust
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_nwarp_adjust_1():
    task = nwarp_adjust()
    task.inputs.warps = [NiftiGz.sample(seed=0)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
