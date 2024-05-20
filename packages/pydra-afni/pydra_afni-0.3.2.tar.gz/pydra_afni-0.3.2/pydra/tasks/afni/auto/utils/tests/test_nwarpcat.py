import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.nwarp_cat import NwarpCat
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_nwarpcat_1():
    task = NwarpCat()
    task.inputs.interp = "wsinc5"
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_nwarpcat_2():
    task = NwarpCat()
    task.inputs.in_files = ["Q25_warp+tlrc.HEAD", ("IDENT", "structural.nii")]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
