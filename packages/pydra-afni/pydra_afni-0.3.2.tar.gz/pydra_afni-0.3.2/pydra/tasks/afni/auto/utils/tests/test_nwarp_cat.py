import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.nwarp_cat import nwarp_cat
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_nwarp_cat_1():
    task = nwarp_cat()
    task.inputs.in_files = ["Q25_warp+tlrc.HEAD", ("IDENT", "structural.nii")]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
