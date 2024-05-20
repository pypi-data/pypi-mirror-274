from fileformats.generic import File
from fileformats.medimage import Nifti1, NiftiGz
from fileformats.medimage_afni import Head
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.qwarp import Qwarp
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_qwarp_1():
    task = Qwarp()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.base_file = Nifti1.sample(seed=1)
    task.inputs.out_file = NiftiGz.sample(seed=2)
    task.inputs.weight = File.sample(seed=13)
    task.inputs.out_weight_file = File.sample(seed=16)
    task.inputs.emask = File.sample(seed=19)
    task.inputs.iniwarp = [Head.sample(seed=23)]
    task.inputs.gridlist = File.sample(seed=27)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_qwarp_2():
    task = Qwarp()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.base_file = Nifti1.sample(seed=1)
    task.inputs.plusminus = True
    task.inputs.nopadWARP = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_qwarp_3():
    task = Qwarp()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.base_file = Nifti1.sample(seed=1)
    task.inputs.resample = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_qwarp_4():
    task = Qwarp()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.base_file = Nifti1.sample(seed=1)
    task.inputs.out_file = NiftiGz.sample(seed=2)
    task.inputs.resample = True
    task.inputs.iwarp = True
    task.inputs.blur = [0, 3]
    task.inputs.verb = True
    task.inputs.lpc = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_qwarp_5():
    task = Qwarp()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.base_file = Nifti1.sample(seed=1)
    task.inputs.blur = [0, 3]
    task.inputs.duplo = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_qwarp_6():
    task = Qwarp()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.base_file = Nifti1.sample(seed=1)
    task.inputs.out_file = NiftiGz.sample(seed=2)
    task.inputs.blur = [0, 3]
    task.inputs.minpatch = 25
    task.inputs.duplo = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_qwarp_7():
    task = Qwarp()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.base_file = Nifti1.sample(seed=1)
    task.inputs.out_file = NiftiGz.sample(seed=2)
    task.inputs.blur = [0, 2]
    task.inputs.iniwarp = [Head.sample(seed=23)]
    task.inputs.inilev = 7
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_qwarp_8():
    task = Qwarp()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.base_file = Nifti1.sample(seed=1)
    task.inputs.allineate = True
    task.inputs.allineate_opts = "-cose lpa -verb"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
