from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.f_w_h_mx import f_w_h_mx
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_f_w_h_mx_1():
    task = f_w_h_mx()
    task.inputs.in_file = Nifti1.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
