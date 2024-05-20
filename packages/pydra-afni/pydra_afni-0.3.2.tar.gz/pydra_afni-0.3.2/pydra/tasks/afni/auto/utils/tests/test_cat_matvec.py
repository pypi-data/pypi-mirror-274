import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.cat_matvec import cat_matvec
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_cat_matvec_1():
    task = cat_matvec()
    task.inputs.in_file = [("structural.BRIK::WARP_DATA", "I")]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
