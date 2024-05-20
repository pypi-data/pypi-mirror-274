from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.fourier import Fourier
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_fourier_1():
    task = Fourier()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_fourier_2():
    task = Fourier()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.lowpass = 0.1
    task.inputs.highpass = 0.005
    task.inputs.retrend = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
