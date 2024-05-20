from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.nwarp_apply import nwarp_apply
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_nwarp_apply_1():
    task = nwarp_apply()
    task.inputs.in_file = "Fred+orig"
    task.inputs.warp = "'Fred_WARP+tlrc Fred.Xaff12.1D'"
    task.inputs.master = File.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
