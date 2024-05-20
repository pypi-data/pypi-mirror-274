from fileformats.generic import File
from fileformats.medimage import NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.qwarp_plus_minus import QwarpPlusMinus
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_qwarpplusminus_1():
    task = QwarpPlusMinus()
    task.inputs.source_file = File.sample(seed=0)
    task.inputs.out_file = File.sample(seed=1)
    task.inputs.plusminus = True
    task.inputs.in_file = NiftiGz.sample(seed=3)
    task.inputs.base_file = NiftiGz.sample(seed=4)
    task.inputs.weight = File.sample(seed=15)
    task.inputs.out_weight_file = File.sample(seed=18)
    task.inputs.emask = File.sample(seed=21)
    task.inputs.iniwarp = [File.sample(seed=25)]
    task.inputs.gridlist = File.sample(seed=29)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_qwarpplusminus_2():
    task = QwarpPlusMinus()
    task.inputs.in_file = NiftiGz.sample(seed=3)
    task.inputs.base_file = NiftiGz.sample(seed=4)
    task.inputs.nopadWARP = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
