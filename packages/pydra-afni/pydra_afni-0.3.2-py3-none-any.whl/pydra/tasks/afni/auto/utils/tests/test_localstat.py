from fileformats.generic import File
from fileformats.medimage import Nifti1, NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.localstat import Localstat
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_localstat_1():
    task = Localstat()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.stat = [File.sample(seed=2)]
    task.inputs.mask_file = NiftiGz.sample(seed=3)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_localstat_2():
    task = Localstat()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.neighborhood = ("SPHERE", 45)
    task.inputs.stat = [File.sample(seed=2)]
    task.inputs.mask_file = NiftiGz.sample(seed=3)
    task.inputs.nonmask = True
    task.inputs.outputtype = "NIFTI_GZ"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
