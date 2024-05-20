from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.auto_tcorrelate import auto_tcorrelate
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_auto_tcorrelate_1():
    task = auto_tcorrelate()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.polort = -1
    task.inputs.eta2 = True
    task.inputs.mask = Nifti1.sample(seed=3)
    task.inputs.mask_only_targets = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
