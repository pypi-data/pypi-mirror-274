from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.edge_3 import Edge3, edge3
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_edge3_1():
    task = edge3()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = Nifti1.sample(seed=1)
    task.inputs.datum = "byte"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_edge3_1():
    task = Edge3()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = Nifti1.sample(seed=1)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_edge3_2():
    task = Edge3()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = Nifti1.sample(seed=1)
    task.inputs.datum = "byte"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
