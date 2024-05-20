from fileformats.medimage import Nifti1, NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.t_correlate import TCorrelate
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_tcorrelate_1():
    task = TCorrelate()
    task.inputs.xset = Nifti1.sample(seed=0)
    task.inputs.yset = Nifti1.sample(seed=1)
    task.inputs.out_file = NiftiGz.sample(seed=2)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_tcorrelate_2():
    task = TCorrelate()
    task.inputs.xset = Nifti1.sample(seed=0)
    task.inputs.yset = Nifti1.sample(seed=1)
    task.inputs.out_file = NiftiGz.sample(seed=2)
    task.inputs.pearson = True
    task.inputs.polort = -1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
