from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.mask_tool import MaskTool
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_masktool_1():
    task = MaskTool()
    task.inputs.in_file = [Nifti1.sample(seed=0)]
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_masktool_2():
    task = MaskTool()
    task.inputs.in_file = [Nifti1.sample(seed=0)]
    task.inputs.outputtype = "NIFTI"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
