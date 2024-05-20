from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.t_shift import TShift
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_tshift_1():
    task = TShift()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.slice_encoding_direction = "k"
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_tshift_2():
    task = TShift()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.tr = "%.1fs" % TR
    task.inputs.tzero = 0.0
    task.inputs.slice_timing = list(np.arange(40) / TR)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_tshift_3():
    task = TShift()
    task.inputs.slice_encoding_direction = "k-"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_tshift_4():
    task = TShift()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.tr = "%.1fs" % TR
    task.inputs.tzero = 0.0
    task.inputs.slice_timing = "slice_timing.1D"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_tshift_5():
    task = TShift()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.tr = "%.1fs" % TR
    task.inputs.tzero = 0.0
    task.inputs.tpattern = "alt+z"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_tshift_6():
    task = TShift()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.tr = "%.1fs" % TR
    task.inputs.tzero = 0.0
    task.inputs.tpattern = "@slice_timing.1D"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
