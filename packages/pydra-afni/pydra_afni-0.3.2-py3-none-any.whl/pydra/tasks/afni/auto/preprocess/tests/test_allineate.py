from fileformats.datascience import TextMatrix
from fileformats.generic import File
from fileformats.medimage import Nifti1
from fileformats.text import TextFile
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.allineate import Allineate
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_allineate_1():
    task = Allineate()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.reference = Nifti1.sample(seed=1)
    task.inputs.out_file = Nifti1.sample(seed=2)
    task.inputs.out_param_file = File.sample(seed=3)
    task.inputs.in_param_file = File.sample(seed=4)
    task.inputs.out_matrix = File.sample(seed=5)
    task.inputs.in_matrix = TextMatrix.sample(seed=6)
    task.inputs.allcostx = TextFile.sample(seed=8)
    task.inputs.weight_file = File.sample(seed=29)
    task.inputs.out_weight_file = File.sample(seed=31)
    task.inputs.source_mask = File.sample(seed=32)
    task.inputs.master = File.sample(seed=43)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_allineate_2():
    task = Allineate()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = Nifti1.sample(seed=2)
    task.inputs.in_matrix = TextMatrix.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_allineate_3():
    task = Allineate()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.reference = Nifti1.sample(seed=1)
    task.inputs.allcostx = TextFile.sample(seed=8)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_allineate_4():
    task = Allineate()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.reference = Nifti1.sample(seed=1)
    task.inputs.nwarp_fixmot = ["X", "Y"]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
