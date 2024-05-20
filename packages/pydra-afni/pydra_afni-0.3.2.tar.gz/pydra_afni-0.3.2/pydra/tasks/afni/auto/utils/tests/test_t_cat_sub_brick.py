import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.t_cat_sub_brick import t_cat_sub_brick
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_t_cat_sub_brick_1():
    task = t_cat_sub_brick()
    task.inputs.in_files = [
        ("functional.nii", "'{2..$}'"),
        ("functional2.nii", "'{2..$}'"),
    ]
    task.inputs.out_file = "functional_tcat.nii"
    task.inputs.rlt = "+"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
