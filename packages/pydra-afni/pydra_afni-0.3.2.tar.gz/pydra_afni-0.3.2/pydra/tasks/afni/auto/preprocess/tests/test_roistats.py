from fileformats.generic import File
from fileformats.medimage import Nifti1, NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.roi_stats import ROIStats
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_roistats_1():
    task = ROIStats()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.mask = File.sample(seed=1)
    task.inputs.mask_file = NiftiGz.sample(seed=2)
    task.inputs.roisel = File.sample(seed=6)
    task.inputs.stat = [File.sample(seed=13)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_roistats_2():
    task = ROIStats()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.mask_file = NiftiGz.sample(seed=2)
    task.inputs.nomeanout = True
    task.inputs.stat = [File.sample(seed=13)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
