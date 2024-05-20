from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.t_corr_1_d import t_corr1_d
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_t_corr1_d_1():
    task = t_corr1_d()
    task.inputs.xset = Nifti1.sample(seed=0)
    task.inputs.y_1d = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
