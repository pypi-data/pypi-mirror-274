from fileformats.medimage import Nifti1
from fileformats.medimage_afni import OneD, R1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.volreg import Volreg
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_volreg_1():
    task = Volreg()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = R1.sample(seed=2)
    task.inputs.basefile = Nifti1.sample(seed=3)
    task.inputs.oned_file = OneD.sample(seed=6)
    task.inputs.oned_matrix_save = OneD.sample(seed=10)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_volreg_2():
    task = Volreg()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.zpad = 4
    task.inputs.outputtype = "NIFTI"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_volreg_3():
    task = Volreg()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = R1.sample(seed=2)
    task.inputs.basefile = Nifti1.sample(seed=3)
    task.inputs.zpad = 1
    task.inputs.oned_file = OneD.sample(seed=6)
    task.inputs.verbose = True
    task.inputs.oned_matrix_save = OneD.sample(seed=10)
    task.inputs.interp = "cubic"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
