from fileformats.medimage import Nifti1, NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.brick_stat import brick_stat
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_brick_stat_1():
    task = brick_stat()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.mask = NiftiGz.sample(seed=1)
    task.inputs.min = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
