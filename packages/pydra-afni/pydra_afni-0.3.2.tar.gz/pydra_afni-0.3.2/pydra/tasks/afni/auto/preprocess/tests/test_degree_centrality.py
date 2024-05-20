from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.degree_centrality import degree_centrality
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_degree_centrality_1():
    task = degree_centrality()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.sparsity = 1  # keep the top one percent of connections
    task.inputs.mask = Nifti1.sample(seed=3)
    task.inputs.out_file = Nifti1.sample(seed=10)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
