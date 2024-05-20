from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.t_smooth import t_smooth
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_t_smooth_1():
    task = t_smooth()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.adaptive = 5
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
