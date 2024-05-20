from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.preprocess.align_epi_anat_py import AlignEpiAnatPy
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_alignepianatpy_1():
    task = AlignEpiAnatPy()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.anat = Nifti1.sample(seed=1)
    task.inputs.suffix = "_al"
    task.inputs.volreg = "on"
    task.inputs.tshift = "on"
    task.inputs.py27_path = "python2"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_alignepianatpy_2():
    task = AlignEpiAnatPy()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.anat = Nifti1.sample(seed=1)
    task.inputs.epi_base = 0
    task.inputs.save_skullstrip = True
    task.inputs.epi_strip = "3dAutomask"
    task.inputs.volreg = "off"
    task.inputs.tshift = "off"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
