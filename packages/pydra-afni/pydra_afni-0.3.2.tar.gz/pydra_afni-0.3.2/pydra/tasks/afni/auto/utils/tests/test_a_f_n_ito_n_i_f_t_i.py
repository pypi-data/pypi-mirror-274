from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.a_f_n_ito_n_i_f_t_i import a_f_n_ito_n_i_f_t_i
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_a_f_n_ito_n_i_f_t_i_1():
    task = a_f_n_ito_n_i_f_t_i()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.out_file = Nifti1.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
