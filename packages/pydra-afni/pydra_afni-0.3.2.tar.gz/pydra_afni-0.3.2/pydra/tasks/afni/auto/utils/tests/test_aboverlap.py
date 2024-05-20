from fileformats.medimage import Nifti1
from fileformats.text import TextFile
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.a_boverlap import ABoverlap
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_aboverlap_1():
    task = ABoverlap()
    task.inputs.in_file_a = Nifti1.sample(seed=0)
    task.inputs.in_file_b = Nifti1.sample(seed=1)
    task.inputs.out_file = TextFile.sample(seed=2)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_aboverlap_2():
    task = ABoverlap()
    task.inputs.in_file_a = Nifti1.sample(seed=0)
    task.inputs.in_file_b = Nifti1.sample(seed=1)
    task.inputs.out_file = TextFile.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
