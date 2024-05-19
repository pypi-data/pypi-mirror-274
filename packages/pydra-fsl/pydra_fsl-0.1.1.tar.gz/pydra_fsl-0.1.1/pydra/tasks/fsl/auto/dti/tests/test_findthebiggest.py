from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.dti.find_the_biggest import FindTheBiggest
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_findthebiggest_1():
    task = FindTheBiggest()
    task.inputs.in_files = [File.sample(seed=0)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_findthebiggest_2():
    task = FindTheBiggest()
    task.inputs.in_files = [File.sample(seed=0)]
    task.inputs.out_file = "biggestSegmentation"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
