from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.t_corr_map import TCorrMap
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_tcorrmap_1():
    task = TCorrMap()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.seeds = File.sample(seed=1)
    task.inputs.mask = Nifti1.sample(seed=2)
    task.inputs.regress_out_timeseries = File.sample(seed=6)
    task.inputs.mean_file = File.sample(seed=9)
    task.inputs.zmean = File.sample(seed=10)
    task.inputs.qmean = File.sample(seed=11)
    task.inputs.pmean = File.sample(seed=12)
    task.inputs.absolute_threshold = File.sample(seed=14)
    task.inputs.var_absolute_threshold = File.sample(seed=15)
    task.inputs.var_absolute_threshold_normalize = File.sample(seed=16)
    task.inputs.correlation_maps = File.sample(seed=17)
    task.inputs.correlation_maps_masked = File.sample(seed=18)
    task.inputs.average_expr = File.sample(seed=20)
    task.inputs.average_expr_nonzero = File.sample(seed=21)
    task.inputs.sum_expr = File.sample(seed=22)
    task.inputs.histogram = File.sample(seed=24)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_tcorrmap_2():
    task = TCorrMap()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.mask = Nifti1.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
