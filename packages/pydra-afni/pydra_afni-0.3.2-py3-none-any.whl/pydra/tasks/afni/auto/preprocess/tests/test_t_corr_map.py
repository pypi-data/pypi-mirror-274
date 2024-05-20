from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.t_corr_map import t_corr_map
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_t_corr_map_1():
    task = t_corr_map()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.mask = Nifti1.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
