from fileformats.generic import File
from fileformats.medimage import Nifti1
from fileformats.medimage_afni import NCorr
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.net_corr import NetCorr
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_netcorr_1():
    task = NetCorr()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.in_rois = Nifti1.sample(seed=1)
    task.inputs.mask = Nifti1.sample(seed=2)
    task.inputs.weight_ts = File.sample(seed=3)
    task.inputs.out_file = NCorr.sample(seed=16)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_netcorr_2():
    task = NetCorr()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.in_rois = Nifti1.sample(seed=1)
    task.inputs.mask = Nifti1.sample(seed=2)
    task.inputs.fish_z = True
    task.inputs.ts_wb_corr = True
    task.inputs.ts_wb_Z = True
    task.inputs.out_file = NCorr.sample(seed=16)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
