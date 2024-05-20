from fileformats.medimage import Nifti1
from fileformats.medimage_afni import OneD
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.fim import Fim
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_fim_1():
    task = Fim()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = Nifti1.sample(seed=1)
    task.inputs.ideal_file = OneD.sample(seed=2)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_fim_2():
    task = Fim()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = Nifti1.sample(seed=1)
    task.inputs.ideal_file = OneD.sample(seed=2)
    task.inputs.fim_thr = 0.0009
    task.inputs.out = "Correlation"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
