from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.outlier_count import OutlierCount
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_outliercount_1():
    task = OutlierCount()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.mask = File.sample(seed=1)
    task.inputs.qthr = 0.001
    task.inputs.autoclip = False
    task.inputs.automask = False
    task.inputs.fraction = False
    task.inputs.interval = False
    task.inputs.save_outliers = False
    task.inputs.legendre = False
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_outliercount_2():
    task = OutlierCount()
    task.inputs.in_file = Nifti1.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
