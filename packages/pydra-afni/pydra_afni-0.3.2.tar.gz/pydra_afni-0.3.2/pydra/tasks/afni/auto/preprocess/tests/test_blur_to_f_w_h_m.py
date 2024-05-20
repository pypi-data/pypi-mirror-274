from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.blur_to_f_w_h_m import blur_to_f_w_h_m
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_blur_to_f_w_h_m_1():
    task = blur_to_f_w_h_m()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.fwhm = 2.5
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
