from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.mask_tool import mask_tool
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mask_tool_1():
    task = mask_tool()
    task.inputs.in_file = [Nifti1.sample(seed=0)]
    task.inputs.outputtype = "NIFTI"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
