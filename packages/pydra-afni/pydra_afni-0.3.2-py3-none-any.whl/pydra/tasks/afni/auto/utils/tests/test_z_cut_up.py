from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.z_cut_up import z_cut_up
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_z_cut_up_1():
    task = z_cut_up()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = Nifti1.sample(seed=1)
    task.inputs.keep = "0 10"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
