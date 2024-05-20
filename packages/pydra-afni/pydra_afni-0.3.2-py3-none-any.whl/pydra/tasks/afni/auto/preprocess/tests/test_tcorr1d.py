from fileformats.medimage import Nifti1
from fileformats.medimage_afni import OneD
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.t_corr_1d import TCorr1D
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_tcorr1d_1():
    task = TCorr1D()
    task.inputs.xset = Nifti1.sample(seed=0)
    task.inputs.y_1d = OneD.sample(seed=1)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_tcorr1d_2():
    task = TCorr1D()
    task.inputs.xset = Nifti1.sample(seed=0)
    task.inputs.y_1d = OneD.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
