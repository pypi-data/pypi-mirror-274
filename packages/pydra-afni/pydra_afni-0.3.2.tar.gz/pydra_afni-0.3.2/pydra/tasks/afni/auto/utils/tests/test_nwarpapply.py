from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.nwarp_apply import NwarpApply
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_nwarpapply_1():
    task = NwarpApply()
    task.inputs.master = File.sample(seed=3)
    task.inputs.interp = "wsinc5"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_nwarpapply_2():
    task = NwarpApply()
    task.inputs.in_file = "Fred+orig"
    task.inputs.warp = "'Fred_WARP+tlrc Fred.Xaff12.1D'"
    task.inputs.master = File.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
