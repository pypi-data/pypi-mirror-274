from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.convert_dset import convert_dset
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_convert_dset_1():
    task = convert_dset()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.out_file = File.sample(seed=1)
    task.inputs.out_type = "niml_asc"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
