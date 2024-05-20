from fileformats.medimage import Nifti1, NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.re_ho import re_ho
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_re_ho_1():
    task = re_ho()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = NiftiGz.sample(seed=1)
    task.inputs.neighborhood = "vertices"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
