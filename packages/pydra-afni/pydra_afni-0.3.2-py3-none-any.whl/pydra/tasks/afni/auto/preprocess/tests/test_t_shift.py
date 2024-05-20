from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.t_shift import t_shift
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_t_shift_1():
    task = t_shift()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.tr = "%.1fs" % TR
    task.inputs.tzero = 0.0
    task.inputs.slice_timing = list(np.arange(40) / TR)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_t_shift_2():
    task = t_shift()
    task.inputs.slice_encoding_direction = "k-"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_t_shift_3():
    task = t_shift()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.tr = "%.1fs" % TR
    task.inputs.tzero = 0.0
    task.inputs.slice_timing = "slice_timing.1D"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_t_shift_4():
    task = t_shift()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.tr = "%.1fs" % TR
    task.inputs.tzero = 0.0
    task.inputs.tpattern = "alt+z"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_t_shift_5():
    task = t_shift()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.tr = "%.1fs" % TR
    task.inputs.tzero = 0.0
    task.inputs.tpattern = "@slice_timing.1D"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
