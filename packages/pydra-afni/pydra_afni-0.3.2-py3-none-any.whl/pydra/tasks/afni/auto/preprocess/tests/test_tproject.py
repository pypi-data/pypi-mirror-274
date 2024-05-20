from fileformats.generic import File
from fileformats.medimage import Nifti1, NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.t_project import TProject
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_tproject_1():
    task = TProject()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = NiftiGz.sample(seed=1)
    task.inputs.censor = File.sample(seed=2)
    task.inputs.concat = File.sample(seed=5)
    task.inputs.ort = File.sample(seed=7)
    task.inputs.dsort = [File.sample(seed=9)]
    task.inputs.mask = File.sample(seed=13)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_tproject_2():
    task = TProject()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = NiftiGz.sample(seed=1)
    task.inputs.polort = 3
    task.inputs.bandpass = (0.00667, 99999)
    task.inputs.automask = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
