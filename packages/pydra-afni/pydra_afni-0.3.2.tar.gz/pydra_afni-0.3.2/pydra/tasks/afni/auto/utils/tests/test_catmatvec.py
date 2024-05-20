from fileformats.medimage_afni import OneD
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.cat_matvec import CatMatvec
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_catmatvec_1():
    task = CatMatvec()
    task.inputs.out_file = OneD.sample(seed=1)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_catmatvec_2():
    task = CatMatvec()
    task.inputs.in_file = [("structural.BRIK::WARP_DATA", "I")]
    task.inputs.out_file = OneD.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
