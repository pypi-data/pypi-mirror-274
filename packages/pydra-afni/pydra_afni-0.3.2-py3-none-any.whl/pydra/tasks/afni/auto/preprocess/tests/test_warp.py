from fileformats.generic import File
from fileformats.medimage import Nifti1, NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.warp import Warp
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_warp_1():
    task = Warp()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = NiftiGz.sample(seed=1)
    task.inputs.matparent = File.sample(seed=4)
    task.inputs.oblique_parent = File.sample(seed=5)
    task.inputs.gridset = File.sample(seed=8)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_warp_2():
    task = Warp()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = NiftiGz.sample(seed=1)
    task.inputs.deoblique = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_warp_3():
    task = Warp()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = NiftiGz.sample(seed=1)
    task.inputs.newgrid = 1.0
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
