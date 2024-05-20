from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.blur_in_mask import blur_in_mask
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_blur_in_mask_1():
    task = blur_in_mask()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.mask = Nifti1.sample(seed=2)
    task.inputs.fwhm = 5.0
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
