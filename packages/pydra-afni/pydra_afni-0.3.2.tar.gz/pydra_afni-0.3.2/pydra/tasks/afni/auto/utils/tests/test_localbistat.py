from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.local_bistat import LocalBistat
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_localbistat_1():
    task = LocalBistat()
    task.inputs.in_file1 = Nifti1.sample(seed=0)
    task.inputs.in_file2 = Nifti1.sample(seed=1)
    task.inputs.stat = [File.sample(seed=3)]
    task.inputs.mask_file = File.sample(seed=4)
    task.inputs.weight_file = File.sample(seed=6)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_localbistat_2():
    task = LocalBistat()
    task.inputs.in_file1 = Nifti1.sample(seed=0)
    task.inputs.in_file2 = Nifti1.sample(seed=1)
    task.inputs.neighborhood = ("SPHERE", 1.2)
    task.inputs.stat = [File.sample(seed=3)]
    task.inputs.outputtype = "NIFTI"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
