from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.quality_index import QualityIndex
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_qualityindex_1():
    task = QualityIndex()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.mask = File.sample(seed=1)
    task.inputs.spearman = False
    task.inputs.quadrant = False
    task.inputs.autoclip = False
    task.inputs.automask = False
    task.inputs.interval = False
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_qualityindex_2():
    task = QualityIndex()
    task.inputs.in_file = Nifti1.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
