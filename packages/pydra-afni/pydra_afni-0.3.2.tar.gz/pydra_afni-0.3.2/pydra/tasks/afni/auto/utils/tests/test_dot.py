from fileformats.generic import File
from fileformats.medimage import Nifti
from fileformats.text import TextFile
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.dot import Dot
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_dot_1():
    task = Dot()
    task.inputs.in_files = [Nifti.sample(seed=0)]
    task.inputs.out_file = TextFile.sample(seed=1)
    task.inputs.mask = File.sample(seed=2)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_dot_2():
    task = Dot()
    task.inputs.in_files = [Nifti.sample(seed=0)]
    task.inputs.out_file = TextFile.sample(seed=1)
    task.inputs.dodice = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
