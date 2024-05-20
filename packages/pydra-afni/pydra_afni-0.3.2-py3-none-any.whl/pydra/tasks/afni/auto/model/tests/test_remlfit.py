from fileformats.generic import File
from fileformats.medimage import Nifti1
from fileformats.medimage_afni import OneD
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.model.remlfit import Remlfit
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_remlfit_1():
    task = Remlfit()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.matrix = OneD.sample(seed=1)
    task.inputs.matim = File.sample(seed=3)
    task.inputs.mask = File.sample(seed=4)
    task.inputs.automask = False
    task.inputs.STATmask = File.sample(seed=6)
    task.inputs.addbase = [File.sample(seed=7)]
    task.inputs.slibase = [File.sample(seed=8)]
    task.inputs.slibase_sm = [File.sample(seed=9)]
    task.inputs.dsort = File.sample(seed=12)
    task.inputs.out_file = Nifti1.sample(seed=20)
    task.inputs.var_file = File.sample(seed=21)
    task.inputs.rbeta_file = File.sample(seed=22)
    task.inputs.glt_file = File.sample(seed=23)
    task.inputs.fitts_file = File.sample(seed=24)
    task.inputs.errts_file = File.sample(seed=25)
    task.inputs.wherr_file = File.sample(seed=26)
    task.inputs.ovar = File.sample(seed=30)
    task.inputs.obeta = File.sample(seed=31)
    task.inputs.obuck = File.sample(seed=32)
    task.inputs.oglt = File.sample(seed=33)
    task.inputs.ofitts = File.sample(seed=34)
    task.inputs.oerrts = File.sample(seed=35)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_remlfit_2():
    task = Remlfit()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.matrix = OneD.sample(seed=1)
    task.inputs.gltsym = [
        ("SYM: +Lab1 -Lab2", "TestSYM"),
        ("timeseries.txt", "TestFile"),
    ]
    task.inputs.out_file = Nifti1.sample(seed=20)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
