from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.t_cat import t_cat
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_t_cat_1():
    task = t_cat()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.out_file = Nifti1.sample(seed=1)
    task.inputs.rlt = "+"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
