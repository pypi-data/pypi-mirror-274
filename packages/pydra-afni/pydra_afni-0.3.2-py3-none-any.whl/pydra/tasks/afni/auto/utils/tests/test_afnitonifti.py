from fileformats.medimage import Nifti1
from fileformats.medimage_afni import ThreeD
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.afn_ito_nifti import AFNItoNIFTI
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_afnitonifti_1():
    task = AFNItoNIFTI()
    task.inputs.in_file = ThreeD.sample(seed=0)
    task.inputs.out_file = Nifti1.sample(seed=1)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_afnitonifti_2():
    task = AFNItoNIFTI()
    task.inputs.in_file = ThreeD.sample(seed=0)
    task.inputs.out_file = Nifti1.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
