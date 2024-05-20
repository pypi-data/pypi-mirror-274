from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.net_corr import net_corr
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_net_corr_1():
    task = net_corr()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.in_rois = Nifti1.sample(seed=1)
    task.inputs.mask = Nifti1.sample(seed=2)
    task.inputs.fish_z = True
    task.inputs.ts_wb_corr = True
    task.inputs.ts_wb_Z = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
