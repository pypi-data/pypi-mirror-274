from fileformats.medimage import Nifti1, NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.t_project import t_project
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_t_project_1():
    task = t_project()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = NiftiGz.sample(seed=1)
    task.inputs.polort = 3
    task.inputs.bandpass = (0.00667, 99999)
    task.inputs.automask = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
