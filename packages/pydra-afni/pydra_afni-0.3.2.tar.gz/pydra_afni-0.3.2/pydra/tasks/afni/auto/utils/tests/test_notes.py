from fileformats.generic import File
from fileformats.medimage_afni import Head
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.afni.auto.utils.notes import Notes
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_notes_1():
    task = Notes()
    task.inputs.in_file = Head.sample(seed=0)
    task.inputs.out_file = File.sample(seed=6)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_notes_2():
    task = Notes()
    task.inputs.in_file = Head.sample(seed=0)
    task.inputs.add = "This note is added."
    task.inputs.add_history = "This note is added to history."
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
